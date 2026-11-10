"""
TRL Debate Engine Core Package
Provides canonical data models, official TRL definitions, and sanitization utilities.
"""

from .models import (
    Document,
    Chunk,
    EvidenceCategory,
    EvidenceStrength,
    EvidenceItem,
    AgentType,
    AgentAssessment,
    DebateMessage,
    ImpliedPrerequisiteAudit,
    FinalAssessment,
)
from .trl_definitions import TRL_LADDER, TRLDefinition, get_trl_definition

__all__ = [
    "Document",
    "Chunk",
    "EvidenceCategory",
    "EvidenceStrength",
    "EvidenceItem",
    "AgentType",
    "AgentAssessment",
    "DebateMessage",
    "ImpliedPrerequisiteAudit",
    "FinalAssessment",
    "TRL_LADDER",
    "TRLDefinition",
    "get_trl_definition",
]

