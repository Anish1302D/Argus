"""
Official Technology Readiness Level (TRL 1-9) Framework Definitions.
Represents the official assessment ladder, criteria checklist, and validation environments.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TRLCriterion(BaseModel):
    id: str = Field(..., description="Unique criterion code, e.g. TRL-1.1")
    description: str = Field(..., description="Specific objective validation requirement")
    is_mandatory: bool = Field(True, description="Whether this criterion is mandatory for the level")


class TRLDefinition(BaseModel):
    level: int = Field(..., ge=1, le=9, description="TRL numeric level (1-9)")
    title: str = Field(..., description="Standard title of the level")
    summary: str = Field(..., description="High-level definition")
    required_environment: str = Field(..., description="Operating or testing environment required")
    criteria: List[TRLCriterion] = Field(..., description="Checklist of criteria that must be satisfied")
    typical_evidence: List[str] = Field(..., description="Types of documents or evidence proving readiness")


TRL_LADDER: Dict[int, TRLDefinition] = {
    1: TRLDefinition(
        level=1,
        title="Basic principles observed",
        summary="Scientific research begins to be translated into applied R&D. Paper studies of basic principles.",
        required_environment="None (Theoretical / Paper)",
        criteria=[
            TRLCriterion(id="TRL-1.1", description="Basic scientific principles observed and reported.", is_mandatory=True),
            TRLCriterion(id="TRL-1.2", description="Mathematical or theoretical formulations published or documented.", is_mandatory=True),
        ],
        typical_evidence=[
            "Peer-reviewed scientific publications",
            "Theoretical research papers",
            "Initial patent filings on basic mechanisms"
        ]
    ),
    2: TRLDefinition(
        level=2,
        title="Technology concept formulated",
        summary="Invention begins. Practical applications can be applied to the basic principles observed.",
        required_environment="None (Analytical / Conceptual)",
        criteria=[
            TRLCriterion(id="TRL-2.1", description="Practical application of basic principles is identified.", is_mandatory=True),
            TRLCriterion(id="TRL-2.2", description="Analytical formulation of concept or application documented.", is_mandatory=True),
            TRLCriterion(id="TRL-2.3", description="No experimental proof or prototype exists yet.", is_mandatory=False),
        ],
        typical_evidence=[
            "System architecture whitepapers",
            "Analytical concept reports",
            "Patent applications describing technical utility"
        ]
    ),
    3: TRLDefinition(
        level=3,
        title="Experimental proof of concept",
        summary="Active R&D initiated. Analytical studies and laboratory studies to physically validate predictions.",
        required_environment="Laboratory bench / Synthetic setup",
        criteria=[
            TRLCriterion(id="TRL-3.1", description="Laboratory-based experimental proof of concept demonstrated.", is_mandatory=True),
            TRLCriterion(id="TRL-3.2", description="Components tested individually on bench-scale setups.", is_mandatory=True),
            TRLCriterion(id="TRL-3.3", description="Measurable experimental metrics validating core scientific assumptions.", is_mandatory=True),
        ],
        typical_evidence=[
            "Bench-scale test reports",
            "Experimental lab data with measurement metrics",
            "Proof-of-concept demonstration results"
        ]
    ),
    4: TRLDefinition(
        level=4,
        title="Technology validated in a laboratory",
        summary="Basic technological components integrated to establish that they will work together in a laboratory.",
        required_environment="Laboratory / Integrated test setup",
        criteria=[
            TRLCriterion(id="TRL-4.1", description="Individual components integrated into a low-fidelity system.", is_mandatory=True),
            TRLCriterion(id="TRL-4.2", description="Integrated system tested in a controlled laboratory environment.", is_mandatory=True),
            TRLCriterion(id="TRL-4.3", description="Basic functional interoperability between components established.", is_mandatory=True),
        ],
        typical_evidence=[
            "Breadboard / bench integrated test logs",
            "Component integration test protocols",
            "Laboratory performance evaluation reports"
        ]
    ),
    5: TRLDefinition(
        level=5,
        title="Technology validated in a relevant environment",
        summary="Reliability of the technology significantly increases. Basic components integrated with realistic supporting elements.",
        required_environment="Relevant environment (simulated operational conditions)",
        criteria=[
            TRLCriterion(id="TRL-5.1", description="High-fidelity laboratory integration or simulated relevant environment testing.", is_mandatory=True),
            TRLCriterion(id="TRL-5.2", description="Testing subjected to realistic external stresses (thermal, pressure, vibration, network, etc.).", is_mandatory=True),
            TRLCriterion(id="TRL-5.3", description="Documented test methodology matching expected operational stressors.", is_mandatory=True),
        ],
        typical_evidence=[
            "Environmental chamber test reports",
            "Simulated operational stress test reports",
            "Relevant-environment validation protocols"
        ]
    ),
    6: TRLDefinition(
        level=6,
        title="Technology demonstrated in a relevant environment",
        summary="Representative model or prototype system tested in a relevant environment. Represents a major step forward.",
        required_environment="Relevant environment (field test / representative platform)",
        criteria=[
            TRLCriterion(id="TRL-6.1", description="Engineering prototype / representative model completed.", is_mandatory=True),
            TRLCriterion(id="TRL-6.2", description="Demonstration of prototype in a relevant operational environment.", is_mandatory=True),
            TRLCriterion(id="TRL-6.3", description="Quantitative engineering performance measured against operational targets.", is_mandatory=True),
        ],
        typical_evidence=[
            "Prototype field trial logs",
            "Engineering model verification reports",
            "Telemetry / measurement reports from relevant environment"
        ]
    ),
    7: TRLDefinition(
        level=7,
        title="System prototype demonstrated in an operational environment",
        summary="Prototype near or at planned operational system. Demonstration of an actual system prototype in an operational environment.",
        required_environment="Operational environment (actual intended user conditions)",
        criteria=[
            TRLCriterion(id="TRL-7.1", description="System prototype at or near full operational scale.", is_mandatory=True),
            TRLCriterion(id="TRL-7.2", description="Demonstration in an actual operational environment (flight, factory floor, real user trial).", is_mandatory=True),
            TRLCriterion(id="TRL-7.3", description="Resolution of major operational interface issues.", is_mandatory=True),
        ],
        typical_evidence=[
            "Flight trial / live field test certificates",
            "Customer pilot deployment reports",
            "Operational demonstration verification sign-off"
        ]
    ),
    8: TRLDefinition(
        level=8,
        title="Actual system completed and qualified through test and demonstration",
        summary="Technology proven to work in its final form and under expected conditions. In most cases, end of true system development.",
        required_environment="Operational environment (fully qualified)",
        criteria=[
            TRLCriterion(id="TRL-8.1", description="Final operational hardware/software completed in commercial/production form.", is_mandatory=True),
            TRLCriterion(id="TRL-8.2", description="System qualified through developmental testing and operational evaluation (DT&E / OT&E).", is_mandatory=True),
            TRLCriterion(id="TRL-8.3", description="Design documentation, operating manuals, and quality certifications completed.", is_mandatory=True),
        ],
        typical_evidence=[
            "Formal qualification test report (QTR)",
            "Certification compliance documents (ISO, FAA, CE, etc.)",
            "Factory acceptance test (FAT) and site acceptance test (SAT) sign-offs"
        ]
    ),
    9: TRLDefinition(
        level=9,
        title="Actual system proven in operational use",
        summary="Actual application of the technology in its final form and under mission conditions, such as operational service.",
        required_environment="Operational use (sustained production / mission deployment)",
        criteria=[
            TRLCriterion(id="TRL-9.1", description="Technology in continuous, sustained operational service or commercial deployment.", is_mandatory=True),
            TRLCriterion(id="TRL-9.2", description="Proven reliability across repeated missions or commercial operations.", is_mandatory=True),
            TRLCriterion(id="TRL-9.3", description="Documented operational maintenance history, uptime metrics, or commercial sales.", is_mandatory=True),
        ],
        typical_evidence=[
            "Operational mission logs / production telemetry",
            "Commercial sales and customer warranty records",
            "Post-deployment maintenance and reliability reports"
        ]
    ),
}


def get_trl_definition(level: int) -> TRLDefinition:
    """Retrieve the official TRL definition for a given level (1-9)."""
    if level not in TRL_LADDER:
        raise ValueError(f"Invalid TRL level: {level}. Level must be an integer between 1 and 9.")
    return TRL_LADDER[level]


def get_all_definitions() -> List[TRLDefinition]:
    """Return all TRL definitions in ascending order (1 to 9)."""
    return [TRL_LADDER[lvl] for lvl in sorted(TRL_LADDER.keys())]

