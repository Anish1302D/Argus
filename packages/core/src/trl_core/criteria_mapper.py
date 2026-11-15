"""
Evidence-to-TRL Criteria Mapping Engine.
Maps extracted evidence items to specific NASA/APCTT criteria checklists.
Distinguishes directly satisfied, partially supported, missing, contradictory,
and inferred criteria without conflating inferred prerequisites with direct empirical evidence.
"""

from typing import Dict, List, Optional
from trl_core.models import (
    ContradictionItem,
    CriteriaMapping,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    ModalityType,
)
from trl_core.trl_definitions import TRL_LADDER, TRLCriterion, get_trl_definition


class CriteriaMapper:
    """
    Evaluates evidence against official TRL 1-9 checklist criteria.
    Maps evidence IDs directly to criteria codes (e.g. TRL-4.1) with explicit status.
    """

    def map_evidence_to_criteria(
        self,
        target_trl: int,
        evidence_items: List[EvidenceItem],
        contradictions: Optional[List[ContradictionItem]] = None,
    ) -> List[CriteriaMapping]:
        """
        Produce exhaustive criteria mappings from TRL 1 up to target_trl + 1.
        """
        mappings: List[CriteriaMapping] = []
        contradictions = contradictions or []

        # Index evidence by target TRL
        evidence_by_trl: Dict[int, List[EvidenceItem]] = {lvl: [] for lvl in range(1, 10)}
        for item in evidence_items:
            if item.target_trl is not None and 1 <= item.target_trl <= 9:
                evidence_by_trl[item.target_trl].append(item)

        # Check for contradictory levels
        contradictory_trls = set()
        for c in contradictions:
            if c.resolved_status == "UNRESOLVED":
                # Mark high impact levels
                contradictory_trls.add(target_trl)

        # Evaluate from Level 1 up to min(9, target_trl + 1)
        max_eval_lvl = min(9, max(target_trl + 1, max(evidence_by_trl.keys(), default=1)))
        for lvl in range(1, max_eval_lvl + 1):
            definition = get_trl_definition(lvl)
            lvl_evidence = evidence_by_trl.get(lvl, [])
            strong_items = [e for e in lvl_evidence if e.strength == EvidenceStrength.STRONG_SUPPORTING]
            moderate_items = [e for e in lvl_evidence if e.strength == EvidenceStrength.MODERATE_SUPPORTING]
            contra_items = [e for e in lvl_evidence if e.strength == EvidenceStrength.CONTRADICTORY]

            for criterion in definition.criteria:
                status = "MISSING"
                supporting_ids: List[str] = []
                inferred_from = None
                rationale = ""

                # Check contradiction
                if contra_items or (lvl in contradictory_trls and lvl == target_trl):
                    status = "CONTRADICTORY"
                    supporting_ids = [e.id for e in contra_items]
                    rationale = f"Criterion challenged by contradictory document evidence or limitation disclosure."

                # Check direct empirical evidence
                elif strong_items:
                    status = "DIRECTLY_SATISFIED"
                    supporting_ids = [e.id for e in strong_items]
                    rationale = f"Directly satisfied by strong empirical evidence ({len(strong_items)} item(s))."

                elif moderate_items or lvl_evidence:
                    status = "PARTIALLY_SUPPORTED"
                    supporting_ids = [e.id for e in lvl_evidence]
                    rationale = f"Partially supported by moderate or qualitative evidence; lacks rigorous quantitative verification."

                # Check implied prerequisite inference
                elif lvl < target_trl and target_trl >= 4 and any(
                    e.strength == EvidenceStrength.STRONG_SUPPORTING for e in evidence_by_trl.get(target_trl, [])
                ):
                    status = "SATISFIED_INFERRED"
                    anchors = [e.id for e in evidence_by_trl.get(target_trl, []) if e.strength == EvidenceStrength.STRONG_SUPPORTING]
                    supporting_ids = anchors[:1]
                    inferred_from = target_trl
                    rationale = (
                        f"Inferred prerequisite: Verified integration at TRL {target_trl} implies foundational "
                        f"criterion {criterion.id} is satisfied despite omitted historical documentation."
                    )
                else:
                    status = "MISSING"
                    supporting_ids = []
                    rationale = f"No verified technical evidence found to satisfy mandatory criterion {criterion.id}."

                mappings.append(
                    CriteriaMapping(
                        criterion_id=criterion.id,
                        trl_level=lvl,
                        criterion_description=criterion.description,
                        status=status,
                        supporting_evidence_ids=supporting_ids,
                        inferred_from_trl=inferred_from,
                        rationale=rationale,
                    )
                )

        return mappings
