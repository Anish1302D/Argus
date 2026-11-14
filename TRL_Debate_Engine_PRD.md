# PRODUCT REQUIREMENTS DOCUMENT (PRD)

# ARGUS

### Adversarial Multi-Agent AI for Technology Readiness Assessment

**Version:** 1.0\
**Status:** Development Specification\
**Competition:** Techfest 2026--27 \| 2nd APCTT Hackathon 2026\
**Challenge:** AI for Technology Readiness\
**Target deployment:** Web application + standalone model inference
pipeline

------------------------------------------------------------------------

# 1. PRODUCT OVERVIEW

## 1.1 Product Name

Argus

> **Implementation-status note:** This document describes the intended product requirements and target experience. It must not be read as proof that every proposed architecture component is currently implemented. The active release uses deterministic evidence mining and rule-based adjudication with structured review synthesis; see README.md for the verified implementation boundary.

## 1.2 Product Vision

Build an intelligent, evidence-driven Technology Readiness Level (TRL)
assessment system that evaluates unstructured technical documentation
using adversarial multi-agent AI.

Unlike conventional AI systems that ask a single model to classify a
document, Argus introduces structured disagreement between
specialised AI agents.

Three reasoning roles participate:

1. **The Optimist:** Argues for the highest Technology Readiness Level
    justified by the available evidence.
2. **The Skeptic:** Challenges optimistic assumptions and argues for
    the lowest defensible Technology Readiness Level.
3. **The Referee:** Independently evaluates the evidence, challenges
    both positions and determines the final TRL.

The system must produce a defensible prediction supported by traceable
evidence, confidence indicators, identified gaps and actionable
recommendations.

## 1.3 Core Value Proposition

Traditional AI assessment:

Document → AI prediction → Result.

Argus:

Document → Evidence extraction → Independent opposing assessments →
Adversarial debate → Independent adjudication → Auditable TRL
assessment.

**Core innovation:** AI models are encouraged to disagree constructively
before reaching an evidence-based conclusion.

------------------------------------------------------------------------

# 2. PROBLEM STATEMENT

Technical documents frequently contain incomplete, ambiguous,
inconsistent or exaggerated claims about technology maturity.

A research paper may describe a successful laboratory experiment without
demonstrating validation in a relevant environment.

A patent may describe a proposed invention without proving that a
functional prototype exists.

A development report may claim operational readiness without providing
sufficient deployment evidence.

Conventional classification systems may incorrectly interpret these
claims as proof of technological maturity.

The proposed system addresses these problems through:

- Context-aware technical document analysis.
- Evidence extraction and verification.
- Adversarial reasoning.
- TRL-specific criteria matching.
- Contradiction detection.
- Explainable classification.
- Transparent reporting.

------------------------------------------------------------------------

# 3. OBJECTIVES

## 3.1 Primary Objectives

1. Automatically process unstructured technical documents.
2. Extract technology-related claims and supporting evidence.
3. Predict Technology Readiness Levels from 1 to 9.
4. Reduce overestimation caused by unsupported claims.
5. Identify missing evidence and technical validation gaps.
6. Generate transparent, auditable assessment reports.
7. Produce machine-readable output compatible with the competition's
    prescribed schema.

## 3.2 Secondary Objectives

- Compare multiple technical documents.
- Visualise the debate between AI agents.
- Generate recommendations for reaching the next TRL.
- Identify contradictory statements.
- Provide confidence and evidence-quality indicators.

## 3.3 Success Criteria

The system should:

- Run reliably on the competition's permitted evaluation environment.
- Produce valid output for every supported input.
- Maximise performance on hidden evaluation data.
- Provide evidence-grounded predictions.
- Avoid unsupported maturity claims.
- Maintain reproducibility between runs.

------------------------------------------------------------------------

# 4. UNDERSTANDING TECHNOLOGY READINESS LEVELS

The system must implement the official TRL 1--9 framework.

  TRL   Description
  ----- -------------------------------------------------------------
  1     Basic principles observed
  2     Technology concept formulated
  3     Experimental proof of concept
  4     Technology validated in a laboratory
  5     Technology validated in a relevant environment
  6     Technology demonstrated in a relevant environment
  7     System prototype demonstrated in an operational environment
  8     Actual system completed and qualified through testing
  9     Actual system proven in operational use

The implementation must use the exact official assessment definitions
and criteria provided by the competition organisers.

Do not assume that a document's claims automatically satisfy a TRL
requirement.

Distinguish between:

- Proposed work.
- Simulated results.
- Experimental results.
- Laboratory validation.
- Relevant-environment validation.
- Operational demonstrations.
- Independent verification.
- Actual deployment.

------------------------------------------------------------------------

# 5. TARGET USERS

## 5.1 Primary Users

- Research institutions.
- Technology evaluators.
- R&D teams.
- Innovation assessment organisations.
- Technology transfer offices.
- Researchers and engineering teams.

## 5.2 Secondary Users

- Universities.
- Startups.
- Government innovation programmes.
- Technology commercialisation organisations.
- Industrial research departments.

------------------------------------------------------------------------

# 6. CORE SYSTEM ARCHITECTURE

The system consists of six primary stages.

## Stage 1: Document Intelligence

**Input:** - Research papers. - Technical reports. - Patents. - R&D
documentation. - Prototype reports. - Experimental results.

**Responsibilities:** - PDF extraction. - OCR when required. - Section
detection. - Table extraction. - Metadata extraction. - Page and
paragraph identification.

**Output:** Structured document representation.

## Stage 2: Evidence Extraction Engine

Extract structured evidence such as:

- Technology objectives.
- Scientific principles.
- Technical concepts.
- Experimental results.
- Prototype descriptions.
- Testing methodology.
- Validation environments.
- Performance metrics.
- Deployment evidence.
- Manufacturing readiness.
- Operational limitations.

Each extracted evidence item must include:

- Evidence ID.
- Original text.
- Page number.
- Section name.
- Evidence category.
- Evidence strength.
- Associated TRL criteria.
- Extraction confidence.

## Stage 3: Optimist Agent

**Role:** Highest defensible readiness assessment.

Responsibilities:

1. Identify evidence supporting advanced technological maturity.
2. Identify demonstrated technical achievements.
3. Match evidence against higher TRL requirements.
4. Build the strongest reasonable case for the technology.
5. Identify the highest potentially justifiable TRL.
6. Cite supporting evidence for every significant claim.

**Output:** - Proposed TRL. - Supporting arguments. - Evidence
references. - Satisfied criteria. - Uncertainties. - Confidence.

The Optimist must not fabricate achievements or interpret proposed
activities as completed activities.

## Stage 4: Skeptic Agent

**Role:** Lowest defensible readiness assessment.

Responsibilities:

1. Challenge unsupported claims.
2. Identify missing experiments and validation.
3. Detect discrepancies between claims and demonstrated results.
4. Identify missing operational evidence.
5. Challenge the Optimist's assumptions.
6. Identify contradictory evidence.
7. Establish the lowest defensible TRL.

**Output:** - Proposed TRL. - Counterarguments. - Missing evidence. -
Contradictions. - Unsatisfied criteria. - Evidence references. -
Confidence.

The Skeptic must not automatically assign TRL 1 simply because evidence
is incomplete. It must identify the highest level actually supported by
the available evidence, while explaining uncertainty.

## Stage 5: Adversarial Debate Engine

**Purpose:** Facilitate structured disagreement between the Optimist and
Skeptic.

### Debate protocol

**Round 1: Independent Assessment**

Both agents independently analyse the extracted evidence. They must not
see each other's initial conclusions.

**Round 2: Argument Exchange**

The Optimist presents its strongest evidence-supported argument. The
Skeptic challenges unsupported claims and identifies gaps.

**Round 3: Counterargument**

The Optimist responds to the Skeptic's objections. The Skeptic evaluates
whether those responses resolve the objections.

**Round 4: Final Positions**

Both agents submit their final TRL positions and supporting evidence.

**Constraints:** - Maximum two debate exchanges after initial
independent assessment. - Every argument must reference evidence. -
Agents cannot invent facts. - Repeated arguments should be
discouraged. - The debate must terminate within defined execution
limits.

The debate must be structured and machine-readable, not merely free-form
conversation.

## Stage 6: Independent Referee

**Role:** Final adjudication.

The Referee must not simply average the two agent predictions.

Responsibilities:

1. Independently examine the extracted evidence.
2. Evaluate official TRL criteria.
3. Review the Optimist's arguments.
4. Review the Skeptic's objections.
5. Determine which claims are supported.
6. Resolve evidence contradictions.
7. Identify the highest fully defensible TRL.
8. Determine confidence and evidence sufficiency.
9. Generate a final explanation.

**Output:** - Final TRL. - Supporting evidence. - Rejected claims. -
Unresolved contradictions. - Criteria satisfied. - Criteria not
satisfied. - Confidence. - Next-stage recommendations.

The Referee must prioritise verified evidence over persuasive language.

------------------------------------------------------------------------

# 7. AI MODEL ARCHITECTURE

Use a hybrid ML and multi-agent architecture.

Do not rely entirely on generative LLM reasoning.

## 7.1 Proposed ML Components

### A. Text Understanding

Candidate models:

- SciBERT.
- SPECTER2.
- Sentence Transformers.

Purpose: - Understand technical language. - Generate document
embeddings. - Identify semantic similarities. - Support evidence
retrieval.

### B. Evidence Classification

Candidate approaches:

- Fine-tuned transformer classifier.
- Multi-label classification.
- Rule-assisted extraction.
- Structured information extraction.

Evidence categories should include:

- Concept.
- Simulation.
- Experiment.
- Prototype.
- Laboratory validation.
- Relevant-environment testing.
- Operational demonstration.
- Deployment.
- Independent verification.

### C. TRL Prediction

Evaluate:

- LightGBM.
- XGBoost.
- Random Forest as a baseline.
- Transformer-based classifier.
- Ordinal regression.
- CORAL-style ordinal classification.

TRL is ordinal data, not an arbitrary nine-category classification
problem.

The system should account for the distance between predicted and actual
TRL.

### D. Explainability

Candidate techniques:

- SHAP for structured-feature models.
- Feature importance.
- Evidence-to-criterion mapping.
- Confidence calibration.

### E. Retrieval

Use:

- BM25.
- Vector search.
- Hybrid retrieval.

Retrieve relevant passages from the document before agents make their
arguments.

## 7.2 Model Selection Policy

Do not select a model simply because it is popular.

Evaluate candidate models using:

- Validation accuracy.
- Ordinal error.
- Macro F1.
- Per-class precision and recall.
- Execution time.
- Memory requirements.
- Dependency compatibility.

Choose the best reproducible configuration that performs well on
validation data and can satisfy the official execution constraints.

------------------------------------------------------------------------

# 8. EVIDENCE CONFIDENCE AND CONTRADICTION DETECTION

This module is a major product differentiator.

## 8.1 Evidence Quality

Evidence must be evaluated on multiple dimensions:

1. **Directness:** Does it directly demonstrate the criterion?
2. **Specificity:** Does it provide measurable details?
3. **Verification:** Is the result independently verified?
4. **Environment:** Was the technology tested in an appropriate
    environment?
5. **Reproducibility:** Can the result be reproduced?
6. **Traceability:** Can the original source be identified?

Do not confuse evidence extraction confidence with actual scientific
validity.

## 8.2 Evidence Classification

Every evidence item should be classified as:

- Strong supporting evidence.
- Moderate supporting evidence.
- Weak supporting evidence.
- Contradictory evidence.
- Missing evidence.
- Unverified claim.

## 8.3 Contradiction Detection

Example:

Document A: A functional prototype has been successfully developed.

Document B: Prototype development is still ongoing.

The system must:

- Identify both claims.
- Preserve their source references.
- Detect the contradiction.
- Avoid automatically accepting either statement.
- Ask the Referee to evaluate context and chronology.

------------------------------------------------------------------------

# 9. PRODUCT FEATURES

## 9.1 Document Upload

Support PDF as the primary format.

Requirements:

- Drag-and-drop upload.
- File validation.
- Processing status.
- Document preview.
- Extracted text preview.
- Error handling.

The competition inference pipeline must also support the organisers'
prescribed input format.

## 9.2 AI Debate Room

A dedicated interface showing:

- Optimist's initial position.
- Skeptic's initial position.
- Supporting evidence.
- Counterarguments.
- Debate rounds.
- Final agent positions.
- Referee decision.

Display each argument with its original evidence citation.

## 9.3 TRL Assessment Dashboard

Display:

- Final TRL.
- Confidence indicator.
- Evidence quality.
- Satisfied criteria.
- Missing criteria.
- Debate disagreement.
- Recommended next TRL.

## 9.4 Evidence Explorer

Allow users to:

- View extracted evidence.
- Jump to original document pages.
- Filter evidence by category.
- View supporting and contradictory claims.
- Inspect agent citations.

## 9.5 Technology Improvement Roadmap

Generate recommendations based on the missing requirements for the next
TRL.

Example:

Current assessment: TRL 4.\
Potential next level: TRL 5.

Missing requirements: - Validation in a relevant environment. -
Documented test methodology. - Performance measurements under relevant
conditions.

Recommendations must be derived from the actual TRL criteria and
identified evidence gaps.

## 9.6 Assessment Report

Generate a structured report containing:

1. Document overview.
2. Final TRL assessment.
3. Optimist assessment.
4. Skeptic assessment.
5. Debate summary.
6. Referee justification.
7. Evidence references.
8. Contradictions.
9. Missing validation.
10. Next-stage recommendations.

------------------------------------------------------------------------

# 10. USER INTERFACE AND DESIGN REQUIREMENTS

The application should look like a professional technology intelligence
platform.

Avoid a generic chatbot appearance.

## 10.1 Design Direction

Visual identity:

- Dark graphite background.
- Deep navy and charcoal surfaces.
- Subtle cyan accents.
- Clean typography.
- Glass-like panels used selectively.
- Precise data visualisations.
- Restrained animations.

The product should feel like an advanced research and intelligence
workstation.

## 10.2 Main Navigation

1. Overview.
2. New Assessment.
3. Debate Room.
4. Evidence Explorer.
5. Assessment History.
6. Reports.
7. Settings.

## 10.3 Dashboard

Include:

- Welcome section.
- New assessment action.
- Recent assessments.
- TRL distribution.
- Processing statistics.
- Model performance information.

## 10.4 Assessment Workspace

**Left panel:** - Document information. - Extracted sections. - Evidence
list.

**Centre panel:** - Debate timeline. - Optimist. - Skeptic. -
Counterarguments.

**Right panel:** - Referee. - Final TRL. - Confidence. - Assessment
criteria.

The interface must be responsive and accessible.

## 10.5 Visualisations

Use Recharts for:

- TRL distribution.
- Evidence category distribution.
- Criteria completion.
- Model performance.
- Assessment comparisons.

Avoid displaying misleading numerical confidence values.

------------------------------------------------------------------------

# 11. TECHNICAL STACK

## Frontend

- Next.js.
- TypeScript.
- Tailwind CSS.
- Shadcn UI.
- Framer Motion.
- Recharts.

## Backend

- Python.
- FastAPI.
- Pydantic.
- Background processing where needed.

## AI and ML

- PyTorch.
- Scikit-learn.
- Hugging Face Transformers.
- Sentence Transformers.
- LightGBM / XGBoost.
- SHAP.

## AI Orchestration

- LangGraph or a lightweight custom orchestration layer.

Use explicit, controlled state transitions.

## Document Processing

- PyMuPDF.
- Docling if compatible with deployment constraints.
- OCR fallback when required.

## Database

Supabase PostgreSQL for application data.

Suggested tables:

### users

- id
- email
- created_at

### assessments

- id
- user_id
- document_name
- status
- predicted_trl
- confidence
- created_at

### documents

- id
- assessment_id
- storage_path
- extracted_text
- metadata

### evidence

- id
- assessment_id
- evidence_text
- page_number
- section_name
- evidence_category
- evidence_strength
- source_reference

### agent_assessments

- id
- assessment_id
- agent_type
- initial_trl
- final_trl
- reasoning
- evidence_references

### debate_messages

- id
- assessment_id
- round_number
- agent_type
- argument
- evidence_references
- created_at

### final_assessments

- id
- assessment_id
- final_trl
- confidence
- justification
- satisfied_criteria
- missing_criteria
- recommendations

Database access must use secure policies. Do not expose service-role
keys in the frontend.

## Deployment

- Frontend: Vercel.
- Backend: Render or another compatible Python hosting environment.
- Model: Deploy separately as an inference service where necessary.

**Important:** The competition's final submission must not depend on an
external hosted service unless explicitly permitted. The standalone
inference package and web application are separate deliverables.

------------------------------------------------------------------------

# 12. COMPETITION-SPECIFIC REQUIREMENTS

The official competition rules take precedence over this PRD.

The model must be designed for:

- Frozen model submissions.
- Hidden evaluation datasets.
- Strict output-schema validation.
- Execution-time constraints.
- Dependency checks.
- Reproducible inference.

## 12.1 Submission Architecture

Separate the project into:

A. Competition inference engine.\
B. Multi-agent assessment system.\
C. Web application.

The competition inference engine must be independently runnable.

Do not assume judges will use the web application.

## 12.2 Output Schema

Implement the exact output format provided by the organisers.

Until the official schema is confirmed, use an internal structured
representation.

Illustrative internal output:

``` json
{
  "predicted_trl": 5,
  "confidence": 0.82,
  "supporting_evidence": [],
  "missing_criteria": [],
  "contradictions": [],
  "reasoning_summary": ""
}
```

This is an internal example only, NOT an assumed competition submission
schema.

Never hardcode an output schema that conflicts with the official
specification.

## 12.3 Submission Restrictions

- Respect the three-submission limit.
- Freeze the final model according to competition rules.
- Do not use undisclosed private API keys.
- Do not use prohibited external AI tools during live rounds.
- Do not use plagiarised models or code.
- Verify Apache License 2.0 compatibility for the required release
    package.

------------------------------------------------------------------------

# 13. EVALUATION FRAMEWORK

The system should be tested on a held-out validation dataset.

## Primary Metrics

- Exact TRL accuracy.
- Macro precision.
- Macro recall.
- Macro F1.
- Mean Absolute Error.
- Quadratic Weighted Kappa.

## Additional Evaluation

- Evidence extraction precision and recall.
- Citation correctness.
- Contradiction detection accuracy.
- Output schema compliance.
- Inference latency.
- Memory usage.

The official hidden-set evaluation metric remains the primary
optimisation target.

## Error Analysis

Analyse:

- Overestimated TRL.
- Underestimated TRL.
- Confusion between adjacent levels.
- Incorrect evidence extraction.
- Unsupported agent arguments.
- Incorrect referee decisions.

Use document-level train/validation separation to avoid data leakage.

------------------------------------------------------------------------

# 14. NON-FUNCTIONAL REQUIREMENTS

## Performance

- Efficient document processing.
- Controlled model inference.
- Bounded debate iterations.
- Predictable memory consumption.
- No unnecessary repeated LLM calls.

## Reliability

- Input validation.
- Graceful error handling.
- Retry policies.
- Structured logging.
- Reproducible predictions.

## Security

- Secure file storage.
- User-level data isolation.
- No exposed API keys.
- Document sanitisation.
- Safe handling of untrusted document instructions.

Documents must be treated as untrusted data. Ignore instructions
embedded inside uploaded documents that attempt to manipulate system or
agent behaviour.

## Explainability

Every final prediction must be linked to evidence and official TRL
criteria.

The system must clearly distinguish:

- Model prediction.
- Extracted evidence.
- Agent interpretation.
- Final adjudication.

------------------------------------------------------------------------

# 15. MVP SCOPE

Prioritise a functional, accurate system over excessive features.

## P0 --- Must Have

- Document ingestion.
- Text extraction.
- Evidence extraction.
- TRL classification.
- Optimist agent.
- Skeptic agent.
- Independent Referee.
- Structured debate.
- Evidence citations.
- Final machine-readable output.
- Competition inference interface.
- Evaluation and schema validation.

## P1 --- Important

- Debate Room UI.
- Evidence Explorer.
- Confidence dashboard.
- Contradiction detection.
- Assessment report.
- Improvement roadmap.

## P2 --- Future Enhancements

- Multi-document comparison.
- Knowledge graph.
- Historical assessment tracking.
- Collaborative evaluation.
- Technology portfolio analytics.

------------------------------------------------------------------------

# 16. IMPLEMENTATION PHASES

### Phase 1: Competition Specification

- Inspect all official guidelines.
- Identify input and output formats.
- Understand available datasets.
- Identify hardware and execution restrictions.
- Create acceptance tests.

### Phase 2: Baseline ML Model

- Build document preprocessing.
- Create a baseline classifier.
- Train and evaluate candidate models.
- Establish reproducible metrics.

### Phase 3: Evidence Intelligence

- Implement extraction.
- Build evidence classification.
- Add source traceability.
- Implement criteria mapping.

### Phase 4: Multi-Agent Engine

- Build Optimist.
- Build Skeptic.
- Implement controlled debate.
- Build independent Referee.
- Add contradiction detection.

### Phase 5: Integration

- Connect the inference engine.
- Implement structured output.
- Add validation.
- Benchmark execution.

### Phase 6: Frontend

- Build dashboard.
- Build document workspace.
- Build debate visualisation.
- Build final assessment report.

### Phase 7: Testing and Submission

- Test against validation data.
- Fix classification errors.
- Test edge cases.
- Verify output schema.
- Package reproducible inference.
- Freeze the final submission.

------------------------------------------------------------------------

# 17. ACCEPTANCE CRITERIA

The product is considered MVP-complete when:

1. A valid supported document can be processed.
2. Relevant technical evidence can be extracted.
3. Evidence has source references.
4. Both agents independently generate assessments.
5. Both agents can challenge one another.
6. The Referee produces an independent final decision.
7. The final TRL is between 1 and 9.
8. The final decision includes evidence and justification.
9. Missing criteria are identified.
10. Invalid documents are handled gracefully.
11. The official competition output schema is satisfied.
12. The inference package runs independently of the frontend.

------------------------------------------------------------------------

# 18. IMPORTANT ENGINEERING PRINCIPLES

1. Accuracy before visual sophistication.
2. Evidence before opinions.
3. Independent assessment before debate.
4. Verification before final adjudication.
5. Ordinal-aware classification instead of naive classification.
6. No fabricated evidence.
7. No unsupported TRL claims.
8. Reproducible ML experiments.
9. Modular and testable architecture.
10. Strict adherence to competition rules.

Do not build a frontend-only simulation of three agents. The underlying
model pipeline must genuinely execute the required processing and
assessment.

Do not make up model accuracy or confidence scores.

------------------------------------------------------------------------

# 19. INSTRUCTIONS TO THE DEVELOPMENT AGENT

You are acting as the lead AI engineer, ML architect, backend developer
and product engineer for Argus.

Before implementation:

1. Inspect the existing repository and understand its current
    structure.
2. Read the official competition guidelines and any available dataset
    documentation.
3. Identify the actual competition input format, output schema and
    execution constraints.
4. Prepare a technical implementation plan.
5. Identify missing dependencies and infrastructure requirements.
6. Separate the competition model from the web application.

## Implementation Rules

- Do not blindly generate the entire application in one pass.
- Build modular components.
- Maintain clear separation between ML inference, document processing,
    agent orchestration and frontend.
- Write unit tests.
- Write integration tests.
- Track model performance.
- Validate every output.
- Maintain a README with setup and execution instructions.
- Do not invent datasets, model weights, performance metrics or
    official schemas.
- Do not use mock agent outputs as a substitute for actual inference.
- If an external API is unavailable, build a configurable adapter and
    a clearly documented fallback.
- Keep the competition inference pipeline compatible with the
    permitted execution environment.

## FIRST TASK

Do not immediately start generating the entire codebase.

First produce:

1. Repository analysis.
2. System architecture.
3. Database schema.
4. ML pipeline design.
5. Agent interaction protocol.
6. Competition inference design.
7. Development milestones.
8. Identified technical risks.

Present the implementation plan for review.

After the architecture is established, implement the MVP in prioritised
phases, testing each phase before proceeding.

## FINAL PRODUCT GOAL

A scientifically defensible, evidence-grounded, adversarial multi-agent
AI system that evaluates technology readiness, explains its conclusions
and produces reproducible TRL 1--9 predictions.
