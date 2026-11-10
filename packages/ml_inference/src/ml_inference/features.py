"""
Feature Extraction & Evidence Mining Engine.
Extracts tabular, keyword, structural, and semantic features grounded in official TRL 1-9 criteria.
"""

import re
from typing import Any, Dict, List, Tuple
import numpy as np

from trl_core.models import (
    Chunk,
    Document,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
)
from trl_core.trl_definitions import TRL_LADDER, get_all_definitions


# Regex patterns matching TRL 1-9 technical milestones
TRL_PATTERNS = {
    1: [
        r"(?i)\bbasic\s+principles?\b",
        r"(?i)\bscientific\s+(principles?|observations?|laws?)\b",
        r"(?i)\btheoretical\s+(formulations?|foundations?|study)\b",
        r"(?i)\bliterature\s+review\b",
        r"(?i)\bpeer-reviewed\s+literature\b",
    ],
    2: [
        r"(?i)\btechnology\s+concept\b",
        r"(?i)\bpractical\s+applications?\b",
        r"(?i)\banalytical\s+(formulation|model(ing)?)\b",
        r"(?i)\bconceptual\s+design\b",
        r"(?i)\binvention\s+disclosure\b",
    ],
    3: [
        r"(?i)\bproof\s+of\s+concept\b",
        r"(?i)\bexperimental\s+(proof|demonstration|results?)\b",
        r"(?i)\bbench-scale\b",
        r"(?i)\blaboratory\s+experiment\b",
        r"(?i)\bmeasured\s+parameter\b",
    ],
    4: [
        r"(?i)\blaboratory\s+validation\b",
        r"(?i)\bvalidated\s+in\s+(a\s+)?laboratory\b",
        r"(?i)\bbreadboard\b",
        r"(?i)\bcomponent\s+integration\b",
        r"(?i)\blow-fidelity\s+system\b",
    ],
    5: [
        r"(?i)\brelevant\s+environment\b",
        r"(?i)\bvalidated\s+in\s+(a\s+)?relevant\s+environment\b",
        r"(?i)\benvironmental\s+(chamber|stress)\b",
        r"(?i)\bsimulated\s+operational\s+conditions\b",
        r"(?i)\bthermal\s+vacuum\b",
    ],
    6: [
        r"(?i)\bdemonstrated\s+in\s+(a\s+)?relevant\s+environment\b",
        r"(?i)\bengineering\s+(model|prototype)\b",
        r"(?i)\bfield\s+test(ing)?\b",
        r"(?i)\brelevant\s+flight\b",
        r"(?i)\brepresentative\s+platform\b",
    ],
    7: [
        r"(?i)\boperational\s+environment\b",
        r"(?i)\bsystem\s+prototype\b",
        r"(?i)\bdemonstrated\s+in\s+an\s+operational\s+environment\b",
        r"(?i)\bflight\s+demonstration\b",
        r"(?i)\bcustomer\s+pilot\b",
    ],
    8: [
        r"(?i)\bcompleted\s+and\s+qualified\b",
        r"(?i)\bdevelopmental\s+testing\b",
        r"(?i)\bqualification\s+testing\b",
        r"(?i)\bfactory\s+acceptance\b",
        r"(?i)\bsite\s+acceptance\b",
        r"(?i)\bcommercial\s+hardware\b",
    ],
    9: [
        r"(?i)\bproven\s+in\s+operational\s+use\b",
        r"(?i)\boperational\s+service\b",
        r"(?i)\bcommercial\s+(deployment|sales)\b",
        r"(?i)\bmission\s+operations\b",
        r"(?i)\brepeated\s+missions\b",
        r"(?i)\bproduction\s+telemetry\b",
    ],
}


class FeatureExtractor:
    """Extracts verifiable evidence items and tabular ML feature vectors from Documents."""

    def extract_evidence(self, document: Document) -> List[EvidenceItem]:
        """Mine granular evidence items matching TRL criteria across document chunks."""
        evidence_items: List[EvidenceItem] = []
        evid_counter = 1

        for chunk in document.chunks:
            text = chunk.text
            # Scan each TRL pattern
            for trl_level, patterns in TRL_PATTERNS.items():
                for pat in patterns:
                    match = re.search(pat, text)
                    if match:
                        # Determine category based on TRL level
                        cat = self._get_category_for_trl(trl_level)
                        # Assess evidence strength based on specificity
                        strength = self._evaluate_strength(text, match.group(0))
                        
                        item = EvidenceItem(
                            id=f"EVID-{document.id[:4]}-{evid_counter:03d}",
                            document_id=document.id,
                            evidence_text=text[:300].strip(),
                            page_number=chunk.page_number,
                            section_name=chunk.section_name,
                            category=cat,
                            strength=strength,
                            target_trl=trl_level,
                            confidence=0.85 if strength == EvidenceStrength.STRONG_SUPPORTING else 0.70,
                            source_reference={
                                "chunk_id": chunk.id,
                                "match_term": match.group(0),
                                "char_start": chunk.char_offset_start + match.start(),
                                "char_end": chunk.char_offset_start + match.end(),
                            }
                        )
                        evidence_items.append(item)
                        evid_counter += 1
                        break  # Match only one pattern per chunk per TRL level

        return evidence_items

    def extract_features(self, document: Document, evidence_items: List[EvidenceItem]) -> Tuple[np.ndarray, List[str]]:
        """
        Construct a dense tabular feature vector for the document:
        - Pattern match frequency per TRL (9 features)
        - Highest pattern level detected (1 feature)
        - Evidence category frequencies (9 features)
        - Evidence strength counts (strong, moderate, weak - 3 features)
        - Document structural properties (total words, chunk count, avg chunk length - 3 features)
        Total: 25 structured features.
        """
        text_full = document.raw_content

        # 1. Pattern frequencies per TRL level (1-9)
        trl_counts = []
        for lvl in range(1, 10):
            cnt = sum(len(re.findall(pat, text_full)) for pat in TRL_PATTERNS[lvl])
            trl_counts.append(float(cnt))

        # Highest pattern level with at least 1 match
        highest_matched_lvl = 1.0
        for lvl in range(9, 0, -1):
            if trl_counts[lvl - 1] > 0:
                highest_matched_lvl = float(lvl)
                break

        # 2. Evidence category distribution
        cat_counts = {c: 0.0 for c in EvidenceCategory}
        for ev in evidence_items:
            cat_counts[ev.category] += 1.0
        cat_features = [cat_counts[c] for c in EvidenceCategory]

        # 3. Evidence strength counts
        str_counts = [
            float(sum(1 for e in evidence_items if e.strength == EvidenceStrength.STRONG_SUPPORTING)),
            float(sum(1 for e in evidence_items if e.strength == EvidenceStrength.MODERATE_SUPPORTING)),
            float(sum(1 for e in evidence_items if e.strength == EvidenceStrength.WEAK_SUPPORTING)),
        ]

        # 4. Structural features
        word_count = float(len(text_full.split()))
        chunk_count = float(len(document.chunks))
        avg_chunk_len = word_count / max(1.0, chunk_count)

        feature_values = (
            trl_counts +
            [highest_matched_lvl] +
            cat_features +
            str_counts +
            [word_count, chunk_count, avg_chunk_len]
        )

        feature_names = (
            [f"trl_{i}_keyword_freq" for i in range(1, 10)] +
            ["highest_matched_trl"] +
            [f"cat_{c.value}_freq" for c in EvidenceCategory] +
            ["count_strong_evidence", "count_moderate_evidence", "count_weak_evidence"] +
            ["total_words", "total_chunks", "avg_chunk_length"]
        )

        return np.array(feature_values, dtype=np.float32), feature_names

    def _get_category_for_trl(self, trl: int) -> EvidenceCategory:
        if trl == 1:
            return EvidenceCategory.CONCEPT
        elif trl == 2:
            return EvidenceCategory.SIMULATION
        elif trl == 3:
            return EvidenceCategory.EXPERIMENT
        elif trl == 4:
            return EvidenceCategory.LABORATORY_VALIDATION
        elif trl == 5:
            return EvidenceCategory.RELEVANT_ENVIRONMENT_TESTING
        elif trl == 6:
            return EvidenceCategory.PROTOTYPE
        elif trl == 7:
            return EvidenceCategory.OPERATIONAL_DEMONSTRATION
        elif trl == 8:
            return EvidenceCategory.INDEPENDENT_VERIFICATION
        else:
            return EvidenceCategory.DEPLOYMENT

    def _evaluate_strength(self, text: str, matched_keyword: str) -> EvidenceStrength:
        # Check if text contains quantitative units, numbers, test metrics
        has_metrics = bool(re.search(r"\b\d+(\.\d+)?\s*(%|hours?|ghz|mhz|nm|db|c|k|pa|bar|psi|v|w|kg|g)\b", text, re.IGNORECASE))
        has_speculative = bool(re.search(r"(?i)\b(will\s+be|planned|proposed|future\s+work|hypothesized)\b", text))

        if has_speculative:
            return EvidenceStrength.WEAK_SUPPORTING
        if has_metrics:
            return EvidenceStrength.STRONG_SUPPORTING
        return EvidenceStrength.MODERATE_SUPPORTING
