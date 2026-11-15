"""
Structured Technical Claim Extractor.
Extracts structured technical claims, quantitative measurements, engineering milestones,
and testing environments from document chunks while preserving exact character offsets.
"""

import re
from typing import Dict, List, Optional, Tuple

from trl_core.models import (
    Chunk,
    Document,
    EvidenceCategory,
    EvidenceType,
    ModalityType,
    QuantitativeMeasurement,
    TechnicalClaim,
    TemporalStatus,
    ValidationEnvironment,
)
from trl_core.trl_definitions import TRL_LADDER

# Regex for extracting scientific and engineering measurements
# Matches numbers with scientific units, percentages, tolerances, and error bars
_MEASUREMENT_PATTERN = re.compile(
    r"(?P<metric_context>[a-zA-Z\s]{0,25})?"
    r"(?P<value>[+-]?\d+(?:,\d{3})*(?:\.\d+)?)\s*"
    r"(?P<tolerance>(?:±|\+/-)\s*\d+(?:\.\d+)?)?\s*"
    r"(?P<unit>%"
    r"|ppb|ppm|ppt"
    r"|ghz|mhz|khz|hz"
    r"|nm|um|µm|mm|cm|m|km"
    r"|db|dbm|dbi"
    r"|k|c|f"
    r"|mpa|gpa|kpa|pa|bar|mbar|psi|torr"
    r"|mj/kg|kj/kg|j/kg|w/cm2|kw/m2|w/m2"
    r"|mw|kw|w|gw"
    r"|v|mv|kv|ma|a"
    r"|hours?|hrs?|minutes?|mins?|seconds?|sec|days?|months?|years?"
    r"|kg|g|mg|ug|µg|tons?"
    r"|mm/min|m/s|km/s|mach\s*\d+"
    r"|passes?|units?|runs?|cycles?|seus?)\b",
    re.IGNORECASE,
)

# Common unit normalization
UNIT_NORMALIZATIONS = {
    "hrs": "hours",
    "hr": "hours",
    "mins": "minutes",
    "min": "minutes",
    "sec": "seconds",
    "cycles": "cycles",
}

# Environmental indicator patterns
_ENV_PATTERNS = [
    (ValidationEnvironment.OPERATIONAL_SPACE_OR_FLIGHT, re.compile(r"(?i)\b(in-orbit|flight\s+operation|mission\s+operation|sun-synchronous\s+orbit|leo\b|flight\s+demonstration|operational\s+service|flight-qualified)\b")),
    (ValidationEnvironment.RELEVANT_ENVIRONMENT, re.compile(r"(?i)\b(arc-jet|thermal\s+vacuum|t-vac|environmental\s+chamber|mach\s+\d+|re-entry\s+aerothermal|relevant\s+environment|suborbital|field\s+test)\b")),
    (ValidationEnvironment.LABORATORY, re.compile(r"(?i)\b(laboratory|breadboard|bench-scale|benchtop|ambient\s+room\s+temperature|optical\s+breadboard|controlled\s+laboratory)\b")),
    (ValidationEnvironment.MATHEMATICAL_THEORY, re.compile(r"(?i)\b(theoretical|mathematical\s+formulation|numerical\s+simulation|analytical\s+model|casimir\s+vacuum|literature\s+review)\b")),
]


class StructuredClaimExtractor:
    """
    Extracts structured technical claims beyond naive keyword matching.
    Captures metrics, engineering milestones, achievements, validation environments,
    and candidate TRL levels with source context.
    """

    def __init__(self):
        # Import milestone patterns
        from ml_inference.features import TRL_PATTERNS
        self.patterns = TRL_PATTERNS

    def extract_measurements(self, text: str) -> List[QuantitativeMeasurement]:
        """Extract quantitative measurements with units, numerical values, and tolerances."""
        measurements: List[QuantitativeMeasurement] = []
        for match in _MEASUREMENT_PATTERN.finditer(text):
            val_str = match.group("value").replace(",", "")
            try:
                val = float(val_str)
            except ValueError:
                continue

            unit = match.group("unit").strip().lower()
            unit = UNIT_NORMALIZATIONS.get(unit, unit)
            raw_text = match.group(0).strip()
            tol = match.group("tolerance")
            tolerance = tol.strip() if tol else None
            ctx = match.group("metric_context")
            metric = ctx.strip().capitalize() if ctx and len(ctx.strip()) > 2 else "Parameter Measurement"

            measurements.append(
                QuantitativeMeasurement(
                    metric=metric,
                    value=val,
                    unit=unit,
                    raw_text=raw_text,
                    tolerance=tolerance,
                )
            )
        return measurements

    def infer_environment(self, text: str) -> ValidationEnvironment:
        """Infer the validation environment from contextual phrases."""
        for env, pat in _ENV_PATTERNS:
            if pat.search(text):
                return env
        return ValidationEnvironment.UNSPECIFIED

    def extract_claims_from_chunk(self, chunk: Chunk) -> List[TechnicalClaim]:
        """Decompose a single document chunk into structured technical claims."""
        from ml_inference.modality import ModalityAnalyzer

        claims: List[TechnicalClaim] = []
        modality_analyzer = ModalityAnalyzer()
        text = chunk.text
        claim_counter = 1

        # Break chunk into candidate sentence clauses
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 15]
        if not sentences:
            sentences = [text.strip()]

        for sentence in sentences:
            sentence_measurements = self.extract_measurements(sentence)
            env = self.infer_environment(sentence)

            # Check candidate TRL milestone patterns
            for trl_lvl in range(9, 0, -1):
                patterns = self.patterns.get(trl_lvl, [])
                matched_pat = None
                matched_str = ""
                span_in_sentence = (0, 0)

                for pat in patterns:
                    m = re.search(pat, sentence)
                    if m:
                        matched_pat = pat
                        matched_str = m.group(0)
                        span_in_sentence = m.span()
                        break

                if matched_pat:
                    # Analyze modality & temporal status
                    modality, temporal = modality_analyzer.analyze_claim_modality(sentence, matched_str)

                    # Compute character offsets relative to document
                    sent_offset_in_chunk = text.find(sentence)
                    if sent_offset_in_chunk == -1:
                        sent_offset_in_chunk = 0
                    char_start = chunk.char_offset_start + sent_offset_in_chunk
                    char_end = char_start + len(sentence)

                    # Category determination
                    category_title = TRL_LADDER.get(trl_lvl).title if trl_lvl in TRL_LADDER else f"TRL {trl_lvl}"

                    # Evidence type inference
                    if env == ValidationEnvironment.MATHEMATICAL_THEORY:
                        ev_type = EvidenceType.THEORETICAL
                    elif modality == ModalityType.SIMULATED or "simulation" in sentence.lower():
                        ev_type = EvidenceType.SIMULATION
                    elif sentence_measurements or env in (ValidationEnvironment.LABORATORY, ValidationEnvironment.RELEVANT_ENVIRONMENT, ValidationEnvironment.OPERATIONAL_SPACE_OR_FLIGHT):
                        ev_type = EvidenceType.EMPIRICAL
                    else:
                        ev_type = EvidenceType.SPECIFICATION

                    claim = TechnicalClaim(
                        id=f"CLAIM-{chunk.document_id[:4]}-{chunk.id[-4:]}-{claim_counter:02d}",
                        document_id=chunk.document_id,
                        chunk_id=chunk.id,
                        text=sentence,
                        candidate_trl=trl_lvl,
                        achievement_category=category_title,
                        measurements=sentence_measurements,
                        validation_environment=env,
                        modality=modality,
                        temporal_status=temporal,
                        evidence_type=ev_type,
                        verbatim_quote=matched_str,
                        char_offset_start=char_start,
                        char_offset_end=char_end,
                        section_name=chunk.section_name,
                        confidence=0.90 if sentence_measurements and modality == ModalityType.COMPLETED else 0.75,
                    )
                    claims.append(claim)
                    claim_counter += 1
                    break  # Keep the highest candidate TRL for this specific sentence

        return claims

    def extract_document_claims(self, document: Document) -> List[TechnicalClaim]:
        """Extract structured technical claims across all document chunks."""
        all_claims: List[TechnicalClaim] = []
        for chunk in document.chunks:
            all_claims.extend(self.extract_claims_from_chunk(chunk))
        return all_claims
