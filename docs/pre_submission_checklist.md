# Argus — Pre-Submission Verification Checklist

**Competition:** Techfest 2026–27 · 2nd APCTT Hackathon 2026  
**Canonical repository:** Anish1302D/Argus  
**Base branch:** main  
**Stabilization branch:** fix/argus-pre-submission-stabilization  
**Submission target:** 15 Nov 2026, 23:59 IST  
**Submission bundle:** submission/

---

## 1. Verification status

The supplied read-only audit was performed against the predecessor TRL Debate Engine codebase at 15 Nov 2026, 01:21 IST. It reported 38/38 existing tests passing before the stabilization changes described below.

That result is a **baseline only**. It is not a test result for the current Argus stabilization branch. Re-run all checks against the final commit before submission and record the exact commit SHA, environment, command, and output.

## 2. Changes made on the Argus stabilization branch

| Area | Change | Source status | Runtime verification |
| --- | --- | --- | --- |
| Frontend interaction | Inactive navigation scrim no longer intercepts pointer events; active scrim remains interactive | Committed | Pending browser regression run |
| Evidence mining | Candidate milestones with nearby explicit negation are filtered | Committed | Pending test run and sample assessment |
| ML regression coverage | Added tests for negated flight, absent lab/breadboard milestones, positive flight, and postposed negation | Committed | Pending test run |
| Standalone bundle | Mirrored negation-aware feature extraction into submission package | Committed | Pending isolated CLI run |
| CORS | Disabled credentialed CORS while wildcard origins remain configured | Committed | Pending API test |
| API concurrency | CPU-bound sample/text/file assessment handlers are synchronous FastAPI handlers and can run in its threadpool | Committed | Pending concurrent request test |
| Product identity | Browser, API metadata, package metadata, README, PRD, CLI docs, and submission docs use Argus | Partially committed | Pending repository-wide branding scan |

## 3. Mandatory pre-submission gates

### Functional verification

- [ ] Backend starts from a clean environment using the documented command.
- [ ] Frontend loads without console errors.
- [ ] Desktop navigation, sample buttons, upload control, toggles, filters, and dialogs accept mouse and keyboard input.
- [ ] Mobile navigation opens and closes correctly; active scrim closes the drawer while inactive scrim does not block the page.
- [ ] Health endpoint returns the expected service status.
- [ ] TRL ladder endpoint returns all nine levels.
- [ ] Sample documents endpoint returns the documented examples.
- [ ] Text assessment succeeds for a valid technical document.
- [ ] PDF, TXT, and MD uploads work.
- [ ] Empty input and unsupported file types return controlled errors.
- [ ] Strict security mode rejects the supplied prompt-injection sample.
- [ ] Assessment history and theme preference persist as designed.
- [ ] Evidence references, criteria, and advancement recommendations render without broken data.

### Negation and assessment regression checks

- [ ] Hypersonic TPS does not award TRL 7 solely from the negated flight-demonstration phrase; expected result is TRL 6.
- [ ] The malicious injection sample does not receive TRL 3 or TRL 4 from milestones explicitly stated as not performed; expected result is TRL 1.
- [ ] Positive flight-demonstration evidence remains detectable.
- [ ] Negated milestones do not inflate the 25-dimensional feature vector or highest-matched-TRL feature.
- [ ] Quantum Cascade sample result is checked against its expected TRL 4.
- [ ] CubeSat sample result is checked against its expected TRL 9.
- [ ] Every mismatch is investigated; do not tune rules merely to force sample labels.

### Security and reliability

- [ ] CORS configuration is verified in the running API.
- [ ] Upload size limits and file-content validation are reviewed before exposing the API beyond localhost.
- [ ] Temporary upload files are cleaned up on success and failure.
- [ ] Error responses do not leak secrets or stack traces.
- [ ] No private API keys, tokens, or credentials are committed.
- [ ] CPU-heavy assessment requests do not starve health checks under concurrent load.

### Automated quality checks

- [ ] Full pytest suite passes on the final branch commit.
- [ ] Frontend interaction regression test passes.
- [ ] Linting passes using the installed/configured linter.
- [ ] Production/startup command succeeds from a clean environment.
- [ ] The final test count and output are recorded without rounding or assumptions.

### Submission bundle

- [ ] Regenerate submission/ from the final source using scripts/package_submission.py.
- [ ] Confirm the negation-aware implementation is present in the generated bundle.
- [ ] Install only the bundle's declared requirements in a clean environment.
- [ ] Run submission/run_inference.py on a sample input.
- [ ] Verify output JSON schema and exit codes.
- [ ] Verify air-gapped execution with network access disabled.
- [ ] Confirm dependency licenses against the competition rules.
- [ ] Record SHA-256 hashes of the submitted bundle and final source commit.

## 4. Known implementation boundaries

The current release must be described accurately:

- Evidence mining is rule/regex based and does not provide full natural-language understanding.
- Negation handling is a bounded local heuristic, not a general semantic NLP model.
- The Optimist/Skeptic/Referee transcript is deterministic review synthesis, not three independent autonomous LLM agents.
- Hybrid BM25/vector retrieval is not implemented in the active assessment path.
- A dedicated Next.js application and Supabase persistence are not part of the active implementation.
- The LightGBM training path must remain disabled for competition inference until permitted, verified labelled training data is available.
- Confidence values are heuristic and must not be described as calibrated probabilities.

## 5. Release discipline

- [ ] All work is committed on a feature branch created from main.
- [ ] No direct commits are made to main.
- [ ] Review the branch diff for unrelated files and accidental secrets.
- [ ] Open a pull request into main only after all P0/P1 checks pass.
- [ ] Keep the submission source and package bundle aligned.
- [ ] Freeze the exact verified commit; do not make untested changes after the freeze.

**Release rule:** A change is complete only when its implementation, relevant regression test, and verification result are all recorded. A commit alone is not proof that a feature works.
