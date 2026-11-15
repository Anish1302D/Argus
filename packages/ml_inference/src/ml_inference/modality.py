"""
Modality, Negation and Temporal Understanding Engine.
Classifies linguistic modality and temporal status of technical claims and milestones.
Distinguishes completed, unperformed, planned, proposed, hypothetical, simulated,
and independently verified achievements with calibrated linguistic qualifiers.
"""

import re
from typing import Tuple

from trl_core.models import ModalityType, TemporalStatus

# Future / Planned linguistic markers
_PLANNED_PATTERNS = re.compile(
    r"(?i)\b("
    r"future\s+work\s+(?:will|shall|aims?\s+to|plans?\s+to)"
    r"|planned\s+(?:for|to|in)"
    r"|scheduled\s+(?:for|to)"
    r"|will\s+(?:focus\s+on|be\s+conducted|be\s+tested|be\s+flown|be\s+integrated|be\s+developed|be\s+evaluated)"
    r"|shall\s+be"
    r"|is\s+planned"
    r"|proposed\s+(?:architecture|system|approach|design)"
    r"|under\s+active\s+development"
    r"|roadmap"
    r"|milestone\s+for\s+Q[1-4]"
    r"|to\s+be\s+demonstrated"
    r")\b"
)

# Hypothetical / Speculative markers
_HYPOTHETICAL_PATTERNS = re.compile(
    r"(?i)\b("
    r"could\s+(?:\w+\s+)?(?:achieve|enable|provide|reach)"
    r"|might\s+(?:\w+\s+)?(?:allow|demonstrate|show)"
    r"|theoretically\s+(?:possible|viable|capable|achieve)?"
    r"|would\s+(?:potentially|theoretically)"
    r"|hypothesized\s+that"
    r"|speculative"
    r"|anticipated\s+performance"
    r")\b"
)

# Simulation-only markers
_SIMULATION_PATTERNS = re.compile(
    r"(?i)\b("
    r"numerical\s+simulation"
    r"|finite\s+element\s+model(?:ing)?"
    r"|simulated\s+results?"
    r"|computational\s+fluid\s+dynamics"
    r"|cfd\s+analysis"
    r"|monte\s+carlo"
    r"|in\s+silico"
    r"|ansys\b|matlab\s+simulink"
    r")\b"
)

# Explicit Negation / Unperformed markers
_NEGATION_PATTERNS = re.compile(
    r"(?i)\b("
    r"not\s+yet\s+(?:undergone|demonstrated|tested|validated|flown|achieved|conducted|built)"
    r"|has\s+not\s+(?:undergone|demonstrated|been\s+tested|been\s+validated)"
    r"|have\s+not\s+been"
    r"|is\s+not\s+(?:ruggedized|tested|validated|qualified)"
    r"|are\s+not\s+yet"
    r"|no\s+(?:laboratory\s+experiment|breadboard|prototype|flight|test)\s+has\s+been"
    r"|neither\s+tested\s+nor"
    r"|without\s+(?:actual|suborbital|orbital|flight)\s+demonstration"
    r"|failed\s+to\s+(?:meet|demonstrate|replicate)"
    r"|unperformed"
    r"|untested"
    r"|absence\s+of\s+(?:flight|empirical|test)\s+data"
    r")\b"
)

# In-Progress markers
_IN_PROGRESS_PATTERNS = re.compile(
    r"(?i)\b("
    r"currently\s+(?:undergoing|in\s+progress|being\s+tested|under\s+evaluation)"
    r"|ongoing\s+(?:trials?|campaign|tests?)"
    r"|preliminary\s+testing\s+is\s+underway"
    r")\b"
)


class ModalityAnalyzer:
    """
    Calibrated linguistic analyzer distinguishing completed achievements
    from planned, hypothetical, simulated, or negated statements.
    """

    def analyze_claim_modality(self, sentence: str, matched_keyword: str) -> Tuple[ModalityType, TemporalStatus]:
        """
        Classify the modality and temporal status of a technical statement.
        Returns (ModalityType, TemporalStatus).
        """
        text = sentence.strip()

        # 1. Check for explicit negation / unperformed status first
        if _NEGATION_PATTERNS.search(text):
            return ModalityType.NEGATED, TemporalStatus.PAST_VERIFIED

        # Check local sentence negation surrounding the keyword
        kw_idx = text.lower().find(matched_keyword.lower())
        if kw_idx != -1:
            left_window = text[max(0, kw_idx - 60):kw_idx]
            right_window = text[kw_idx + len(matched_keyword):min(len(text), kw_idx + len(matched_keyword) + 60)]

            if re.search(r"(?i)\b(no|not|never|without|unperformed|absence\s+of|lack\s+of)\b", left_window):
                return ModalityType.NEGATED, TemporalStatus.PAST_VERIFIED
            if re.search(r"(?i)\b(not\s+yet|has\s+not\s+been|was\s+not)\b", right_window):
                return ModalityType.NEGATED, TemporalStatus.PAST_VERIFIED

        # 2. Check for planned / future milestone
        if _PLANNED_PATTERNS.search(text):
            return ModalityType.PLANNED, TemporalStatus.FUTURE_PROPOSED

        # 3. Check for hypothetical / speculative claims
        if _HYPOTHETICAL_PATTERNS.search(text):
            return ModalityType.HYPOTHETICAL, TemporalStatus.FUTURE_PROPOSED

        # 4. Check for in-progress activities
        if _IN_PROGRESS_PATTERNS.search(text):
            return ModalityType.COMPLETED, TemporalStatus.IN_PROGRESS

        # 5. Check for pure simulation
        if _SIMULATION_PATTERNS.search(text) and not re.search(r"(?i)\b(hardware|flight|experimental\s+data|measured|telemetry)\b", text):
            return ModalityType.SIMULATED, TemporalStatus.PAST_VERIFIED

        # Default: Verified completed milestone
        return ModalityType.COMPLETED, TemporalStatus.PAST_VERIFIED

    def is_claim_satisfiable(self, claim_modality: ModalityType, claim_temporal: TemporalStatus) -> bool:
        """
        Adjudication rule: A claim can ONLY satisfy a required TRL criterion
        if it is COMPLETED and NOT planned, hypothetical, or negated.
        """
        if claim_modality in (ModalityType.NEGATED, ModalityType.PLANNED, ModalityType.HYPOTHETICAL, ModalityType.UNPERFORMED):
            return False
        if claim_temporal == TemporalStatus.FUTURE_PROPOSED:
            return False
        return True
