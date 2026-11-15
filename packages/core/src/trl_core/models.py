"""
Canonical Domain Models for the TRL Debate Engine.
Defines immutable structured representations used across all layers.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EvidenceCategory(str, Enum):
    CONCEPT = "concept"
    SIMULATION = "simulation"
    EXPERIMENT = "experiment"
    PROTOTYPE = "prototype"
    LABORATORY_VALIDATION = "laboratory_validation"
    RELEVANT_ENVIRONMENT_TESTING = "relevant_environment_testing"
    OPERATIONAL_DEMONSTRATION = "operational_demonstration"
    DEPLOYMENT = "deployment"
    INDEPENDENT_VERIFICATION = "independent_verification"


class EvidenceStrength(str, Enum):
    STRONG_SUPPORTING = "strong_supporting"
    MODERATE_SUPPORTING = "moderate_supporting"
    WEAK_SUPPORTING = "weak_supporting"
    CONTRADICTORY = "contradictory"
    MISSING = "missing"
    UNVERIFIED_CLAIM = "unverified_claim"


class ModalityType(str, Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    HYPOTHETICAL = "hypothetical"
    SIMULATED = "simulated"
    NEGATED = "negated"
    UNPERFORMED = "unperformed"


class TemporalStatus(str, Enum):
    PAST_VERIFIED = "past_verified"
    IN_PROGRESS = "in_progress"
    FUTURE_PROPOSED = "future_proposed"


class EvidenceType(str, Enum):
    EMPIRICAL = "empirical"
    THEORETICAL = "theoretical"
    SIMULATION = "simulation"
    SPECIFICATION = "specification"


class ValidationEnvironment(str, Enum):
    MATHEMATICAL_THEORY = "mathematical_theory"
    LABORATORY = "laboratory"
    RELEVANT_ENVIRONMENT = "relevant_environment"
    OPERATIONAL_SPACE_OR_FLIGHT = "operational_space_or_flight"
    UNSPECIFIED = "unspecified"


class QuantitativeMeasurement(BaseModel):
    """Quantitative measurement extracted from technical claims."""
    model_config = ConfigDict(frozen=True)

    metric: str = Field(..., description="Name or description of measured metric, e.g. 'sensitivity'")
    value: float = Field(..., description="Numerical magnitude")
    unit: str = Field(..., description="Engineering or physical unit, e.g. 'ppb', 'GHz', 'MPa'")
    raw_text: str = Field(..., description="Original raw snippet containing the measurement")
    tolerance: Optional[str] = Field(None, description="Tolerance or error bounds if present, e.g. '+/- 0.05'")


class TechnicalClaim(BaseModel):
    """A structured technical claim extracted from a document chunk."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Unique claim identifier, e.g. CLAIM-001")
    document_id: str = Field(..., description="Parent document identifier")
    chunk_id: str = Field(..., description="Source chunk identifier")
    text: str = Field(..., min_length=1, description="Complete claim statement")
    candidate_trl: int = Field(..., ge=1, le=9, description="Candidate TRL level associated with milestone")
    achievement_category: str = Field(..., description="Specific milestone category")
    measurements: List[QuantitativeMeasurement] = Field(default_factory=list, description="Quantitative values")
    validation_environment: ValidationEnvironment = Field(
        default=ValidationEnvironment.UNSPECIFIED,
        description="Assessed validation environment"
    )
    modality: ModalityType = Field(default=ModalityType.COMPLETED, description="Modality of claim")
    temporal_status: TemporalStatus = Field(default=TemporalStatus.PAST_VERIFIED, description="Temporal status")
    evidence_type: EvidenceType = Field(default=EvidenceType.EMPIRICAL, description="Evidence type")
    verbatim_quote: str = Field(..., description="Exact matched substring quote")
    char_offset_start: int = Field(..., ge=0, description="Start offset in document")
    char_offset_end: int = Field(..., ge=0, description="End offset in document")
    section_name: Optional[str] = Field(None, description="Section heading")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Extraction confidence")


class ContradictionItem(BaseModel):
    """Identified contradiction between technical claims in a document."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Contradiction ID, e.g. CONTRA-001")
    claim_id_a: str = Field(..., description="First claim ID (e.g. high-TRL assertion)")
    claim_id_b: str = Field(..., description="Second claim ID (e.g. limitation or negation)")
    explanation: str = Field(..., description="Detailed explanation of the contradiction")
    severity: Literal["HIGH", "MEDIUM", "LOW"] = Field("HIGH", description="Severity impact on TRL")
    resolved_status: Literal["UNRESOLVED", "ACCEPTED_A", "ACCEPTED_B", "DISMISSED_BOTH"] = Field(
        "UNRESOLVED", description="Adjudication resolution state"
    )
    resolution_rationale: Optional[str] = Field(None, description="Referee rationale for resolution")


class UncertaintyProfile(BaseModel):
    """Multi-dimensional uncertainty model separating heuristic confidence from statistical certainty."""
    model_config = ConfigDict(frozen=True)

    extraction_confidence: float = Field(..., ge=0.0, le=1.0, description="Average pattern extraction confidence")
    criteria_coverage: float = Field(..., ge=0.0, le=1.0, description="Ratio of verified criteria for target TRL")
    conflict_penalty: float = Field(..., ge=0.0, le=1.0, description="Uncertainty penalty from unresolved contradictions")
    composite_certainty: float = Field(..., ge=0.0, le=1.0, description="Final composite certainty score [0.0, 1.0]")
    calibration_status: Literal["UNCALIBRATED_HEURISTIC", "CALIBRATED_EMPIRICAL"] = Field(
        "UNCALIBRATED_HEURISTIC",
        description="Explicit disclosure that confidence is heuristic rather than calibrated statistical probability"
    )
    notes: List[str] = Field(default_factory=list, description="Methodological uncertainty notes")


class SourceProvenance(BaseModel):
    """Granular character-level provenance connecting claims to source text."""
    model_config = ConfigDict(frozen=True)

    document_id: str = Field(..., description="Parent document identifier")
    chunk_id: str = Field(..., description="Source chunk identifier")
    page_number: int = Field(..., ge=1, description="Page number (1-indexed)")
    section_name: Optional[str] = Field(None, description="Section or heading title")
    char_offset_start: int = Field(..., ge=0, description="Exact start character offset in raw document")
    char_offset_end: int = Field(..., ge=0, description="Exact end character offset in raw document")
    verbatim_excerpt: str = Field(..., description="Verbatim text slice matching offsets")
    context_window: Optional[str] = Field(None, description="Surrounding contextual text (+/- 150 chars)")


class CriteriaMapping(BaseModel):
    """Mapping between evidence items and formal canonical TRL checklist criteria."""
    model_config = ConfigDict(frozen=True)

    criterion_id: str = Field(..., description="Canonical criterion ID, e.g. TRL-4.1")
    trl_level: int = Field(..., ge=1, le=9, description="Associated TRL level")
    criterion_description: str = Field(..., description="Formal criterion description")
    status: Literal["DIRECTLY_SATISFIED", "PARTIALLY_SUPPORTED", "MISSING", "CONTRADICTORY", "SATISFIED_INFERRED"] = Field(
        ..., description="Adjudicated criteria satisfaction status"
    )
    supporting_evidence_ids: List[str] = Field(default_factory=list, description="IDs of supporting evidence items")
    inferred_from_trl: Optional[int] = Field(None, description="Source TRL level if inferred")
    rationale: str = Field(..., description="Detailed rationale for the mapping determination")


class AdvancementGapReport(BaseModel):
    """Detailed gap analysis and actionable recommendations for advancement to TRL N+1."""
    model_config = ConfigDict(frozen=True)

    current_trl: int = Field(..., ge=1, le=9, description="Currently adjudicated TRL")
    target_next_trl: Optional[int] = Field(None, ge=2, le=9, description="Next target TRL (None if TRL 9)")
    missing_criteria: List[str] = Field(default_factory=list, description="Mandatory criteria missing for N+1")
    required_environment: Optional[str] = Field(None, description="Required testing environment for N+1")
    recommended_activities: List[str] = Field(default_factory=list, description="Specific engineering recommendations")
    blockers: List[str] = Field(default_factory=list, description="Active blockers or contradictions preventing advancement")


class AuditRecord(BaseModel):
    """Immutable audit record of a specific adjudication rule execution."""
    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Identifier of the rule evaluated, e.g. RULE-PREREQ-INFER")
    stage: str = Field(..., description="Adjudication pipeline stage")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Retained input parameters")
    outcome: str = Field(..., description="Rule outcome or decision")
    explanation: str = Field(..., description="Detailed explanation")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Audit record timestamp"
    )


class AuditTrail(BaseModel):
    """Complete immutable audit trail of the assessment adjudication pipeline."""
    model_config = ConfigDict(frozen=True)

    methodology_version: str = Field(default="2.0.0-argus", description="Methodology version")
    records: List[AuditRecord] = Field(default_factory=list, description="Ordered audit log records")
    reproducibility_hash: str = Field(..., description="Deterministic sha256 hash of inputs and decisions")


class AgentType(str, Enum):
    OPTIMIST = "optimist"
    SKEPTIC = "skeptic"
    REFEREE = "referee"


class Chunk(BaseModel):
    """A granular structural chunk of a technical document."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Unique identifier for the chunk, e.g. chunk_p1_0")
    document_id: str = Field(..., description="Parent document identifier")
    text: str = Field(..., min_length=1, description="Sanitized text content")
    page_number: int = Field(..., ge=1, description="Source page number (1-indexed)")
    section_name: Optional[str] = Field(None, description="Heading or section name if identified")
    char_offset_start: int = Field(..., ge=0, description="Start character offset in page/document")
    char_offset_end: int = Field(..., ge=0, description="End character offset")
    is_sanitized: bool = Field(True, description="Indicates whether prompt injection defense was applied")


class Document(BaseModel):
    """An ingested technical document."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Unique document ID (hash or UUID)")
    name: str = Field(..., description="Original filename or document title")
    raw_content: str = Field(..., description="Full extracted text")
    chunks: List[Chunk] = Field(default_factory=list, description="Extracted structural chunks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata such as page count, format, extraction tool")


class EvidenceItem(BaseModel):
    """A verified or candidate technical claim extracted from a document."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Unique evidence ID, e.g. EVID-001")
    document_id: str = Field(..., description="Source document identifier")
    evidence_text: str = Field(..., min_length=1, description="Verbatim or summarized evidence statement")
    page_number: int = Field(..., ge=1, description="Page where evidence appears")
    section_name: Optional[str] = Field(None, description="Section where evidence appears")
    category: EvidenceCategory = Field(..., description="Primary evidence category")
    strength: EvidenceStrength = Field(..., description="Assessed evidence strength")
    target_trl: Optional[int] = Field(None, ge=1, le=9, description="Associated TRL level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence score [0.0, 1.0]")
    source_reference: Dict[str, Any] = Field(
        default_factory=dict,
        description="Traceability details (char offsets, chunk_id, bounding boxes)"
    )
    claim_id: Optional[str] = Field(None, description="Associated technical claim ID")
    modality: ModalityType = Field(default=ModalityType.COMPLETED, description="Claim modality")
    temporal_status: TemporalStatus = Field(default=TemporalStatus.PAST_VERIFIED, description="Temporal status")
    evidence_type: EvidenceType = Field(default=EvidenceType.EMPIRICAL, description="Type of evidence")
    validation_environment: ValidationEnvironment = Field(
        default=ValidationEnvironment.UNSPECIFIED,
        description="Validation environment"
    )
    measurements: List[QuantitativeMeasurement] = Field(
        default_factory=list,
        description="Quantitative measurements extracted for this evidence"
    )


class AgentAssessment(BaseModel):
    """The position taken by an individual agent (Optimist, Skeptic, or Referee)."""
    model_config = ConfigDict(frozen=True)

    agent_type: AgentType = Field(..., description="Role of the agent")
    initial_trl: int = Field(..., ge=1, le=9, description="Initial independent TRL assessment")
    final_trl: int = Field(..., ge=1, le=9, description="Final TRL stance after debate")
    reasoning: str = Field(..., min_length=1, description="Detailed technical reasoning")
    evidence_references: List[str] = Field(
        default_factory=list,
        description="List of verified evidence IDs (EVID-xxx) supporting the stance"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent confidence score")


class DebateMessage(BaseModel):
    """A single structured turn in the adversarial debate protocol."""
    model_config = ConfigDict(frozen=True)

    round_number: int = Field(..., ge=1, le=4, description="Debate round (1 to 4)")
    agent_type: AgentType = Field(..., description="Author agent (optimist or skeptic)")
    argument: str = Field(..., min_length=1, description="Technical argument or counterargument")
    evidence_references: List[str] = Field(
        default_factory=list,
        description="Evidence IDs cited in this specific turn"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of the turn"
    )

    @field_validator("agent_type")
    @classmethod
    def validate_debate_author(cls, v: AgentType) -> AgentType:
        if v not in (AgentType.OPTIMIST, AgentType.SKEPTIC):
            raise ValueError("Debate messages may only be authored by optimist or skeptic")
        return v


class ImpliedPrerequisiteAudit(BaseModel):
    """Audit record for a lower-level TRL criterion inferred from verified higher-level evidence."""
    model_config = ConfigDict(frozen=True)

    criterion_id: str = Field(..., description="ID of the inferred prerequisite, e.g. TRL-3.1")
    target_level: int = Field(..., ge=1, le=8, description="The lower level that was inferred")
    status: Literal["SATISFIED_INFERRED"] = Field(
        "SATISFIED_INFERRED",
        description="Status marking this criterion as inferred rather than explicitly documented"
    )
    inferred_from_trl: int = Field(..., ge=2, le=9, description="The higher TRL with verified strong evidence")
    anchoring_evidence_id: str = Field(..., description="The verified evidence ID anchoring the inference")
    inference_rationale: str = Field(..., min_length=1, description="Audit justification explaining the inference")
    auditable: bool = Field(True, description="Flag confirming this record is exposed in audit reports")

    @field_validator("inferred_from_trl")
    @classmethod
    def validate_hierarchy(cls, v: int, info) -> int:
        target = info.data.get("target_level")
        if target is not None and v <= target:
            raise ValueError(f"Inferred source level ({v}) must be strictly higher than target level ({target})")
        return v


class FinalAssessment(BaseModel):
    """The canonical adjudication produced by the Referee and Engine."""
    model_config = ConfigDict(frozen=True)

    predicted_trl: int = Field(..., ge=1, le=9, description="Final adjudicated TRL between 1 and 9")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated confidence [0.0, 1.0]")
    justification: str = Field(..., min_length=1, description="Defensible technical explanation")
    satisfied_criteria: List[str] = Field(
        default_factory=list,
        description="List of criterion descriptions satisfied with explicit evidence"
    )
    implied_prerequisites_audit: List[ImpliedPrerequisiteAudit] = Field(
        default_factory=list,
        description="Audit ledger of implied lower-level prerequisites"
    )
    missing_criteria: List[str] = Field(
        default_factory=list,
        description="Identified validation gaps preventing advancement to the next TRL"
    )
    contradictions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Identified conflicting claims within the document"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable engineering recommendations to reach the next readiness level"
    )
    supporting_evidence: List[EvidenceItem] = Field(
        default_factory=list,
        description="Traceable evidence items upholding the final decision"
    )
    agent_assessments: Dict[str, AgentAssessment] = Field(
        default_factory=dict,
        description="Summary positions of all participating agents"
    )
    debate_transcript: List[DebateMessage] = Field(
        default_factory=list,
        description="Auditable message history of the adversarial debate"
    )
    evidence_ledger: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Structured relational evidence ledger"
    )
    criteria_mappings: List[CriteriaMapping] = Field(
        default_factory=list,
        description="Detailed criteria mappings for audited levels"
    )
    uncertainty_profile: Optional[UncertaintyProfile] = Field(
        default=None,
        description="Multi-dimensional uncertainty profile"
    )
    audit_trail: Optional[AuditTrail] = Field(
        default=None,
        description="Comprehensive assessment audit trail"
    )
    gap_report: Optional[AdvancementGapReport] = Field(
        default=None,
        description="Advancement gap report for progression to TRL N+1"
    )
    methodology_version: str = Field(
        default="2.0.0-argus",
        description="Argus adjudication methodology version"
    )

