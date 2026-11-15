"""
Advancement Gap Analysis Engine.
Analyzes missing criteria between current adjudicated TRL and target level N+1.
Generates concrete, actionable engineering recommendations, required environments,
and identifies active blockers preventing advancement.
"""

from typing import List, Optional
from trl_core.models import (
    AdvancementGapReport,
    ContradictionItem,
    CriteriaMapping,
    EvidenceItem,
)
from trl_core.trl_definitions import TRL_LADDER, get_trl_definition


class AdvancementGapAnalyzer:
    """
    Identifies specific engineering requirements and missing milestones
    needed to progress from TRL N to TRL N+1.
    """

    def analyze_gap(
        self,
        current_trl: int,
        criteria_mappings: List[CriteriaMapping],
        contradictions: Optional[List[ContradictionItem]] = None,
    ) -> AdvancementGapReport:
        """
        Generate structured gap report for current_trl -> current_trl + 1.
        """
        contradictions = contradictions or []

        if current_trl >= 9:
            return AdvancementGapReport(
                current_trl=9,
                target_next_trl=None,
                missing_criteria=[],
                required_environment="Operational Flight / Space Missions",
                recommended_activities=[
                    "System has achieved highest readiness level (TRL 9).",
                    "Maintain continuous mission operational logs and telemetry verification.",
                    "Sustain configuration control across flight deployments and depot maintenance.",
                ],
                blockers=[],
            )

        next_trl = current_trl + 1
        next_def = get_trl_definition(next_trl)

        # Extract criteria for next TRL that are missing or only partially supported
        next_mappings = [m for m in criteria_mappings if m.trl_level == next_trl]
        missing_crit_descs = [
            m.criterion_description for m in next_mappings
            if m.status in ("MISSING", "PARTIALLY_SUPPORTED", "CONTRADICTORY")
        ]
        if not missing_crit_descs:
            missing_crit_descs = [c.description for c in next_def.criteria]

        # Extract active blockers (unresolved contradictions or negated attempts)
        blockers = []
        for c in contradictions:
            if c.resolved_status == "UNRESOLVED":
                blockers.append(f"Unresolved document tension: {c.explanation}")

        # Formulate specific actionable engineering recommendations based on NASA/APCTT standards
        recommended_activities = []
        if next_trl == 2:
            recommended_activities.extend([
                "Formulate practical application concepts transitioning from paper principles.",
                "Document mathematical simulation architecture and design utility models.",
            ])
        elif next_trl == 3:
            recommended_activities.extend([
                "Execute bench-scale laboratory experiments to establish analytical predictions physically.",
                "Measure key performance parameters under controlled baseline conditions.",
            ])
        elif next_trl == 4:
            recommended_activities.extend([
                "Integrate individual laboratory components onto a low-fidelity breadboard.",
                "Perform continuous multi-hour interoperability testing in a controlled laboratory setting.",
            ])
        elif next_trl == 5:
            recommended_activities.extend([
                "Transition breadboard hardware into a high-fidelity integrated component enclosure.",
                "Conduct simulated environmental stress tests (thermal vacuum, arc-jet, vibration, or temperature chamber).",
            ])
        elif next_trl == 6:
            recommended_activities.extend([
                "Fabricate full-scale engineering prototype model.",
                "Execute field testing or representative platform validation under simulated operational aerothermal/acoustic loads.",
            ])
        elif next_trl == 7:
            recommended_activities.extend([
                "Conduct actual suborbital, sounding rocket, or flight test demonstration in an operational environment.",
                "Obtain customer pilot operational flight telemetry.",
            ])
        elif next_trl == 8:
            recommended_activities.extend([
                "Complete full developmental qualification testing per aerospace/military standards (e.g., MIL-STD, NASA-STD).",
                "Execute final factory acceptance and site acceptance testing on commercial hardware.",
            ])
        elif next_trl == 9:
            recommended_activities.extend([
                "Demonstrate flight heritage through repeated operational mission cycles under real space/flight conditions.",
                "Verify sustained mission operational link availability and zero-degradation telemetry over extended deployment.",
            ])

        return AdvancementGapReport(
            current_trl=current_trl,
            target_next_trl=next_trl,
            missing_criteria=missing_crit_descs,
            required_environment=next_def.required_environment,
            recommended_activities=recommended_activities,
            blockers=blockers,
        )
