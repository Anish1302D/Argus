# ARGUS Technical Methodology Specification
**Version:** 2.0.0-argus  
**Classification:** Technical Architecture & Scientific Methodology Specification  
**System:** ARGUS Evidence Intelligence Engine  
**Deployment Constraint:** 100% Air-Gapped, Zero External Network Calls, Deterministic Execution  

---

## 1. Executive Summary & Methodological Philosophy

ARGUS (Automated Readiness Grading & Uncertainty Synthesis) evaluates the Technology Readiness Level (TRL 1–9) of advanced aerospace, defense, energy, and deep-tech engineering documentation. 

Traditional readiness assessment systems suffer from two fatal failure modes:
1. **Keyword Overconfidence:** Naive keyword or string matching mistakes speculative claims, introductory literature reviews, or negated historical failures for verified operational maturity.
2. **Generative Hallucination & Epistemic Opacity:** LLM-based black-box evaluators invent non-existent experimental evidence, fluctuate across identical runs, and cannot trace claims to verifiable character offsets in source documentation.

ARGUS 2.0.0 resolves these deficiencies through a **14-stage modular pipeline** that combines high-precision deterministic claim extraction, grammatical modality analysis, multi-agent adversarial argumentation, explicit criteria checklist verification, multi-dimensional uncertainty decomposition, and immutable cryptographic audit trails.

---

## 2. Canonical 14-Stage Assessment Pipeline

Every technical document ingested into ARGUS undergoes the following sequential processing stages:

```
[1. Input Sanitization] ───> [2. Structural Chunking] ───> [3. Claim Extraction]
                                                                     │
[6. Contradiction Detection] <── [5. Quality Scoring] <─── [4. Modality Analysis]
         │
         ▼
[7. Candidate TRL Gate] ───> [8. Criteria Mapping] ───> [9. Adversarial Review]
                                                                     │
[12. Uncertainty Profile] <── [11. Gap Analysis] <────── [10. Referee Adjudication]
         │
         ▼
[13. Relational Ledger] ───> [14. Audit Trail & SHA-256 Hash] ───> Final Assessment
```

### Stage 1: Input Sanitization & Threat Neutralization
- **Purpose:** Protects the downstream pipeline against adversarial prompt injections, indirect delimiter escapes, roleplay hijack attacks, and Unicode zero-width evasion attacks.
- **Mechanism:** Text is passed through `Sanitizer.sanitize_text()`. In strict mode (`strict_security=True`), high-severity prompt injections trigger an immediate security rejection. In standard production mode, adversarial injection phrases are neutralized while stripping dangerous zero-width and invisible directional Unicode characters (`\u200B`, `\u200E`, `\uFEFF`).

### Stage 2: Structural Chunk Decomposition & Context Preservation
- **Purpose:** Segments raw text or multi-page PDF documents into manageable contextual chunks while retaining document identifiers, page numbers, section headers, and character boundaries.
- **Mechanism:** `DocumentExtractor` generates `Chunk` entities with `char_offset_start` and `char_offset_end`.

### Stage 3: Structured Technical Claim & Measurement Extraction
- **Purpose:** Extracts empirical claims and quantitative measurements beyond superficial keyword matching.
- **Mechanism:** `StructuredClaimExtractor` extracts:
  - Quantitative measurements: Value, unit, scientific context, and tolerances ($\pm \delta$).
  - Achievement categories: Mapped to candidate TRL levels (TRL 1 to TRL 9).
  - Verbatim excerpt slices and exact character offsets.

### Stage 4: Modality, Temporal, and Negation Classification
- **Purpose:** Grammatically classifies each technical claim to distinguish verified accomplishments from unperformed or hypothetical ideas.
- **Taxonomy:**
  - `COMPLETED`: Empirical milestones executed and verified.
  - `UNPERFORMED` / `NEGATED`: Milestones explicitly negated or not yet executed (e.g., *"no flight test has been conducted"*, *"has not flown"*).
  - `PLANNED`: Future proposed or roadmapped work (e.g., *"scheduled for Q4"*, *"will be demonstrated"*).
  - `HYPOTHETICAL`: Speculative statements (e.g., *"could theoretically achieve"*).
  - `SIMULATED`: Purely numerical, finite-element, or computational models without physical hardware.

### Stage 5: Empirical Specificity & Evidence Quality Assessment
- **Purpose:** Grades evidence items according to empirical rigor, quantitative data support, and experimental specificity.
- **Classification:** Categorizes evidence into `EMPIRICAL`, `SIMULATION`, `THEORETICAL`, or `SPECIFICATION`, assigning quality weights ranging from `VERY_STRONG` to `WEAK`.

### Stage 6: Contradictory Evidence Detection (Abstract vs Limitations)
- **Purpose:** Identifies document tensions where high-level summary claims in abstracts or conclusions are refuted by technical disclaimers, test failure notes, or limitation disclosures in the body text.
- **Mechanism:** Evaluates pairwise cross-claims. If an asserted milestone (e.g., TRL 7 flight demonstration) is contradicted by a negated or unperformed statement (e.g., *"suborbital flights have not yet been performed"*), a high-severity `ContradictionItem` is generated.

### Stage 7: Preliminary Candidate TRL Feature Gate
- **Purpose:** Computes the preliminary candidate maturity level $L_{cand}$ based on ordinal feature vectors and high-strength empirical evidence items.

### Stage 8: Canonical TRL 1–9 Criteria Checklist Mapping
- **Purpose:** Maps all extracted claims and evidence against the official 9-level TRL ladder criteria.
- **Status Codes:**
  - `DIRECTLY_SATISFIED`: Supported by observed, non-negated empirical evidence.
  - `PARTIALLY_SUPPORTED`: Preliminary or simulated validation without full parameter demonstration.
  - `SATISFIED_INFERRED`: Prerequisite foundational criteria implicitly satisfied by verified higher-level achievements.
  - `CONTRADICTORY`: Criterion challenged by documented failure or limitation.
  - `MISSING`: No evidence found in document for this mandatory criterion.

### Stage 9: Formal Adversarial Debate Protocol (Optimist vs Skeptic)
- **Purpose:** Subject candidate maturity claims to formal multi-perspective debate.
- **Actors:**
  - **The Optimist:** Constructs the strongest defensible maturity argumentation, citing evidence IDs, quantitative metrics, and testing environments.
  - **The Skeptic:** Methodically challenges every claim, highlighting missing prerequisites, unperformed milestones, simulation-only testing, and detected contradictions.

### Stage 10: Referee Adjudication Ledger & Prerequisite Audit
- **Purpose:** Acts as the deterministic final arbiter.
- **Mechanism:** Evaluates Optimist arguments against Skeptic challenges.
  - If a fatal blocker or unresolved contradiction exists, the Referee downgrades the maturity level to the highest uncompromised tier.
  - Generates an immutable Adjudication Ledger recording accepted evidence, rejected claims, and prerequisite audits.

### Stage 11: Advancement Gap Analysis (Target: TRL N+1)
- **Purpose:** Produces actionable engineering recommendations detailing exact requirements to reach the next readiness level.
- **Components:** Target next TRL, required operational/validation environment, explicit missing criteria, and actionable engineering activities.

### Stage 12: Decoupled Multi-Dimensional Uncertainty Profiling
- **Purpose:** Separates extraction reliability from evidence completeness and document tension.
- **Mathematical Formula:** (See Section 3).

### Stage 13: Relational Evidence Ledger
- **Purpose:** Establishes a fully queryable relational graph linking `Document` $\to$ `Claim` $\to$ `Evidence` $\to$ `TRL Criterion` $\to$ `Adjudication Decision`.

### Stage 14: Immutable Cryptographic Audit Trail
- **Purpose:** Guarantees 100% deterministic reproducibility.
- **Mechanism:** Every rule invocation, state transition, and intermediate outcome is hashed using SHA-256. Identical document text with identical configuration yields identical cryptographic hashes.

---

## 3. Mathematical Formulations & Thresholds

### 3.1 Composite Certainty Formulation
Uncertainty in ARGUS is decoupled into three orthogonal dimensions:
1. **Extraction Confidence ($c_{ext} \in [0, 1]$):** The linguistic certainty and quantitative grounding of extracted technical claims.
2. **Criteria Coverage ($c_{cov} \in [0, 1]$):** The proportion of canonical criteria for the target TRL satisfied by empirical evidence:
   $$c_{cov} = \frac{|\text{Satisfied Criteria}| + 0.5 \cdot |\text{Partially Supported Criteria}|}{|\text{Total Required Criteria for Target TRL}|}$$
3. **Conflict Penalty ($p_{conflict} \in [0, 0.40]$):** The cumulative penalty from internal document contradictions:
   $$p_{conflict} = \min\left(0.40, \sum_{i=1}^{k} \omega(c_i)\right)$$
   where $\omega(c_i) = 0.20$ for HIGH severity contradictions and $0.10$ for MEDIUM severity contradictions.

The **Composite Certainty Score ($C \in [0.10, 1.00]$)** is defined as:
$$C = \text{clamp}\left(0.40 \cdot c_{ext} + 0.40 \cdot c_{cov} - p_{conflict}, \; 0.10, \; 0.99\right)$$

### 3.2 Evaluation Metrics Formulations

#### 1. Quadratic Weighted Kappa (QWK)
Measures inter-rater agreement between ground-truth TRL $y_i$ and predicted TRL $\hat{y}_i$, penalizing errors quadratic in distance:
$$w_{ij} = \frac{(i - j)^2}{(N - 1)^2}$$
$$\kappa = 1 - \frac{\sum_{i,j} w_{ij} O_{ij}}{\sum_{i,j} w_{ij} E_{ij}}$$
where $O_{ij}$ is the observed confusion matrix, and $E_{ij}$ is the expected matrix under independence.

#### 2. Mean Absolute Error (MAE)
$$\text{MAE} = \frac{1}{M} \sum_{k=1}^{M} |y_k - \hat{y}_k|$$

#### 3. Adjacent-Level Accuracy ($\text{Acc}_{\pm 1}$)
$$\text{Acc}_{\pm 1} = \frac{1}{M} \sum_{k=1}^{M} \mathbb{I}(|y_k - \hat{y}_k| \le 1)$$

#### 4. Expected Calibration Error (ECE)
For $B$ certainty bins:
$$\text{ECE} = \sum_{b=1}^{B} \frac{|B_b|}{M} \left| \text{acc}(B_b) - \text{conf}(B_b) \right|$$

---

## 4. Epistemic Calibration & Methodological Limitations Register

In accordance with strict scientific validation principles, ARGUS provides complete disclosure regarding its epistemic boundaries:

| Limitation Category | Architectural Boundary | Operational Remediation |
|---|---|---|
| **Deterministic Synthesis vs LLM** | ARGUS multi-agent debate (Optimist, Skeptic, Referee) is powered by deterministic rule-based state-machine synthesis, NOT an ungrounded non-deterministic LLM. | Ensures 100% reproducibility, zero token costs, zero drift, and full compliance with air-gap competition mandates. |
| **Heuristic Confidence Disclosure** | Confidence percentages are bounded composite heuristics combining coverage and linguistic quality, not frequentist Bayesian posterior probabilities. | Explicitly disclosed in API responses and frontend as `UNCALIBRATED_HEURISTIC_BOUNDED`. |
| **Language & Morphology Scope** | The claim extractor uses English engineering morphology and technical lexicon patterns. | Non-English documents or highly idiosyncratic non-standard engineering acronyms should be normalized prior to ingestion. |
| **Air-Gap Operational Boundary** | No external APIs, web searches, or online vector databases are invoked during runtime inference. | The entire evaluation graph executes locally in memory within $<100$ ms per document. |

---
*Authorized by the ARGUS Principal Systems Architecture & Scientific Validation Directorate.*
