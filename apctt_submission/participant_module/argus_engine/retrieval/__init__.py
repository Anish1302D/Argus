"""
Retrieval Package.
Provides hybrid BM25 + lexical-semantic retrieval and criterion-aware evidence ranking.
"""

from retrieval.engine import (
    BM25Index,
    RankedEvidenceCandidate,
    RetrievalDocument,
    is_bare_trl_assertion,
    normalize_stem,
    tokenize,
)

__version__ = "0.2.0"

__all__ = [
    "BM25Index",
    "RankedEvidenceCandidate",
    "RetrievalDocument",
    "is_bare_trl_assertion",
    "normalize_stem",
    "tokenize",
]
