"""
Hybrid Lexical & Criterion-Aware Evidence Retrieval Engine for ARGUS.

Provides deterministic, CPU-fast Okapi BM25 + TF-IDF n-gram hybrid retrieval
and criterion-aware evidence ranking without requiring external network access
or non-base packages.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[-._/][A-Za-z0-9]+)*")

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "having",
        "he",
        "her",
        "here",
        "hers",
        "him",
        "his",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "just",
        "may",
        "might",
        "more",
        "most",
        "must",
        "my",
        "no",
        "nor",
        "not",
        "now",
        "of",
        "off",
        "on",
        "once",
        "only",
        "or",
        "other",
        "our",
        "ours",
        "out",
        "over",
        "own",
        "same",
        "she",
        "should",
        "so",
        "some",
        "such",
        "than",
        "that",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "very",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "would",
        "you",
        "your",
        "yours",
    }
)

# Bare TRL assertion regex: matches spans that ONLY claim a TRL level without technical substance
BARE_TRL_ASSERTION_RE = re.compile(
    r"^\s*(?:the\s+)?(?:technology|system|component|subsystem|project|method|tool|model|prototype)?\s*"
    r"(?:is\s+(?:at|currently\s+at|assessed\s+at)|has\s+reached|achieved|attained|corresponds\s+to)?\s*"
    r"(?:a\s+)?(?:technology\s+readiness\s+level|trl)\s*(?:of\s*)?[1-9](?:\s*[/\-–]\s*[1-9])?\s*[.!]?\s*$",
    re.IGNORECASE,
)


def normalize_stem(token: str) -> str:
    """Lightweight deterministic suffix stripping for technical English."""
    t = token.lower().strip("-._/")
    if len(t) <= 3:
        return t
    for suffix in (
        "izations",
        "ization",
        "ational",
        "fulness",
        "ousness",
        "iveness",
        "ements",
        "ement",
        "ations",
        "ation",
        "ities",
        "ingly",
        "edly",
        "ments",
        "ment",
        "ness",
        "ings",
        "ing",
        "able",
        "ible",
        "ions",
        "ion",
        "ates",
        "ated",
        "ate",
        "ers",
        "ied",
        "ies",
        "ed",
        "es",
        "er",
        "ly",
        "s",
    ):
        if t.endswith(suffix) and len(t) - len(suffix) >= 3:
            return t[: -len(suffix)]
    return t


def tokenize(text: str, include_stems: bool = True) -> List[str]:
    """Tokenize text into lowercase content terms plus optional stems."""
    if not text:
        return []
    raw_tokens = [m.group(0).lower() for m in TOKEN_RE.finditer(text)]
    tokens: List[str] = []
    for tok in raw_tokens:
        if tok in STOPWORDS or len(tok) < 2:
            continue
        tokens.append(tok)
        if include_stems:
            stem = normalize_stem(tok)
            if stem != tok and len(stem) >= 3 and stem not in STOPWORDS:
                tokens.append(stem)
        # Also split hyphenated words so "bench-scale" matches both "bench-scale" and "bench", "scale"
        if "-" in tok:
            for part in tok.split("-"):
                if len(part) >= 2 and part not in STOPWORDS:
                    tokens.append(part)
                    if include_stems:
                        p_stem = normalize_stem(part)
                        if p_stem != part and len(p_stem) >= 3:
                            tokens.append(p_stem)
    return tokens


@dataclass
class RetrievalDocument:
    """A retrievable passage or page unit with full provenance."""

    passage_id: str
    document_id: str
    page: int
    text: str
    section: Optional[str] = None
    document_date: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RankedEvidenceCandidate:
    """A scored candidate passage with verbatim span and diagnostic breakdown."""

    document_id: str
    page: int
    supporting_span: str
    score: float
    bm25_score: float = 0.0
    tfidf_score: float = 0.0
    target_alignment_score: float = 0.0
    modality: str = "COMPLETED"
    is_negated: bool = False
    is_quantitative: bool = False
    matched_terms: List[str] = field(default_factory=list)


class BM25Index:
    """
    Deterministic Okapi BM25 + TF-IDF Hybrid Index over a collection of passages.
    Zero external dependencies outside Python standard library and NumPy.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.passages: List[RetrievalDocument] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_freqs: List[Counter[str]] = []
        self.doc_lens: np.ndarray = np.zeros(0, dtype=np.float64)
        self.avgdl: float = 1.0
        self.idf: Dict[str, float] = {}
        self.N: int = 0

    def build(self, passages: Sequence[RetrievalDocument]) -> "BM25Index":
        self.passages = list(passages)
        self.N = len(self.passages)
        if self.N == 0:
            self.doc_tokens = []
            self.doc_freqs = []
            self.doc_lens = np.zeros(0, dtype=np.float64)
            self.avgdl = 1.0
            self.idf = {}
            return self

        self.doc_tokens = [tokenize(p.text) for p in self.passages]
        self.doc_freqs = [Counter(toks) for toks in self.doc_tokens]
        self.doc_lens = np.array([max(len(toks), 1) for toks in self.doc_tokens], dtype=np.float64)
        self.avgdl = float(np.mean(self.doc_lens)) if self.N > 0 else 1.0

        df_counts: Counter[str] = Counter()
        for tf_map in self.doc_freqs:
            for term in tf_map.keys():
                df_counts[term] += 1

        self.idf = {}
        for term, df in df_counts.items():
            # Standard Robertson-Sparck Jones IDF with smoothing
            self.idf[term] = math.log(1.0 + (self.N - df + 0.5) / (df + 0.5))

        return self

    def score_query(self, query_text: str, extra_terms: Optional[Sequence[str]] = None) -> np.ndarray:
        """Compute hybrid BM25 + TF-IDF cosine score for every passage in the index."""
        if self.N == 0:
            return np.zeros(0, dtype=np.float64)

        q_tokens = tokenize(query_text)
        if extra_terms:
            for term in extra_terms:
                q_tokens.extend(tokenize(term))

        if not q_tokens:
            return np.zeros(self.N, dtype=np.float64)

        q_counts = Counter(q_tokens)
        scores = np.zeros(self.N, dtype=np.float64)

        for idx, tf_map in enumerate(self.doc_freqs):
            dl = self.doc_lens[idx]
            norm_factor = self.k1 * (1.0 - self.b + self.b * (dl / max(self.avgdl, 1.0)))
            doc_score = 0.0
            matched_unique = 0
            for term, q_weight in q_counts.items():
                tf = tf_map.get(term, 0)
                if tf <= 0:
                    continue
                matched_unique += 1
                idf_val = self.idf.get(term, 0.5)
                denom = tf + norm_factor
                bm25_term = idf_val * ((tf * (self.k1 + 1.0)) / max(denom, 1e-9))
                doc_score += bm25_term * (1.0 + 0.25 * math.log1p(q_weight))

            if matched_unique > 0:
                # Coverage bonus for matching multiple distinct query terms
                coverage = matched_unique / max(len(q_counts), 1)
                scores[idx] = doc_score * (1.0 + 0.35 * coverage)

        return scores

    def search(
        self,
        query_text: str,
        top_k: int = 10,
        extra_terms: Optional[Sequence[str]] = None,
    ) -> List[Tuple[RetrievalDocument, float]]:
        """Return top-k passages sorted by descending score."""
        scores = self.score_query(query_text, extra_terms=extra_terms)
        if len(scores) == 0:
            return []
        ranked_indices = np.argsort(-scores)
        results: List[Tuple[RetrievalDocument, float]] = []
        for idx in ranked_indices[:top_k]:
            sc = float(scores[int(idx)])
            if sc <= 0.0:
                break
            results.append((self.passages[int(idx)], sc))
        return results


def is_bare_trl_assertion(span: str) -> bool:
    """
    Return True if a span merely asserts a TRL number without describing technical work,
    tests, conditions, or results (Part C scoring rule).
    """
    cleaned = " ".join(span.strip().split())
    if not cleaned:
        return True
    if BARE_TRL_ASSERTION_RE.match(cleaned):
        return True
    # Also catch very short spans (< 55 chars) that mention TRL [1-9] without verbs of testing/analysis
    if len(cleaned) < 55 and re.search(r"\btrl\s*[1-9]\b", cleaned, re.IGNORECASE):
        if not re.search(
            r"\b(test|validat|calibrat|measur|simulat|integrat|deploy|operat|experiment|demonstrat|analy)\w*",
            cleaned,
            re.IGNORECASE,
        ):
            return True
    return False
