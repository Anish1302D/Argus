"""
Internal Format Adapters.
Implements the internal baseline specification described in PRD §12.2.
Guarantees zero guesswork regarding the unconfirmed official competition submission schema.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union
from trl_core.adapters.base import BaseInputAdapter, BaseOutputAdapter
from trl_core.models import Chunk, Document, FinalAssessment
from trl_core.sanitizer import sanitize_text


class InternalInputAdapter(BaseInputAdapter):
    """
    Default internal input adapter for plain text and raw technical reports.
    Reads UTF-8 encoded files and constructs canonical Document and Chunk objects.
    """

    def load_document(self, source: Union[str, Path]) -> Document:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path.resolve()}")
        if not path.is_file():
            raise ValueError(f"Path is not a regular file: {path.resolve()}")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback with error handling for non-utf8 documents
            content = path.read_text(encoding="latin-1")

        if not content.strip():
            raise ValueError(f"Input document is empty: {path.resolve()}")

        # Chunk document by paragraphs
        raw_paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks: List[Chunk] = []
        doc_id = path.stem

        current_offset = 0
        for idx, paragraph in enumerate(raw_paragraphs):
            # Locate paragraph in original content
            start_pos = content.find(paragraph, current_offset)
            if start_pos == -1:
                start_pos = current_offset
            end_pos = start_pos + len(paragraph)
            current_offset = end_pos

            sanitized = sanitize_text(paragraph)
            chunk = Chunk(
                id=f"{doc_id}_chunk_{idx + 1:03d}",
                document_id=doc_id,
                text=sanitized.cleaned_text,
                page_number=1,  # Single-page assumption for raw text unless multi-page metadata provided
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
                "source_path": str(path.resolve()),
                "file_size_bytes": path.stat().st_size,
                "chunk_count": len(chunks),
                "adapter": "InternalInputAdapter"
            }
        )

    def load_batch(self, source_dir: Union[str, Path]) -> List[Document]:
        dir_path = Path(source_dir)
        if not dir_path.exists():
            raise FileNotFoundError(f"Input directory not found: {dir_path.resolve()}")
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path.resolve()}")

        eligible_extensions = {".txt", ".md", ".json"}
        files = [f for f in sorted(dir_path.iterdir()) if f.is_file() and f.suffix.lower() in eligible_extensions]

        if not files:
            raise ValueError(f"No supported text documents found in directory: {dir_path.resolve()}")

        documents: List[Document] = []
        for file in files:
            documents.append(self.load_document(file))
        return documents


class InternalOutputAdapter(BaseOutputAdapter):
    """
    Default internal output adapter implementing the PRD §12.2 internal representation:
    {
      "predicted_trl": 5,
      "confidence": 0.82,
      "supporting_evidence": [...],
      "missing_criteria": [...],
      "contradictions": [...],
      "reasoning_summary": "...",
      "implied_prerequisites_audit": [...]
    }
    """

    def format_assessment(self, assessment: FinalAssessment) -> Dict[str, Any]:
        """Convert a canonical FinalAssessment into the internal JSON-compatible dictionary."""
        return {
            "predicted_trl": assessment.predicted_trl,
            "confidence": round(assessment.confidence, 4),
            "reasoning_summary": assessment.justification,
            "satisfied_criteria": assessment.satisfied_criteria,
            "missing_criteria": assessment.missing_criteria,
            "contradictions": assessment.contradictions,
            "recommendations": assessment.recommendations,
            "implied_prerequisites_audit": [
                audit.model_dump() for audit in assessment.implied_prerequisites_audit
            ],
            "supporting_evidence": [
                {
                    "evidence_id": item.id,
                    "text": item.evidence_text,
                    "page_number": item.page_number,
                    "category": item.category.value,
                    "strength": item.strength.value,
                    "confidence": round(item.confidence, 4),
                }
                for item in assessment.supporting_evidence
            ],
        }

    def write_assessment(self, assessment: FinalAssessment, destination: Union[str, Path]) -> Path:
        out_path = Path(destination)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        payload = self.format_assessment(assessment)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return out_path

