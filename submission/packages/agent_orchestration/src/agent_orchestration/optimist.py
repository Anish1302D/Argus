"""
Optimist Evidence Argumentation Engine.
Identifies the strongest defensible maturity evidence and constructs
evidence-grounded arguments citing verified evidence IDs, quantitative metrics,
and official TRL criteria.
"""

from typing import List, Tuple
from trl_core.models import (
    AgentAssessment,
    AgentType,
    DebateMessage,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    TechnicalClaim,
)
from trl_core.trl_definitions import get_trl_definition


class OptimistReviewer:
    """
    Constructs the strongest evidence-backed position advocating for the highest defensible TRL.
    Every argument explicitly cites evidence IDs and quantitative empirical data.
    """

    def evaluate_initial_position(
        self,
        evidence_items: List[EvidenceItem],
        claims: List[TechnicalClaim],
    ) -> Tuple[int, AgentAssessment]:
        """
        Determine initial optimist TRL stance based on verified supporting evidence.
        """
        strong_items = [e for e in evidence_items if e.strength == EvidenceStrength.STRONG_SUPPORTING]
        all_trls = [e.target_trl for e in evidence_items if e.target_trl is not None and e.strength != EvidenceStrength.CONTRADICTORY]

        # Highest level with supporting evidence
        highest_trl = max(all_trls, default=1)
        supporting_ids = [e.id for e in strong_items[:3]] or [e.id for e in evidence_items[:2]]

        definition = get_trl_definition(highest_trl)
        reasoning = (
            f"The technical documentation presents verified empirical evidence demonstrating "
            f"maturity at {definition.title} (TRL {highest_trl}). "
            f"Key engineering milestones have been validated under required conditions with "
            f"{len(strong_items)} strong evidence item(s)."
        )

        assessment = AgentAssessment(
            agent_type=AgentType.OPTIMIST,
            initial_trl=highest_trl,
            final_trl=highest_trl,
            reasoning=reasoning,
            evidence_references=supporting_ids,
            confidence=0.88 if strong_items else 0.72,
        )
        return highest_trl, assessment

    def generate_opening_argument(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
    ) -> DebateMessage:
        """
        Generate Round 1 opening argument advocating for candidate TRL with specific evidence citations.
        """
        matching_ev = [e for e in evidence_items if e.target_trl == candidate_trl and e.strength != EvidenceStrength.CONTRADICTORY]
        definition = get_trl_definition(candidate_trl)
        ev_refs = [e.id for e in matching_ev[:3]]

        # Incorporate quantitative snippets
        snippets = []
        for e in matching_ev[:2]:
            snippets.append(f"[{e.id}: \"{e.evidence_text[:120].strip()}...\"]")
        citation_text = " ".join(snippets) if snippets else f"[{matching_ev[0].id}]" if matching_ev else ""

        arg_text = (
            f"We argue for TRL {candidate_trl} ({definition.title}). The record establishes tangible engineering "
            f"progress satisfying core criteria in {definition.required_environment}. Specifically, verified evidence "
            f"{citation_text} confirms that required subsystem capabilities have been physically demonstrated."
        )

        return DebateMessage(
            round_number=1,
            agent_type=AgentType.OPTIMIST,
            argument=arg_text,
            evidence_references=ev_refs,
        )

    def generate_rebuttal(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
        skeptic_challenges: List[str],
    ) -> DebateMessage:
        """
        Generate Round 2 rebuttal defending against Skeptic objections using prerequisite rules and metrics.
        """
        strong_ev = [e for e in evidence_items if e.strength == EvidenceStrength.STRONG_SUPPORTING]
        ev_refs = [e.id for e in strong_ev[:3]]

        challenge_summary = skeptic_challenges[0] if skeptic_challenges else "missing historical bench notes"
        arg_text = (
            f"In response to the Skeptic's challenge regarding {challenge_summary}: per APCTT and NASA guidelines, "
            f"when higher-tier integration at TRL {candidate_trl} is empirically validated with quantitative data "
            f"({len(strong_ev)} strong record(s)), foundational analytical prerequisites are implied. "
            f"Rigorous telemetry and repeatability supersede unrecorded early-stage notes."
        )

        return DebateMessage(
            round_number=2,
            agent_type=AgentType.OPTIMIST,
            argument=arg_text,
            evidence_references=ev_refs,
        )
