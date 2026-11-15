"""
Page-faithful multi-PDF extraction for ARGUS APCTT participant_module.
Uses pypdf, pypdfium2, and pdfplumber from the common base environment.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Union

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None

try:
    import pypdfium2 as pdfium
except ImportError:  # pragma: no cover
    pdfium = None

try:
    import pdfplumber
except ImportError:  # pragma: no cover
    pdfplumber = None


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
    """Extracts 1-based page texts from PDF documents."""

    def extract_pages_from_pdf(
        self,
        file_path: Union[str, Path],
        document_id: Optional[str] = None,
        document_date: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Tuple[List[ExtractedPage], int, str]:
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

        extractor_used = "pypdf" if pypdf_pages else ("pypdfium2" if pdfium_pages else "pdfplumber")
        return pages, total_pages, extractor_used
