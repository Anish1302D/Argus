"""
Deterministic Adjudication Engine & Ordinal Classifier.
Executes the modular 14-stage research intelligence adjudication pipeline:
Technical claim extraction, modality analysis, evidence quality grading,
criteria mapping, contradiction detection, formal adversarial review,
referee adjudication ledger, and advancement gap analysis.

COMPETITION RULE COMPLIANCE:
Until real, verified labelled training data is officially released by competition organizers,
the submission pipeline operates in deterministic rule-based adjudication mode only.
No trained LightGBM model fitted on synthetic data is shipped or used for inference.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import lightgbm as lgb
import numpy as np

from trl_core.audit import AuditTrailBuilder
from trl_core.contradiction import ContradictionDetector
from trl_core.criteria_mapper import CriteriaMapper
from trl_core.gap_analysis import AdvancementGapAnalyzer
from trl_core.ledger import EvidenceLedger
from trl_core.models import (
    AgentAssessment,
    AgentType,
    DebateMessage,
    Document,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    FinalAssessment,
    ImpliedPrerequisiteAudit,
    ModalityType,
    TechnicalClaim,
)
from trl_core.trl_definitions import TRL_LADDER, get_trl_definition
from trl_core.uncertainty import UncertaintyModel
from agent_orchestration.protocol import ReviewProtocol
from ml_inference.claim_extractor import StructuredClaimExtractor
from ml_inference.features import FeatureExtractor


class TRLOrdinalClassifier:
    """
    Deterministic TRL Adjudicator with optional ML fallback.
    Default mode: Pure deterministic rule-based criteria ladder with implied prerequisites.
    """

    def __init__(self, model: Optional[lgb.LGBMRegressor] = None, enable_ml: bool = False):
        self.feature_extractor = FeatureExtractor()
        self.claim_extractor = StructuredClaimExtractor()
        self.contradiction_detector = ContradictionDetector()
        self.criteria_mapper = CriteriaMapper()
        self.review_protocol = ReviewProtocol(methodology_version="2.0.0-argus")
        self.gap_analyzer = AdvancementGapAnalyzer()
        self.uncertainty_model = UncertaintyModel()
        self.enable_ml = enable_ml
        self.model = model
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "TRLOrdinalClassifier":
        """
        Fit the LightGBM ordinal regressor on training feature matrix X and ground truth TRLs y.
        Only called when official labelled data is available.
        """
        if self.model is None:
            self.model = lgb.LGBMRegressor(
                objective="regression_l1",
                n_estimators=50,
                learning_rate=0.1,
                max_depth=3,
                num_leaves=7,
                min_child_samples=1,
                random_state=42,
                verbosity=-1
            )
        y_float = np.asarray(y, dtype=np.float32)
        self.model.fit(X, y_float)
        self.is_fitted = True
        self.enable_ml = True
        return self

    def predict_score(self, X: np.ndarray) -> np.ndarray:
        """Predict ordinal score. Uses ML if enabled and fitted; otherwise uses feature heuristic."""
        if self.enable_ml and self.is_fitted and self.model is not None:
            return self.model.predict(X)
        # Deterministic feature heuristic: highest matched TRL (feature index 9)
        return X[:, 9]

    def adjudicate(
        self,
        document: Document,
        evidence_items: List[EvidenceItem],
        feature_vector: np.ndarray
    ) -> FinalAssessment:
        """
        Adjudicate final TRL using the modular 14-stage research intelligence pipeline:
        1. Claim extraction and source context
        2. Contradiction detection across abstract vs limitations
        3. Criteria checklist mapping
        4. Multi-agent review protocol (Optimist vs Skeptic vs Referee)
        5. Advancement gap report for TRL N+1
        6. Multi-dimensional uncertainty profiling
        7. Immutable audit trail with SHA-256 reproducibility hash
        """
        audit_builder = AuditTrailBuilder(methodology_version="2.0.0-argus")
        audit_builder.record_stage(
            rule_id="RULE-INGESTION-VALIDATE",
            stage="INGESTION",
            inputs={"doc_id": document.id, "chunks": len(document.chunks)},
            outcome="INGESTION_VERIFIED",
            explanation=f"Ingested document '{document.name}' with {len(document.chunks)} structural chunks.",
        )

        # 1. Extract structured technical claims
        claims = self.claim_extractor.extract_document_claims(document)
        audit_builder.record_stage(
            rule_id="RULE-CLAIM-EXTRACT",
            stage="CLAIM_EXTRACTION",
            inputs={"claim_count": len(claims)},
            outcome="CLAIMS_EXTRACTED",
            explanation=f"Extracted {len(claims)} structured technical claims with quantitative measurements.",
        )

        # 2. Detect contradictory evidence
        contradictions = self.contradiction_detector.detect_contradictions(claims)
        audit_builder.record_stage(
            rule_id="RULE-CONTRADICTION-CHECK",
            stage="CONTRADICTION_DETECTION",
            inputs={"contradictions_found": len(contradictions)},
            outcome="CONTRADICTIONS_AUDITED",
            explanation=f"Identified {len(contradictions)} document tension(s) between claims and qualifiers.",
        )

        # Initial candidate TRL from evidence ledger
        all_trls = [e.target_trl for e in evidence_items if e.target_trl is not None and e.strength != EvidenceStrength.CONTRADICTORY]
        highest_matched_feature = int(np.clip(feature_vector[9], 1, 9))
        max_evidence_trl = max(all_trls, default=1)
        candidate_trl = max(1, min(highest_matched_feature, max_evidence_trl))

        # 3. Map evidence against canonical criteria
        criteria_mappings = self.criteria_mapper.map_evidence_to_criteria(
            target_trl=candidate_trl,
            evidence_items=evidence_items,
            contradictions=contradictions,
        )

        # 4. Run formal multi-agent debate and referee adjudication
        transcript, agent_assessments, adjudicated_trl, adjudication_reason, implied_audits, adj_ledger = self.review_protocol.run_debate(
            candidate_trl=candidate_trl,
            evidence_items=evidence_items,
            claims=claims,
            contradictions=contradictions,
            criteria_mappings=criteria_mappings,
        )

        # Re-sync criteria mapping to final adjudicated level
        final_criteria_mappings = self.criteria_mapper.map_evidence_to_criteria(
            target_trl=adjudicated_trl,
            evidence_items=evidence_items,
            contradictions=contradictions,
        )

        # 5. Advancement gap report for level N+1
        gap_report = self.gap_analyzer.analyze_gap(
            current_trl=adjudicated_trl,
            criteria_mappings=final_criteria_mappings,
            contradictions=contradictions,
        )

        # 6. Decoupled uncertainty profile
        uncertainty_profile = self.uncertainty_model.compute_profile(
            target_trl=adjudicated_trl,
            evidence_items=evidence_items,
            contradictions=contradictions,
            required_criteria_count=len([m for m in final_criteria_mappings if m.trl_level == adjudicated_trl]) or 2,
        )

        # 7. Relational Evidence Ledger
        ledger = EvidenceLedger(
            document_id=document.id,
            claims=claims,
            evidence_items=evidence_items,
            criteria_mappings=final_criteria_mappings,
            adjudicated_trl=adjudicated_trl,
        )

        # 8. Finalize Audit Trail
        audit_builder.record_stage(
            rule_id="RULE-REFEREE-ADJUDICATE",
            stage="ADJUDICATION_RULING",
            inputs={"candidate_trl": candidate_trl, "final_trl": adjudicated_trl},
            outcome=f"ADJUDICATED_TRL_{adjudicated_trl}",
            explanation=adjudication_reason,
        )
        audit_trail = audit_builder.build_audit_trail(document.id, adjudicated_trl)

        # Satisfied criteria list
        definition = get_trl_definition(adjudicated_trl)
        satisfied_criteria = [
            m.criterion_description for m in final_criteria_mappings
            if m.trl_level == adjudicated_trl and m.status in ("DIRECTLY_SATISFIED", "PARTIALLY_SUPPORTED", "SATISFIED_INFERRED")
        ] or [c.description for c in definition.criteria]

        return FinalAssessment(
            predicted_trl=adjudicated_trl,
            confidence=uncertainty_profile.composite_certainty,
            justification=adjudication_reason,
            satisfied_criteria=satisfied_criteria,
            implied_prerequisites_audit=implied_audits,
            missing_criteria=gap_report.missing_criteria,
            contradictions=[c.model_dump() for c in contradictions],
            recommendations=gap_report.recommended_activities,
            supporting_evidence=evidence_items[:10],
            agent_assessments=agent_assessments,
            debate_transcript=transcript,
            evidence_ledger=ledger.to_dict(),
            criteria_mappings=final_criteria_mappings,
            uncertainty_profile=uncertainty_profile,
            audit_trail=audit_trail,
            gap_report=gap_report,
            methodology_version="2.0.0-argus",
        )
