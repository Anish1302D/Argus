"""
Evidence Confidence and Uncertainty Model.
Decouples extraction confidence, evidence completeness, criteria coverage,
source reliability, and assessment certainty.
Explicitly avoids representing uncalibrated heuristics as calibrated probabilities.
"""

from typing import List, Optional
from trl_core.models import (
    ContradictionItem,
    EvidenceItem,
    EvidenceStrength,
    UncertaintyProfile,
)


class UncertaintyModel:
    """
    Computes an inspectable, multi-dimensional uncertainty profile.
    Separates extraction confidence from criteria coverage and contradiction penalties.
    """

    def compute_profile(
        self,
        target_trl: int,
        evidence_items: List[EvidenceItem],
        contradictions: List[ContradictionItem],
        required_criteria_count: int = 3,
    ) -> UncertaintyProfile:
        """
        Compute decoupled uncertainty metrics for the final adjudicated assessment.
        """
        # 1. Extraction confidence: average confidence of supporting items
        supporting_items = [e for e in evidence_items if e.strength != EvidenceStrength.CONTRADICTORY]
        if supporting_items:
            avg_extraction_conf = sum(e.confidence for e in supporting_items) / len(supporting_items)
        else:
            avg_extraction_conf = 0.50

        # 2. Criteria coverage: ratio of verified criteria relative to canonical requirement
        strong_supporting = [e for e in supporting_items if e.strength == EvidenceStrength.STRONG_SUPPORTING]
        moderate_supporting = [e for e in supporting_items if e.strength == EvidenceStrength.MODERATE_SUPPORTING]
        
        effective_evidence_score = (len(strong_supporting) * 1.0) + (len(moderate_supporting) * 0.5)
        criteria_coverage = min(1.0, max(0.2, effective_evidence_score / max(1, required_criteria_count)))

        # 3. Conflict penalty: penalty applied for unresolved contradictions
        unresolved_contradictions = [c for c in contradictions if c.resolved_status == "UNRESOLVED"]
        high_severity_conflicts = [c for c in unresolved_contradictions if c.severity == "HIGH"]
        conflict_penalty = min(0.40, (len(high_severity_conflicts) * 0.15) + (len(unresolved_contradictions) * 0.05))

        # 4. Composite certainty: calibrated combination of extraction, coverage, and conflict
        base_certainty = (avg_extraction_conf * 0.4) + (criteria_coverage * 0.6)
        composite_certainty = max(0.10, min(0.98, base_certainty - conflict_penalty))

        # 5. Methodological notes
        notes = [
            f"Extraction confidence ({avg_extraction_conf:.2f}) represents linguistic milestone recognition reliability.",
            f"Criteria coverage ({criteria_coverage:.2f}) reflects ratio of verified empirical evidence to required checklist items.",
            "Confidence representation is heuristic-bounded; competition air-gap constraints preclude uncalibrated statistical overfitting.",
        ]
        if conflict_penalty > 0:
            notes.append(f"Conflict penalty (-{conflict_penalty:.2f}) applied due to {len(unresolved_contradictions)} unresolved document tension(s).")

        return UncertaintyProfile(
            extraction_confidence=round(avg_extraction_conf, 3),
            criteria_coverage=round(criteria_coverage, 3),
            conflict_penalty=round(conflict_penalty, 3),
            composite_certainty=round(composite_certainty, 3),
            calibration_status="UNCALIBRATED_HEURISTIC",
            notes=notes,
        )
