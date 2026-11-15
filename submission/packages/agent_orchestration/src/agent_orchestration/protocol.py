"""
Formal Multi-Agent Debate Protocol Engine.
Orchestrates structured adversarial exchanges between Optimist and Skeptic,
followed by definitive Referee adjudication.
Guarantees bit-for-bit deterministic reproducibility across runs (Issue 15).
"""

from typing import Any, Dict, List, Optional, Tuple
from trl_core.models import (
    AgentAssessment,
    AgentType,
    ContradictionItem,
    CriteriaMapping,
    DebateMessage,
    EvidenceItem,
    TechnicalClaim,
)
from agent_orchestration.optimist import OptimistReviewer
from agent_orchestration.skeptic import SkepticReviewer
from agent_orchestration.referee import RefereeAdjudicator


class ReviewProtocol:
    """
    Formal, bounded adversarial review protocol orchestrating:
    - Optimist argumentation (Issue 12)
    - Skeptic challenge (Issue 13)
    - Referee adjudication ledger (Issue 14)
    - 100% deterministic reproducibility (Issue 15)
    """

    def __init__(self, methodology_version: str = "2.0.0-argus"):
        self.methodology_version = methodology_version
        self.optimist = OptimistReviewer()
        self.skeptic = SkepticReviewer()
        self.referee = RefereeAdjudicator()

    def run_debate(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
        claims: List[TechnicalClaim],
        contradictions: Optional[List[ContradictionItem]] = None,
        criteria_mappings: Optional[List[CriteriaMapping]] = None,
    ) -> Tuple[List[DebateMessage], Dict[str, AgentAssessment], int, str, Any, Dict[str, Any]]:
        """
        Execute the deterministic review protocol.
        Returns:
            debate_transcript: List[DebateMessage]
            agent_assessments: Dict[str, AgentAssessment]
            final_trl: int
            justification: str
            implied_prerequisites: List[ImpliedPrerequisiteAudit]
            adjudication_ledger: Dict[str, Any]
        """
        contradictions = contradictions or []
        criteria_mappings = criteria_mappings or []

        # 1. Evaluate independent positions
        opt_trl, opt_assessment = self.optimist.evaluate_initial_position(evidence_items, claims)
        skep_trl, skep_assessment = self.skeptic.evaluate_initial_position(candidate_trl, evidence_items, contradictions)

        # 2. Round 1: Opening Arguments
        msg_r1_opt = self.optimist.generate_opening_argument(candidate_trl, evidence_items)
        msg_r1_skep = self.skeptic.generate_opening_challenge(candidate_trl, evidence_items)

        # 3. Round 2: Targeted Rebuttal & Contradiction Scrutiny
        skeptic_challenges = [msg_r1_skep.argument]
        msg_r2_opt = self.optimist.generate_rebuttal(candidate_trl, evidence_items, skeptic_challenges)
        neg_claims = [c for c in claims if c.modality.value in ("negated", "unperformed")]
        msg_r2_skep = self.skeptic.generate_counter_rebuttal(candidate_trl, contradictions, neg_claims)

        transcript = [msg_r1_opt, msg_r1_skep, msg_r2_opt, msg_r2_skep]

        # 4. Referee Adjudication
        final_trl, justification, implied_audits, ref_assessment, adj_ledger = self.referee.adjudicate_debate(
            candidate_trl=candidate_trl,
            evidence_items=evidence_items,
            claims=claims,
            contradictions=contradictions,
            criteria_mappings=criteria_mappings,
        )

        agent_assessments = {
            "optimist": opt_assessment.model_copy(update={"final_trl": final_trl}),
            "skeptic": skep_assessment.model_copy(update={"final_trl": final_trl}),
            "referee": ref_assessment,
        }

        return transcript, agent_assessments, final_trl, justification, implied_audits, adj_ledger
