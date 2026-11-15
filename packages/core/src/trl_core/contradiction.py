"""
Contradictory Evidence Detection Engine.
Identifies internal conflicts and discrepancies between claims, results,
limitations, and future-work sections across technical documents.
Preserves both sides with full provenance for Referee adjudication.
"""

from typing import List, Tuple
from trl_core.models import (
    ContradictionItem,
    EvidenceStrength,
    ModalityType,
    TechnicalClaim,
)


class ContradictionDetector:
    """
    Detects contradictory technical statements and evidence within a document.
    Ensures that high-maturity assertions in abstracts are challenged if contradicted
    by explicit limitations, absent milestones, or failure disclosures in the text.
    """

    def detect_contradictions(self, claims: List[TechnicalClaim]) -> List[ContradictionItem]:
        """
        Scan a collection of claims for conflicting statements regarding TRL milestones,
        validation environments, or achievement status.
        """
        contradictions: List[ContradictionItem] = []
        contra_counter = 1

        # Separate positive claims from negated / planned / limitation statements
        positive_claims = [
            c for c in claims
            if c.modality == ModalityType.COMPLETED and c.candidate_trl >= 3
        ]
        negated_or_limited_claims = [
            c for c in claims
            if c.modality in (ModalityType.NEGATED, ModalityType.UNPERFORMED, ModalityType.PLANNED)
        ]

        for pos in positive_claims:
            for neg in negated_or_limited_claims:
                # 1. Level clash: Same or higher candidate TRL mentioned as negated or planned
                if neg.candidate_trl >= pos.candidate_trl or (
                    neg.candidate_trl == pos.candidate_trl
                    and neg.modality == ModalityType.NEGATED
                ):
                    explanation = (
                        f"Conflict detected between completed claim '{pos.verbatim_quote}' "
                        f"(TRL {pos.candidate_trl}) and qualifying disclaimer '{neg.verbatim_quote}' "
                        f"(Modality: {neg.modality.value}, TRL {neg.candidate_trl})."
                    )
                    contra = ContradictionItem(
                        id=f"CONTRA-{contra_counter:03d}",
                        claim_id_a=pos.id,
                        claim_id_b=neg.id,
                        explanation=explanation,
                        severity="HIGH" if neg.modality == ModalityType.NEGATED else "MEDIUM",
                        resolved_status="UNRESOLVED",
                        resolution_rationale=None,
                    )
                    contradictions.append(contra)
                    contra_counter += 1

                # 2. General negation clash: neg claim explicitly mentions "no experiment", "no breadboard", "no flight"
                elif neg.modality == ModalityType.NEGATED and (
                    "no " in neg.text.lower() or "not yet" in neg.text.lower() or "without" in neg.text.lower()
                ):
                    # Check if neg text contradicts pos category
                    pos_cat_words = set(pos.achievement_category.lower().split())
                    neg_words = set(neg.text.lower().split())
                    overlap = pos_cat_words.intersection(neg_words)
                    if overlap and len(overlap) >= 2:
                        explanation = (
                            f"General negation statement '{neg.verbatim_quote}' conflicts with "
                            f"asserted milestone '{pos.verbatim_quote}'."
                        )
                        contra = ContradictionItem(
                            id=f"CONTRA-{contra_counter:03d}",
                            claim_id_a=pos.id,
                            claim_id_b=neg.id,
                            explanation=explanation,
                            severity="HIGH",
                            resolved_status="UNRESOLVED",
                            resolution_rationale=None,
                        )
                        contradictions.append(contra)
                        contra_counter += 1

        return contradictions
