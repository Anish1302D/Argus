"""
Granular Source Provenance Engine.
Preserves character-level offsets, chunk identifiers, page numbers,
and verbatim excerpts linking extracted claims back to raw document source.
"""

from typing import Optional
from trl_core.models import Chunk, Document, SourceProvenance, TechnicalClaim


class ProvenanceEngine:
    """
    Manages granular character-level provenance between claims, evidence, and source text.
    Enforces that verbatim quotes match exact character slices in the underlying document.
    """

    def extract_provenance(
        self,
        document: Document,
        chunk: Chunk,
        claim: TechnicalClaim,
        context_padding: int = 150
    ) -> SourceProvenance:
        """
        Extract full source provenance including exact slice and surrounding context window.
        """
        raw_text = document.raw_content
        doc_len = len(raw_text)

        start = max(0, min(claim.char_offset_start, doc_len))
        end = max(start, min(claim.char_offset_end, doc_len))

        # Verbatim excerpt directly from slice
        verbatim = raw_text[start:end]
        if not verbatim:
            verbatim = claim.text

        # Context window surrounding the claim
        ctx_start = max(0, start - context_padding)
        ctx_end = min(doc_len, end + context_padding)
        context_window = raw_text[ctx_start:ctx_end]

        return SourceProvenance(
            document_id=document.id,
            chunk_id=chunk.id,
            page_number=chunk.page_number,
            section_name=chunk.section_name or claim.section_name,
            char_offset_start=start,
            char_offset_end=end,
            verbatim_excerpt=verbatim,
            context_window=context_window,
        )

    def verify_provenance_slice(self, raw_text: str, provenance: SourceProvenance) -> bool:
        """Verify that provenance character offsets faithfully reproduce the verbatim excerpt."""
        if provenance.char_offset_start >= len(raw_text) or provenance.char_offset_end > len(raw_text):
            return False
        slice_text = raw_text[provenance.char_offset_start:provenance.char_offset_end]
        return slice_text == provenance.verbatim_excerpt
