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

