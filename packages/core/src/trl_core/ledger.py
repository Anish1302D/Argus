"""
Evidence Ledger & Source Inspection Engine.
Provides a unified relational graph connecting:
Document -> Claim -> Evidence -> TRL Criterion -> Assessment Decision.
Supports bi-directional navigation, traceability lookups, and direct source inspection.
"""

from typing import Any, Dict, List, Optional
from trl_core.models import (
    CriteriaMapping,
    Document,
    EvidenceItem,
    SourceProvenance,
    TechnicalClaim,
)


class EvidenceLedger:
    """
    Relational Evidence Ledger maintaining explicit graph connections across:
    Document -> Claim -> Evidence -> Criterion -> Assessment Decision.
    """

    def __init__(
        self,
        document_id: str,
        claims: Optional[List[TechnicalClaim]] = None,
        evidence_items: Optional[List[EvidenceItem]] = None,
        criteria_mappings: Optional[List[CriteriaMapping]] = None,
        adjudicated_trl: Optional[int] = None,
    ):
        self.document_id = document_id
        self.claims: Dict[str, TechnicalClaim] = {c.id: c for c in (claims or [])}
        self.evidence: Dict[str, EvidenceItem] = {e.id: e for e in (evidence_items or [])}
        self.criteria: Dict[str, CriteriaMapping] = {c.criterion_id: c for c in (criteria_mappings or [])}
        self.adjudicated_trl = adjudicated_trl

        # Relational mapping indices
        self.claim_to_evidence: Dict[str, List[str]] = {}
        self.evidence_to_claims: Dict[str, List[str]] = {}
        self.criterion_to_evidence: Dict[str, List[str]] = {}
        self.evidence_to_criteria: Dict[str, List[str]] = {}

        self._build_indices()

    def _build_indices(self):
        """Construct bidirectional graph links."""
        for ev_id, ev in self.evidence.items():
            if ev.claim_id and ev.claim_id in self.claims:
                self.claim_to_evidence.setdefault(ev.claim_id, []).append(ev_id)
                self.evidence_to_claims.setdefault(ev_id, []).append(ev.claim_id)

        for crit_id, crit in self.criteria.items():
            for ev_id in crit.supporting_evidence_ids:
                self.criterion_to_evidence.setdefault(crit_id, []).append(ev_id)
                self.evidence_to_criteria.setdefault(ev_id, []).append(crit_id)

    def get_claims_for_evidence(self, evidence_id: str) -> List[TechnicalClaim]:
        """Lookup source claims underpinning an evidence item."""
        claim_ids = self.evidence_to_claims.get(evidence_id, [])
        return [self.claims[cid] for cid in claim_ids if cid in self.claims]

    def get_evidence_for_criterion(self, criterion_id: str) -> List[EvidenceItem]:
        """Lookup all evidence items satisfying or referencing a criterion."""
        ev_ids = self.criterion_to_evidence.get(criterion_id, [])
        return [self.evidence[eid] for eid in ev_ids if eid in self.evidence]

    def get_criteria_for_evidence(self, evidence_id: str) -> List[CriteriaMapping]:
        """Lookup all criteria supported by a specific evidence item."""
        crit_ids = self.evidence_to_criteria.get(evidence_id, [])
        return [self.criteria[cid] for cid in crit_ids if cid in self.criteria]

    def inspect_source_context(
        self,
        evidence_id: str,
        document_text: Optional[str] = None,
        context_padding: int = 150
    ) -> Dict[str, Any]:
        """
        Inspect the original source document context for an evidence item (Issue 10).
        Returns exact character offsets, verbatim quote, page, and surrounding context.
        """
        if evidence_id not in self.evidence:
            raise KeyError(f"Evidence item {evidence_id} not found in ledger")

        ev = self.evidence[evidence_id]
        src_ref = ev.source_reference or {}

        char_start = src_ref.get("char_start", 0)
        char_end = src_ref.get("char_end", 0)
        verbatim = ev.evidence_text

        context_window = ""
        if document_text and len(document_text) > 0:
            doc_len = len(document_text)
            start_bounded = max(0, min(char_start, doc_len))
            end_bounded = max(start_bounded, min(char_end, doc_len))

            ctx_start = max(0, start_bounded - context_padding)
            ctx_end = min(doc_len, end_bounded + context_padding)
            context_window = document_text[ctx_start:ctx_end]
            if not verbatim and end_bounded > start_bounded:
                verbatim = document_text[start_bounded:end_bounded]

        return {
            "evidence_id": ev.id,
            "document_id": ev.document_id,
            "page_number": ev.page_number,
            "section_name": ev.section_name,
            "char_offset_start": char_start,
            "char_offset_end": char_end,
            "verbatim_excerpt": verbatim,
            "context_window": context_window or verbatim,
            "target_trl": ev.target_trl,
            "strength": ev.strength.value if hasattr(ev.strength, "value") else str(ev.strength),
            "category": ev.category.value if hasattr(ev.category, "value") else str(ev.category),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize complete relational ledger to dictionary representation."""
        return {
            "document_id": self.document_id,
            "adjudicated_trl": self.adjudicated_trl,
            "total_claims": len(self.claims),
            "total_evidence_items": len(self.evidence),
            "total_criteria_mapped": len(self.criteria),
            "links": {
                "claim_to_evidence": self.claim_to_evidence,
                "evidence_to_criteria": self.evidence_to_criteria,
            },
            "claims": [c.model_dump() for c in self.claims.values()],
            "evidence_summary": [
                {
                    "id": e.id,
                    "target_trl": e.target_trl,
                    "strength": e.strength.value if hasattr(e.strength, "value") else str(e.strength),
                    "supported_criteria": self.evidence_to_criteria.get(e.id, []),
                }
                for e in self.evidence.values()
            ],
        }
