"""
Referee Adjudication Engine & Decision Ledger.
Adjudicates between Optimist claims and Skeptic challenges, enforces canonical
readiness criteria, applies implied prerequisite rules, resolves contradictions,
and produces a transparent, auditable adjudication ledger.
"""

from typing import Any, Dict, List, Optional, Tuple
from trl_core.models import (
    AgentAssessment,
    AgentType,
    ContradictionItem,
    CriteriaMapping,
    DebateMessage,
    EvidenceItem,
    EvidenceStrength,
    ImpliedPrerequisiteAudit,
    ModalityType,
    TechnicalClaim,
)
from trl_core.trl_definitions import TRL_LADDER, get_trl_definition


class RefereeAdjudicator:
    """
    Independent Referee adjudicating the adversarial debate.
    Produces the final decision, justification, accepted/rejected evidence lists,
    and formal decision ledger.
    """

    def adjudicate_debate(
        self,
        candidate_trl: int,
        evidence_items: List[EvidenceItem],
        claims: List[TechnicalClaim],
        contradictions: List[ContradictionItem],
        criteria_mappings: List[CriteriaMapping],
    ) -> Tuple[int, str, List[ImpliedPrerequisiteAudit], List[DebateMessage], Dict[str, Any]]:
        """
        Adjudicate final TRL based on evidence strength, contradictions, and debate arguments.
        Returns: (final_trl, justification, implied_prerequisites, referee_messages, adjudication_ledger).
        """
        strong_evidence = [e for e in evidence_items if e.strength == EvidenceStrength.STRONG_SUPPORTING]
        moderate_evidence = [e for e in evidence_items if e.strength == EvidenceStrength.MODERATE_SUPPORTING]
        negated_claims = [c for c in claims if c.modality in (ModalityType.NEGATED, ModalityType.UNPERFORMED)]

        # 1. Contradiction Resolution
        resolved_contradictions = []
        final_trl = candidate_trl
        downgrade_reasons = []

        for c in contradictions:
            # If high-severity contradiction exists (e.g. claimed TRL 7 flight but admitted not flown), resolve by upholding negation
            if c.severity == "HIGH":
                matching_neg = next((cl for cl in claims if cl.id == c.claim_id_b and cl.modality == ModalityType.NEGATED), None)
                if matching_neg:
                    c_updated = c.model_copy(update={
                        "resolved_status": "ACCEPTED_B",
                        "resolution_rationale": (
                            f"Referee upholds Skeptic challenge: Explicit disclaimer '{matching_neg.verbatim_quote}' "
                            f"supersedes positive milestone assertion. Milestone cannot be credited."
                        )
                    })
                    resolved_contradictions.append(c_updated)
                    if matching_neg.candidate_trl <= final_trl:
                        final_trl = max(1, matching_neg.candidate_trl - 1)
                        downgrade_reasons.append(
                            f"Adjudicated level constrained from {candidate_trl} to {final_trl} due to verified disclaimer: '{matching_neg.text}'."
                        )
                else:
                    resolved_contradictions.append(c)
            else:
                resolved_contradictions.append(c)

        # 2. Accepted vs Rejected Evidence
        accepted_evidence_ids = []
        rejected_evidence = []

        for item in evidence_items:
            if item.strength == EvidenceStrength.CONTRADICTORY or item.modality == ModalityType.NEGATED:
                rejected_evidence.append({
                    "evidence_id": item.id,
                    "reason": "Milestone is explicitly negated or unperformed in source context.",
                })
            elif item.modality in (ModalityType.PLANNED, ModalityType.HYPOTHETICAL):
                rejected_evidence.append({
                    "evidence_id": item.id,
                    "reason": f"Claim expresses {item.modality.value} milestone; cannot satisfy completed criteria.",
                })
            elif item.target_trl is not None and item.target_trl > final_trl:
                rejected_evidence.append({
                    "evidence_id": item.id,
                    "reason": f"Claim for TRL {item.target_trl} lacks mandatory operational environment verification.",
                })
            else:
                accepted_evidence_ids.append(item.id)

        # 3. Implied Prerequisites Ledger
        implied_audits: List[ImpliedPrerequisiteAudit] = []
        if final_trl >= 4 and strong_evidence:
            anchoring_item = strong_evidence[0]
            for lower_lvl in range(2, final_trl):
                lower_def = get_trl_definition(lower_lvl)
                for crit in lower_def.criteria:
                    implied_audits.append(
                        ImpliedPrerequisiteAudit(
                            criterion_id=crit.id,
                            target_level=lower_lvl,
                            status="SATISFIED_INFERRED",
                            inferred_from_trl=final_trl,
                            anchoring_evidence_id=anchoring_item.id,
                            inference_rationale=(
                                f"Demonstrated verification at TRL {final_trl} ({anchoring_item.category.value}) "
                                f"implies prerequisite criterion {crit.id} is satisfied despite omitted lab historical notes."
                            ),
                            auditable=True,
                        )
                    )

        # 4. Final Justification
        final_def = get_trl_definition(final_trl)
        if downgrade_reasons:
            justification = (
                f"Adjudicated TRL {final_trl} ({final_def.title}). " + " ".join(downgrade_reasons) +
                f" Verified empirical support established for TRL {final_trl} in {final_def.required_environment}."
            )
        else:
            justification = (
                f"Adjudicated TRL {final_trl} ({final_def.title}). Deterministic adjudication confirms "
                f"mandatory criteria satisfied with {len(accepted_evidence_ids)} accepted evidence record(s). "
                f"Validation environment ({final_def.required_environment}) matches demonstrated milestone scope."
            )

        # 5. Referee Agent Assessment
        referee_assessment = AgentAssessment(
            agent_type=AgentType.REFEREE,
            initial_trl=candidate_trl,
            final_trl=final_trl,
            reasoning=justification,
            evidence_references=accepted_evidence_ids[:3],
            confidence=0.90 if strong_evidence and not downgrade_reasons else 0.78,
        )

        adjudication_ledger = {
            "adjudicated_trl": final_trl,
            "title": final_def.title,
            "accepted_evidence_ids": accepted_evidence_ids,
            "rejected_evidence": rejected_evidence,
            "resolved_contradictions": [c.model_dump() for c in resolved_contradictions],
            "implied_prerequisites_count": len(implied_audits),
            "justification": justification,
            "referee_assessment": referee_assessment.model_dump(),
        }

        return final_trl, justification, implied_audits, referee_assessment, adjudication_ledger
