"""
Skeptic Evidence Challenge Engine.
Audits claims for unsupported assertions, missing validation environments,
negated achievements, planned future work, and internal document contradictions.
"""

from typing import List, Optional, Tuple
from trl_core.models import (
    AgentAssessment,
    AgentType,
    ContradictionItem,
    DebateMessage,
    EvidenceItem,
    EvidenceStrength,
    ModalityType,
    TechnicalClaim,
)
from trl_core.trl_definitions import get_trl_definition


class SkepticReviewer:
    """
    Constructs the rigorous adversarial challenge against unverified readiness assertions.
    Focuses on missing operational validation, future work masquerading as completed, and contradictions.
    """

    def evaluate_initial_position(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
        contradictions: Optional[List[ContradictionItem]] = None,
    ) -> Tuple[int, AgentAssessment]:
        """
        Determine initial skeptic stance. Typically advocates for candidate_trl - 1 or level with unassailable data.
        """
        contradictions = contradictions or []
        has_high_conflict = any(c.severity == "HIGH" for c in contradictions)

        # If contradictions exist, pull back harder
        if has_high_conflict:
            skeptic_trl = max(1, candidate_trl - 2)
        else:
            skeptic_trl = max(1, candidate_trl - 1)

        definition = get_trl_definition(candidate_trl)
        reasoning = (
            f"Skeptic audit flags that full operational demonstration for {definition.title} (TRL {candidate_trl}) "
            f"lacks exhaustive multi-mission qualification. Bounding stance at TRL {skeptic_trl} "
            f"pending direct verification of all mandatory environmental criteria."
        )

        assessment = AgentAssessment(
            agent_type=AgentType.SKEPTIC,
            initial_trl=skeptic_trl,
            final_trl=candidate_trl if not has_high_conflict else skeptic_trl,
            reasoning=reasoning,
            evidence_references=[c.claim_id_b for c in contradictions[:2]],
            confidence=0.85,
        )
        return skeptic_trl, assessment

    def generate_opening_challenge(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
    ) -> DebateMessage:
        """
        Generate Round 1 challenge identifying missing criteria or lack of higher validation.
        """
        definition = get_trl_definition(candidate_trl)
        next_trl = min(9, candidate_trl + 1)
        next_def = get_trl_definition(next_trl)

        arg_text = (
            f"We challenge the assertion of readiness beyond TRL {candidate_trl}. While evidence supports "
            f"aspects of {definition.title}, the record lacks verified qualification for TRL {next_trl} "
            f"({next_def.title}) in {next_def.required_environment}. Unproven assumptions cannot substitute "
            f"for empirical data under actual mission stress."
        )

        return DebateMessage(
            round_number=1,
            agent_type=AgentType.SKEPTIC,
            argument=arg_text,
            evidence_references=[],
        )

    def generate_counter_rebuttal(
        self,
        candidate_trl: int,
        contradictions: List[ContradictionItem],
        negated_claims: List[TechnicalClaim],
    ) -> DebateMessage:
        """
        Generate Round 2 counter-rebuttal highlighting specific contradictions and planned/negated milestones.
        """
        ref_ids: List[str] = []
        if contradictions:
            c = contradictions[0]
            ref_ids.append(c.id)
            arg_text = (
                f"We must scrutinize document tension [{c.id}]: {c.explanation}. "
                f"An assertion of high readiness is invalid when the text explicitly discloses that "
                f"operational milestones remain planned, hypothetical, or unperformed."
            )
        elif negated_claims:
            neg = negated_claims[0]
            ref_ids.append(neg.id)
            arg_text = (
                f"Source claim [{neg.id}] explicitly discloses: \"{neg.verbatim_quote}\" was not completed. "
                f"Advancement to TRL {candidate_trl + 1} is legally and technically blocked by this admitted gap."
            )
        else:
            arg_text = (
                f"Advancement is blocked by absence of developmental qualification testing. "
                f"We concede TRL {candidate_trl} only under strict condition that implied prerequisite audits "
                f"are formally registered and unrecorded criteria are documented."
            )

        return DebateMessage(
            round_number=2,
            agent_type=AgentType.SKEPTIC,
            argument=arg_text,
            evidence_references=ref_ids,
        )
