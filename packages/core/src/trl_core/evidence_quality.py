"""
Evidence Classification and Quality Assessment Engine.
Evaluates evidence specificity, quantitative support, experimental context,
validation environments, reproducibility indicators, and evidence strength.
Prevents ungrounded keyword matches from being treated as conclusive proof.
"""

from typing import List, Optional
from trl_core.models import (
    EvidenceCategory,
    EvidenceStrength,
    EvidenceType,
    ModalityType,
    QuantitativeMeasurement,
    TechnicalClaim,
    ValidationEnvironment,
)


class EvidenceQualityAssessor:
    """
    Assesses the quality, specificity, and empirical strength of technical claims and evidence.
    Enforces that keyword presence alone is insufficient for strong readiness classification.
    """

    def assess_claim_quality(
        self,
        claim: TechnicalClaim,
        measurements: Optional[List[QuantitativeMeasurement]] = None
    ) -> EvidenceStrength:
        """
        Assess evidence strength based on quantitative support, modality, and environment.
        """
        measures = measurements or claim.measurements

        # 1. Negated or unperformed claims are contradictory or unverified
        if claim.modality == ModalityType.NEGATED:
            return EvidenceStrength.CONTRADICTORY
        if claim.modality in (ModalityType.UNPERFORMED, ModalityType.HYPOTHETICAL):
            return EvidenceStrength.UNVERIFIED_CLAIM
        if claim.modality == ModalityType.PLANNED:
            return EvidenceStrength.WEAK_SUPPORTING

        # 2. Check for quantitative support (presence of verified numbers, scientific units, sample sizes)
        has_quantitative = len(measures) > 0
        has_tolerance = any(m.tolerance is not None for m in measures)
        has_high_sample_size = any(
            m.value >= 10 and m.unit in ("runs", "cycles", "hours", "passes", "months", "days", "units")
            for m in measures
        )

        # 3. Environment check
        env = claim.validation_environment

        # High-TRL claims (TRL >= 6) REQUIRE relevant or operational environments
        if claim.candidate_trl >= 6:
            if env not in (ValidationEnvironment.RELEVANT_ENVIRONMENT, ValidationEnvironment.OPERATIONAL_SPACE_OR_FLIGHT):
                # Vague or laboratory-only claim claiming high TRL
                return EvidenceStrength.WEAK_SUPPORTING

        # 4. Strength grading
        if has_quantitative and (has_tolerance or has_high_sample_size or env in (ValidationEnvironment.OPERATIONAL_SPACE_OR_FLIGHT, ValidationEnvironment.RELEVANT_ENVIRONMENT, ValidationEnvironment.LABORATORY)):
            return EvidenceStrength.STRONG_SUPPORTING
        elif has_quantitative or env in (ValidationEnvironment.LABORATORY, ValidationEnvironment.RELEVANT_ENVIRONMENT):
            return EvidenceStrength.MODERATE_SUPPORTING
        else:
            # Pure keyword assertion without quantitative data or environment details
            return EvidenceStrength.WEAK_SUPPORTING

    def score_extraction_confidence(
        self,
        claim: TechnicalClaim,
        strength: EvidenceStrength
    ) -> float:
        """
        Produce a calibrated extraction confidence score.
        Separates extraction reliability from evidence completeness.
        """
        if strength == EvidenceStrength.CONTRADICTORY:
            return 0.88  # High confidence that contradiction exists
        if strength == EvidenceStrength.STRONG_SUPPORTING:
            return 0.92
        if strength == EvidenceStrength.MODERATE_SUPPORTING:
            return 0.80
        if strength == EvidenceStrength.WEAK_SUPPORTING:
            return 0.65
        return 0.50
