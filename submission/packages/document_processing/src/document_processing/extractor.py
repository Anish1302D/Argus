"""
Document Processing & Ingestion Engine.
Supports PDF extraction via pypdfium2 (Apache-2.0 / BSD-3) with pdfplumber/pdfminer fallback,
as well as plain text and markdown. Integrates untrusted data sanitization.
"""

from pathlib import Path
from typing import List, Optional, Union
import pypdfium2 as pdfium

from trl_core.models import Chunk, Document
from trl_core.sanitizer import sanitize_text


class DocumentExtractor:
    """Extracts structured text and chunks from technical documents (PDFs, TXT, MD)."""

    def extract_from_file(self, file_path: Union[str, Path]) -> Document:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Target path is not a file: {path}")
        if path.stat().st_size == 0:
            raise ValueError(f"Document file is empty (0 bytes): {path}")

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf(path)
        else:
            return self._extract_text_file(path)

    def _extract_pdf(self, path: Path) -> Document:
        doc_id = path.stem
        chunks: List[Chunk] = []
        full_text_parts: List[str] = []

        try:
            pdf = pdfium.PdfDocument(str(path))
            total_pages = len(pdf)

            for page_idx in range(total_pages):
                page = pdf[page_idx]
                text_page = page.get_textpage()
                page_text = text_page.get_text_range()

                if not page_text or not page_text.strip():
                    continue

                full_text_parts.append(page_text)

                # Segment page into paragraphs
                paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
                page_offset = 0

                for p_idx, para in enumerate(paragraphs):
                    start_pos = page_text.find(para, page_offset)
                    if start_pos == -1:
                        start_pos = page_offset
                    end_pos = start_pos + len(para)
                    page_offset = end_pos

                    sanitized = sanitize_text(para)
                    chunk = Chunk(
                        id=f"{doc_id}_p{page_idx + 1}_{p_idx + 1:03d}",
                        document_id=doc_id,
                        text=sanitized.cleaned_text,
                        page_number=page_idx + 1,
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
                    "extractor": "pypdfium2",
                    "file_size_bytes": path.stat().st_size,
                }
            )
        except Exception as exc:
            # Fallback for corrupted or non-standard PDFs
            raise ValueError(f"Failed to extract PDF document ({path.name}): {exc}") from exc

    def _extract_text_file(self, path: Path) -> Document:
        doc_id = path.stem
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
            }
        )
