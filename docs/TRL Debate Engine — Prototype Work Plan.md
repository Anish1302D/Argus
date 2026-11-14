# Argus — Prototype Work Plan

**Repository:** `Anish1302D/Argus`  
**Plan date:** November 10, 2026  
**Target:** A credible, runnable prototype and competition submission candidate by November 15, 2026 (23:59 IST, per the repository checklist).  
**Scope assumption:** Prioritize a trustworthy standalone assessment pipeline and a clear demo. A polished web application is not a prerequisite for this deadline.

---

## 1. Current Baseline

The repository currently contains a Python CLI, PDF and text extraction, regex/keyword-based evidence mining, deterministic TRL adjudication, canonical output models/adapters, prompt-injection checks, and unit-test files.

The following work is not yet demonstrated as complete in the checked-out source:

- Evidence extraction is heuristic and must not treat a keyword match alone as proof of a claim.
- The Optimist/Skeptic positions and transcript are currently assembled in the adjudicator; a separate, genuinely executed debate engine is not yet present.
- The agent orchestration, retrieval, and API/UI modules are largely empty or skeletal.
- Confidence values are heuristic, not calibrated; do not present them as measured probabilities.
- The repository checklist contains benchmark claims that need reconciliation with the latest commit, which removed synthetic benchmark data and disabled ML fitting pending verified official labels.
- The test suite could not be run during this review because `pytest` is not installed in the review environment. This is an environment limitation; test status remains unverified.

**Product rule:** Label implemented behavior honestly. Do not describe mocked or rule-generated agent messages as a live multi-agent debate, and do not publish performance metrics until they are reproduced from permitted, traceable data.

---

## 2. MVP Goal and Definition of Done

A reviewer should be able to provide a supported PDF or text document, run the standalone pipeline offline, and receive a valid machine-readable assessment that is explainable and traceable to the input.

The deadline MVP is done when:

- [ ] A clean environment can install the declared submission dependencies.
- [ ] The standalone CLI accepts supported PDF and text/Markdown inputs and writes the expected output.
- [ ] Extracted evidence includes usable page references and source locations where available.
- [ ] The result distinguishes evidence found, evidence strength, missing criteria, limitations, and recommendations.
- [ ] Negated, proposed, planned, or otherwise unverified claims are not silently treated as completed proof.
- [ ] Empty, unreadable, invalid, and security-flagged inputs fail clearly and predictably.
- [ ] Output is validated against the currently applicable schema or clearly labeled internal schema; unknown official format details remain behind the adapter.
- [ ] Tests run from a clean setup and their exact result is recorded.
- [ ] No synthetic-data performance claims or unsupported confidence claims remain in user-facing docs.
- [ ] A short demo example can be reproduced from the documented commands.

---

## 3. Daily Phases and Work Items

### Day 1 — November 10: Scope, evidence, and release truth

**Objective:** Align the repository, documentation, and submission target around facts that can be verified.

- [ ] Confirm whether the official supplemental rules, output schema, sample cases, and approved datasets are available to the team. Record source and date for each.
- [ ] Reconcile `docs/pre_submission_checklist.md`, `README.md`, and `submission/README.md` with the latest deterministic-only submission mode.
- [ ] Remove, retract, or clearly mark benchmark scores and latency/memory claims that cannot currently be reproduced from permitted data and a reproducible script.
- [ ] Separate verified requirements from unknowns. Do not guess a required organizer schema or invocation format.
- [ ] Agree on supported inputs, output fields, security behavior, and a short list of must-pass test cases.
- [ ] Decide explicitly whether a UI is in deadline scope. Default: no, unless the inference path is already stable.

**Acceptance gate:** The team can explain exactly what the prototype does today, what it does not do, and which competition requirements remain unknown.

### Day 2 — November 11: Reliable inference vertical slice

**Objective:** Make the real input-to-output path defensible and inspectable.

- [ ] Exercise PDF, TXT, and Markdown input paths, including multi-page PDFs, malformed files, empty files, and PDFs with no extractable text.
- [ ] Ensure sanitization and extraction produce consistent, traceable content; verify page numbers and offsets with a small hand-checked fixture set.
- [ ] Improve evidence rules around negation, modality (`planned`, `proposed`, `will`), failed results, and claims without demonstrated test evidence.
- [ ] Ensure each reported supporting claim has a source reference; do not convert a bare keyword hit into verified evidence.
- [ ] Review how the selected TRL is bounded by evidence and criteria; document the rule and known failure modes.
- [ ] Ensure no-evidence and low-quality-extraction cases return a cautious assessment with explicit limitations.
- [ ] Add regression tests for every behavior changed.

**Acceptance gate:** At least one hand-reviewed document result can be traced from assessment → evidence item → input page/text; a negative or planned claim is not presented as completed validation.

### Day 3 — November 12: Clean install and diagnostic candidate

**Objective:** Produce the first reproducible standalone candidate and use the first diagnostic opportunity if available.

- [ ] Create a fresh Python 3.10+ virtual environment and install from `submission/requirements.txt` (or the officially required dependency file).
- [ ] Run the CLI using only the documented command; confirm there are no hidden dependencies on the repository root, local models, secrets, or network.
- [ ] Run unit and integration tests; install the declared development/test dependencies if needed. Record command, environment, and result.
- [ ] Validate output JSON programmatically, including TRL bounds, required fields, evidence references, and error behavior.
- [ ] Test at least one supported PDF, one text/Markdown file, one empty/invalid file, and one prompt-injection case.
- [ ] Verify package inclusion, licenses, dependency compatibility, and offline execution.
- [ ] If the organizer accepts the planned diagnostic submission on Nov 12, submit the operational candidate and preserve feedback verbatim.

**Acceptance gate:** Another developer can create a clean environment, run the documented command, and reproduce a valid output. If a diagnostic is submitted, its exact artifact/version is tagged or otherwise recorded.

### Day 4 — November 13: Fix diagnostic and test failures

**Objective:** Fix the highest-impact defects without destabilizing the pipeline.

- [ ] Triage diagnostic feedback and test failures into: blocker, important, and deferred.
- [ ] Fix schema, packaging, import, dependency, CLI, and crash issues before tuning prediction rules.
- [ ] Add one regression test per fixed defect.
- [ ] Do not adjust thresholds against a tiny sample unless the change is explained and validated on permitted, independent cases.
- [ ] Re-run the clean-install workflow after changes.
- [ ] Update assumptions/unknowns and record anything still awaiting official clarification.

**Acceptance gate:** All known blockers are closed or explicitly documented with a fallback; the diagnostic build remains reproducible.

### Day 5 — November 14: Demo clarity and release candidate

**Objective:** Make the prototype easy to understand without disguising its limitations.

- [ ] Produce one small, legally usable demo input and its generated output; identify the sample as illustrative and not training/evaluation data if applicable.
- [ ] Improve the human-readable report or CLI summary to show final TRL, evidence citations, missing criteria, recommendations, and limitations.
- [ ] Use confidence wording carefully. If the value is heuristic, label it as a heuristic indicator or remove it from prominent display.
- [ ] Make the output and documentation distinguish actual pipeline results from any illustrative visualization.
- [ ] Verify that all reported debate/agent fields accurately describe their deterministic or genuine source.
- [ ] Freeze feature work after the release-candidate test run; fix only release-blocking defects.

**Acceptance gate:** A first-time reviewer can run one example, understand the assessment and its evidence, and see the system's limitations without needing verbal explanation.

### Day 6 — November 15: Final verification and freeze

**Objective:** Submit a stable, auditable artifact before the stated deadline.

- [ ] Run the full test suite from a fresh environment and save the output.
- [ ] Run the full CLI smoke-test matrix and validate every produced JSON file.
- [ ] Confirm offline operation, dependency list, licensing, package layout, and absence of private keys or secret configuration.
- [ ] Recheck official input/output rules and update adapters only from confirmed instructions.
- [ ] Verify README commands from a clean checkout or packaged submission directory.
- [ ] Tag or archive the exact candidate; record commit SHA, package checksum, test results, and submission timestamp.
- [ ] Submit with time to spare; do not make untested changes after freeze.

**Acceptance gate:** One known artifact has passed the recorded release checks and is the artifact actually submitted.

---

## 4. Work That Should Wait Until After the Deadline MVP

These are valuable, but should not displace submission reliability unless the core path is already green:

1. **Real multi-agent debate:** Implement independent Optimist and Skeptic assessments, bounded argument exchange, citation validation, early termination, and an independent Referee. Mark the current transcript as rule-generated until this exists.
2. **Evidence intelligence:** Improve extraction beyond regexes; add robust claim classification, negation, chronology, contradiction detection, evidence quality, and citation validation.
3. **Retrieval:** Add hybrid BM25/vector retrieval only when it improves traceability and can run within resource constraints.
4. **Evaluation:** Obtain verified, permitted, labeled cases; use document-level separation; report ordinal and per-class metrics with sample size and scripts. Never invent labels or use test data to tune and report as held out.
5. **Web demo:** Add upload/status/results, evidence explorer, and a clear assessment workspace after the backend contract stabilizes. Keep the web app separate from the air-gapped competition runner.
6. **Production capabilities:** Authentication, secure storage, database policies, history, deployment, observability, and multi-user support.

---

## 5. Risk Register

| Risk | Why it matters | Mitigation / decision |
|---|---|---|
| Unknown official schema or invocation format | A technically correct result can fail organizer validation. | Keep input/output adapters isolated; confirm official guidance; do not hardcode guessed rules. |
| Keyword evidence is mistaken for proof | Can lead to unsupported or overestimated TRL. | Add negation/modality checks, source citations, cautious fallback, and hand-reviewed regression examples. |
| Stale metrics or benchmark claims | Can undermine trust and potentially violate data constraints. | Remove or label unverified claims; publish only reproducible results with traceable data and scripts. |
| Test environment is incomplete | A green-looking repository may fail on a fresh machine. | Install dependencies in a clean environment; run and record the actual test suite. |
| Fake or rule-generated debate appears genuine | Misrepresents a core product promise. | Label it accurately; implement a real bounded debate later, or omit debate from the prototype demo. |
| Last-minute UI expansion | Can take time away from a reliable inference package. | Treat the web UI as optional until the end-to-end CLI release gate passes. |
| Dependency/license incompatibility | Can cause submission failure or redistribution problems. | Verify the exact pinned package set and licenses in the final bundle. |

---

## 6. Daily Progress Log Template

Copy this section for each work day.

```markdown
### YYYY-MM-DD — [phase]

**Goal:**

**Completed:**
- [ ]

**Evidence / commands run:**
- 

**Test results:**
- 

**Blockers / unknowns:**
- 

**Next action:**
- 
```

---

## 7. Final Release Notes Checklist

- [ ] Exact commit SHA and submission artifact recorded.
- [ ] Clean install and CLI commands documented.
- [ ] Supported inputs and known limitations documented.
- [ ] Output schema provenance documented (official or internal).
- [ ] Tests and smoke checks actually run; results recorded.
- [ ] Metrics are traceable, reproducible, and not based on prohibited or synthetic labels.
- [ ] Agent/debate behavior is described honestly.
- [ ] No secrets, external API dependencies, or unapproved network calls in the standalone package.
- [ ] Final submission freeze completed before **November 15, 2026, 23:59 IST**, subject to confirmation against the latest official organizer instructions.
