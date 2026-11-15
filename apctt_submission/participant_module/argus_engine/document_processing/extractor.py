"""
Document Processing & Ingestion Engine.
Supports PDF extraction via pypdfium2, pypdf, and pdfplumber/pdfminer fallback,
as well as plain text and markdown. Integrates untrusted data sanitization and
page-faithful multi-PDF extraction for APCTT cases.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import pypdfium2 as pdfium
except ImportError:  # pragma: no cover
    pdfium = None

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None

try:
    import pdfplumber
except ImportError:  # pragma: no cover
    pdfplumber = None

from trl_core.models import Chunk, Document
from trl_core.sanitizer import sanitize_text


@dataclass
class ExtractedPage:
    """Single 1-based page extracted from a document with verbatim text."""

    document_id: str
    page: int
    text: str
    pypdf_text: str = ""
    pdfium_text: str = ""
    document_date: Optional[str] = None
    title: Optional[str] = None


class DocumentExtractor:
    """Extracts structured text, pages, and chunks from technical documents (PDFs, TXT, MD)."""

    def extract_pages_from_pdf(
        self,
        file_path: Union[str, Path],
        document_id: Optional[str] = None,
        document_date: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Tuple[List[ExtractedPage], int, str]:
        """
        Extract 1-based page texts from a PDF file using pypdf and/or pypdfium2.
        Returns (pages, page_count, extractor_name).
        Raises ValueError if the PDF cannot be opened or contains 0 pages.
        """
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Target path is not a file: {path}")
        if path.stat().st_size == 0:
            raise ValueError(f"Document file is empty (0 bytes): {path}")

        doc_id = document_id or path.stem
        pypdf_pages: List[str] = []
        pdfium_pages: List[str] = []
        errors: List[str] = []

        # 1. Try pypdf (matches APCTT base environment reference reader)
        if PdfReader is not None:
            try:
                reader = PdfReader(str(path), strict=False)
                for p in reader.pages:
                    try:
                        pypdf_pages.append(p.extract_text() or "")
                    except Exception:
                        pypdf_pages.append("")
            except Exception as exc:
                errors.append(f"pypdf: {exc}")

        # 2. Try pypdfium2 (fast native PDFium extraction)
        if pdfium is not None:
            try:
                pdf = pdfium.PdfDocument(str(path))
                total = len(pdf)
                for idx in range(total):
                    try:
                        page = pdf[idx]
                        tp = page.get_textpage()
                        txt = tp.get_text_range() or ""
                        pdfium_pages.append(txt.replace("\r\n", "\n").replace("\r", "\n"))
                    except Exception:
                        pdfium_pages.append("")
                try:
                    pdf.close()
                except Exception:
                    pass
            except Exception as exc:
                errors.append(f"pypdfium2: {exc}")

        # 3. Fallback to pdfplumber if both pypdf and pypdfium2 failed to open
        plumber_pages: List[str] = []
        if not pypdf_pages and not pdfium_pages and pdfplumber is not None:
            try:
                with pdfplumber.open(str(path)) as pdf_pl:
                    for p in pdf_pl.pages:
                        plumber_pages.append(p.extract_text() or "")
            except Exception as exc:
                errors.append(f"pdfplumber: {exc}")

        total_pages = max(len(pypdf_pages), len(pdfium_pages), len(plumber_pages))
        if total_pages == 0:
            detail = "; ".join(errors) if errors else "no pages found"
            raise ValueError(f"Failed to extract PDF document ({path.name}): {detail}")

        pages: List[ExtractedPage] = []
        for idx in range(total_pages):
            p_pypdf = pypdf_pages[idx] if idx < len(pypdf_pages) else ""
            p_pdfium = pdfium_pages[idx] if idx < len(pdfium_pages) else ""
            p_plumber = plumber_pages[idx] if idx < len(plumber_pages) else ""

            # Prefer pypdf text when non-empty so supporting_span matches pypdf page text verbatim;
            # fall back to pdfium or pdfplumber if pypdf text is empty on that page.
            primary = p_pypdf if p_pypdf.strip() else (p_pdfium if p_pdfium.strip() else p_plumber)
            pages.append(
                ExtractedPage(
                    document_id=doc_id,
                    page=idx + 1,
                    text=primary,
                    pypdf_text=p_pypdf,
                    pdfium_text=p_pdfium,
                    document_date=document_date,
                    title=title,
                )
            )

        extractor_used = "pypdfium2" if pdfium_pages else ("pypdf" if pypdf_pages else "pdfplumber")
        return pages, total_pages, extractor_used

    def extract_from_file(
        self,
        file_path: Union[str, Path],
        document_id: Optional[str] = None,
    ) -> Document:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Target path is not a file: {path}")
        if path.stat().st_size == 0:
            raise ValueError(f"Document file is empty (0 bytes): {path}")

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf(path, document_id=document_id)
        else:
            return self._extract_text_file(path, document_id=document_id)

    def _extract_pdf(self, path: Path, document_id: Optional[str] = None) -> Document:
        doc_id = document_id or path.stem
        chunks: List[Chunk] = []
        full_text_parts: List[str] = []

        pages, total_pages, extractor_used = self.extract_pages_from_pdf(path, document_id=doc_id)

        for ep in pages:
            # For general Document extraction, prefer pdfium_text if richer, else ep.text
            page_text = ep.pdfium_text if ep.pdfium_text.strip() else ep.text
            if not page_text or not page_text.strip():
                continue

            full_text_parts.append(page_text)

            # Segment page into paragraphs
            paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
            if not paragraphs:
                paragraphs = [page_text.strip()]
            page_offset = 0

            for p_idx, para in enumerate(paragraphs):
                start_pos = page_text.find(para, page_offset)
                if start_pos == -1:
                    start_pos = page_offset
                end_pos = start_pos + len(para)
                page_offset = end_pos

                sanitized = sanitize_text(para)
                chunk = Chunk(
                    id=f"{doc_id}_p{ep.page}_{p_idx + 1:03d}",
                    document_id=doc_id,
                    text=sanitized.cleaned_text,
                    page_number=ep.page,
                    section_name=None,
                    char_offset_start=start_pos,
                    char_offset_end=end_pos,
                    is_sanitized=sanitized.is_safe,
                )
                chunks.append(chunk)

        raw_content = "\n\n".join(full_text_parts)
        if not raw_content.strip():
            raise ValueError(f"No extractable text found in PDF: {path}")

        return Document(
            id=doc_id,
            name=path.name,
            raw_content=raw_content,
            chunks=chunks,
            metadata={
                "source_path": str(path),
                "format": "pdf",
                "page_count": total_pages,
                "extractor": extractor_used,
                "file_size_bytes": path.stat().st_size,
            },
        )

    def _extract_text_file(self, path: Path, document_id: Optional[str] = None) -> Document:
        doc_id = document_id or path.stem
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="latin-1")

        if not content.strip():
            raise ValueError(f"Text file is empty: {path}")

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks: List[Chunk] = []
        offset = 0

        for idx, para in enumerate(paragraphs):
            start_pos = content.find(para, offset)
            if start_pos == -1:
                start_pos = offset
            end_pos = start_pos + len(para)
            offset = end_pos

            sanitized = sanitize_text(para)
            chunk = Chunk(
                id=f"{doc_id}_chunk_{idx + 1:03d}",
                document_id=doc_id,
                text=sanitized.cleaned_text,
                page_number=1,
                section_name=None,
                char_offset_start=start_pos,
                char_offset_end=end_pos,
                is_sanitized=sanitized.is_safe,
            )
            chunks.append(chunk)

        return Document(
            id=doc_id,
            name=path.name,
            raw_content=content,
            chunks=chunks,
            metadata={
                "source_path": str(path),
                "format": path.suffix.lstrip(".").lower() or "txt",
                "page_count": 1,
                "extractor": "plain_text",
                "file_size_bytes": path.stat().st_size,
            },
        )
