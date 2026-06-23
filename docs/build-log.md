# Build Log

## 2026-06-23

### Phase 7A - Clean Copy Generation

Completed:
- Added `src/clean_copy_writer.py` to generate separate clean-copy artifacts
  under `output/` without modifying the original input file.
- Added `--clean-copy` to `src/main.py` so clean-copy generation is explicit
  and opt-in.
- Limited clean-copy application to conservative exact replacements only when
  source text, suggested replacement, and uniqueness checks all pass.
- Skipped ambiguous or missing replacements safely and surfaced the skipped
  reasons in the audit report.
- Updated `src/report_writer.py` so clean-copy runs include a summary with the
  generated path, applied count, skipped count, and skipped reasons.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/realistic_sample.py --backend deterministic --clean-copy`.
- Ran `python -m src.main examples/realistic_sample.py --backend deterministic`.

Result:
- `output/realistic_sample-clean-copy.py` was generated as a separate artifact.
- The deterministic clean-copy run applied 2 conservative replacements and
  skipped 1 ambiguous or missing replacement safely.
- The original `examples/realistic_sample.py` file remained unchanged.
- Default deterministic behavior without `--clean-copy` still worked.

### Phase 8B.4J - Realistic File Validation

Completed:
- Added `examples/realistic_sample.py` as a more natural user-style review
  target with mostly normal code and comments plus three intentional reviewable
  issues across security, internal codename exposure, and professionalism.
- Kept the realistic sample outside `evaluation/cases/` so the committed
  10-case evaluation dataset remains the formal benchmark.
- Documented the realistic sample as usability and demo-style validation
  rather than a scored benchmark artifact.
- Kept the recommended live Gemini command aligned with the project's
  reliability-sensitive model choice: `gemini-2.5-pro`.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/realistic_sample.py --backend deterministic`.
- Attempted `python -m src.main examples/realistic_sample.py --backend gemini`
  with `GEMINI_MODEL=gemini-2.5-pro`.

Result:
- The deterministic review completed and produced
  `output/realistic_sample-audit-report.md`.
- The deterministic run surfaced three findings on the realistic sample:
  security risk, internal codename exposure, and professionalism risk.
- The Gemini Pro run could not proceed in this environment because no
  `GOOGLE_API_KEY` or `GEMINI_API_KEY` was configured.

### Phase 8B.4I - Production Model Validation

Completed:
- Updated `src/agent_review.py` so normal Gemini review and evaluation runs can
  use the shared `GEMINI_MODEL` environment variable while keeping the default
  model selection at `gemini-2.5-flash`.
- Updated `evaluation/run.py` so committed evaluation result artifacts include
  the selected model in addition to the backend.
- Kept `evaluation/diagnose_gemini.py` support for explicit `--model`
  overrides while aligning its default behavior with the shared project model
  selection.
- Documented the full reliability investigation path, including intermittent
  Flash `503 UNAVAILABLE` failures, API-key-variable checks, the fixed ADK
  event-loop lifecycle issue, bounded transient retries, and prior manual
  evidence that `gemini-2.5-pro` completed 5/5 diagnostic cycles and that the
  10 Gemini evaluation cases passed when collected one by one.
- Recorded the current model decision: keep Flash as the default model, but
  recommend Pro for reliability-sensitive Gemini validation and demo use.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --case security_python`.
- Checked local environment variable availability for `GOOGLE_API_KEY`,
  `GEMINI_API_KEY`, and `GEMINI_MODEL`.
- Could not run credentialed Gemini Pro diagnostics or full Gemini evaluation
  in this environment because no Gemini credentials were set.

Result:
- The repository now supports shared Gemini model selection across diagnostics,
  normal review, and evaluation without changing prompts, extraction,
  matching, or dataset content.
- The current project recommendation is explicit: `gemini-2.5-pro` is the
  preferred reliability-sensitive production candidate, while
  `gemini-2.5-flash` remains the default model because latency and cost
  tradeoffs still matter.

### Phase 8B.4H - Gemini Model Stability Comparison

Completed:
- Updated `src/agent_review.py` so Gemini model selection is configurable while
  preserving the existing default model name of `gemini-2.5-flash`.
- Kept the standard CLI review path unchanged when no model override is
  supplied.
- Extended `evaluation/diagnose_gemini.py` with an optional `--model`
  override, selected-model reporting, and clearer backend-path reporting for
  direct and ADK-backed Gemini checks.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.diagnose_gemini --repeat 1`.

Result:
- The repository can now compare Gemini stability across model names during
  diagnostics without changing prompts, extraction behavior, evaluation
  matching, or the default review configuration.

### Phase 8B.4G - Gemini Transient Retry Handling

Completed:
- Added bounded retry handling in `src/agent_review.py` for transient
  Gemini-backed provider failures only.
- Configured the retry path for up to three total attempts with short
  exponential backoff delays of 1 second and 2 seconds.
- Limited retries to clearly transient Gemini errors such as `503`,
  `UNAVAILABLE`, and `high demand` messages.
- Kept deterministic review behavior unchanged.
- Kept validation/schema failures out of the transient provider retry path so
  non-transient failures still fail clearly.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --case security_python`.

Result:
- The Gemini-backed review path now has small, bounded transient retry
  handling without changing prompts, extraction behavior, evaluation matching,
  or dataset content.
- Provider-side failures may still remain visible after all retry attempts,
  which is expected for this phase.

### Phase 8B.4F - ADK Event Loop Lifecycle Fix

Completed:
- Updated `src/agent_review.py` so the ADK `InMemoryRunner` is created inside
  each active review call instead of being cached across repeated
  `asyncio.run(...)` event loops.
- Kept backend selection, credential validation, prompts, extraction behavior,
  and evaluation matching unchanged.
- Removed the unsafe cross-loop runner reuse introduced in the earlier
  optimization pass.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --case security_python`.

Result:
- The review path now avoids reusing a loop-bound ADK runner across closed
  event loops.
- Provider-side Gemini `503 UNAVAILABLE` behavior remains out of scope for this
  phase and unchanged.

### Phase 8B.4E - Gemini Reliability Investigation

Completed:
- Expanded `evaluation/diagnose_gemini.py` with safe API-key configuration
  reporting that shows whether `GOOGLE_API_KEY` and `GEMINI_API_KEY` are set
  and which variable would be used without printing the key value.
- Added a reminder that the selected API key should be restricted to the
  Gemini API / `generativelanguage.googleapis.com`.
- Added per-test elapsed-duration reporting plus concise PASS / FAIL, preview,
  error type, and short error message output.
- Added `--repeat` support so the same diagnostic set can be observed across
  multiple fresh cycles without adding retries.
- Added `--delay-seconds` support so repeated diagnostic cycles can be paced
  without delaying before the first cycle.
- Added per-test PASS / FAIL summary counts across repeated cycles.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.diagnose_gemini --repeat 1`.
- Ran `python -m evaluation.diagnose_gemini --repeat 2 --delay-seconds 1`.
- Ran `python -m evaluation.diagnose_gemini --repeat 0`.
- Ran `python -m evaluation.diagnose_gemini --repeat 1 --delay-seconds -1`.

Result:
- The repository now has a more useful Gemini reliability-investigation tool
  without changing production prompts, ADK usage, evaluation matching, or
  runtime review behavior.

### Phase 8B.4D - ADK Runner Reuse Optimization

Completed:
- Updated `src/agent_review.py` to cache the ADK `InMemoryRunner` by active
  backend instead of rebuilding it on every review call.
- Reused the cached runner when `configure_backend()` is called again with the
  same backend.
- Invalidated and rebuilt the cached runner when switching between Gemini and
  deterministic backends.
- Added a fail-clear guard so review raises an explicit error if no configured
  cached runner is available.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --case security_python`.

Result:
- The Agent Review runtime now avoids unnecessary ADK runner reconstruction for
  repeated reviews while preserving the same prompts, schemas, extraction
  behavior, evaluation matching, and backend boundaries.

## 2026-06-22

### Phase 8B.4C - Gemini Backend Path Diagnosis

Completed:
- Added `evaluation/diagnose_gemini.py`.
- Implemented a direct `google.genai` smoke test with a minimal prompt.
- Implemented a direct `google.genai` realistic review-prompt test using the
  committed `security_python.py` evaluation case.
- Implemented an ADK-backed review-path test that exercises the existing
  production Gemini review boundary on the same evaluation case.
- Added concise PASS / FAIL reporting plus short previews or error summaries.
- Added an interpretation summary that points toward general Gemini
  availability, ADK-path isolation, realistic prompt complexity, or
  intermittent behavior depending on the observed pattern.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.diagnose_gemini`.

Result:
- The repository now includes a focused Gemini path-diagnosis command without
  changing production backend behavior, prompts, extraction, or evaluation
  data.

### Phase 8B.4B - Evaluation Case Selection

Completed:
- Added `--case` support to run exactly one evaluation case by case ID or file
  stem.
- Added `--cases` support to run multiple evaluation cases by comma-separated
  case IDs or file stems.
- Made `--case` and `--cases` mutually exclusive.
- Kept backend-specific result files while marking selected-case runs as
  partial evaluation runs in the generated report.
- Kept matching, scoring, dataset loading, and expected-output validation
  unchanged.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.run --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --case security_python`.
- Ran `python -m evaluation.run --backend deterministic --cases security_python,security_javascript`.
- Ran `python -m evaluation.run --backend deterministic --case does_not_exist`
  and verified clear failure behavior.
- Ran `python -m evaluation.run --backend deterministic --case security_python --cases security_javascript`
  and verified mutual-exclusion validation.
- Did not require a full Gemini run in this environment.

Result:
- The evaluation runner now supports targeted single-case and selected-case
  runs for both deterministic and Gemini backends without changing scoring or
  the dataset.

### Phase 8B.4A - Gemini Evaluation Rate-Limit Handling

Completed:
- Added optional `--delay-seconds` support to `evaluation/run.py`.
- Kept the default delay at `0` seconds so deterministic runs remain fast by
  default.
- Applied the delay only between evaluation cases, never before the first case.
- Added clear CLI validation so negative delay values fail immediately.
- Kept evaluation matching, scoring, dataset loading, and result formatting
  unchanged.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.run --backend deterministic`.
- Ran `python -m evaluation.run --backend deterministic --delay-seconds 0`.
- Ran `python -m evaluation.run --backend deterministic --delay-seconds -1`
  and verified that the CLI fails clearly.
- Ran `python -m evaluation.run --backend gemini --delay-seconds 15` and
  verified CLI parsing plus existing fail-clear Gemini credential behavior.

Result:
- Free-tier Gemini users now have a simple pacing control for evaluation runs
  without changing review behavior, matching rules, or evaluation scoring.

### Phase 8B.4 - Gemini Evaluation Snapshot

Completed:
- Extended `evaluation/run.py` so the same evaluation runner now accepts both
  `--backend deterministic` and `--backend gemini`.
- Kept the expected-output loading rules and matching logic unchanged so the
  deterministic and Gemini paths remain directly comparable.
- Added backend-specific result-file generation behavior so Gemini runs target
  `evaluation/results/gemini-results.md`.
- Kept Gemini snapshot notes separate from deterministic repeatability notes in
  the generated evaluation report content.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.run --backend deterministic`.
- Ran `python -m evaluation.run --backend gemini`.
- Verified that deterministic evaluation still works unchanged.
- Verified that the Gemini path fails clearly when credentials are not present.

Result:
- The evaluation runner now supports the Gemini backend without changing agent
  behavior, prompts, matching rules, or the dataset.
- A committed Gemini results snapshot could not be generated in this shell
  session because `GOOGLE_API_KEY` and `GEMINI_API_KEY` were both unavailable.

### Phase 8B.3 - Deterministic Runner and Metrics

Completed:
- Added `evaluation/run.py` as the first working evaluation execution path for
  the deterministic backend only.
- Implemented strict loading of all files from `evaluation/cases/` and matching
  expected JSON files from `evaluation/expected/`.
- Implemented simple and explainable expected-to-actual matching using category
  plus target-text or line-range checks, with optional suggested-replacement
  requirements.
- Calculated TP, FP, FN, precision, and recall across the committed dataset.
- Generated `evaluation/results/deterministic-results.md` as a human-readable
  committed evaluation artifact.
- Updated status docs so Phase 8B.3 is recorded as complete and Phase 8B.4 is
  the next implementation slice.

Tested:
- Ran `python -m compileall src evaluation`.
- Ran `python -m evaluation.run --backend deterministic`.
- Verified that all 10 evaluation cases were processed.
- Verified that concise per-case progress and final precision/recall summary
  were printed to the console.
- Verified that `evaluation/results/deterministic-results.md` was generated.

Result:
- The repository now has a deterministic evaluation runner and metrics output
  without changing the normal runtime review pipeline or adding Gemini
  evaluation behavior.

### Phase 8B.2 - Evaluation Dataset

Completed:
- Added 10 small evaluation input files under `evaluation/cases/`.
- Added 10 matching expected-output JSON files under `evaluation/expected/`
  using the approved Phase 8A schema.
- Covered clean behavior, documentation false-positive handling, security
  risks, internal codename exposure, professionalism risks, and suggested
  replacement coverage.
- Included representative supported-file coverage across Python,
  JavaScript-family, HTML, Markdown, and TypeScript.
- Updated status docs so Phase 8B.2 is recorded as complete and Phase 8B.3 is
  the next implementation slice.

Tested:
- Dataset-only task; no runtime code, evaluation runner, or results generation
  behavior was changed.
- Verified that `evaluation/results/` remains empty and that no runner or
  metrics implementation was added in this slice.

Result:
- The repository now contains a small, credible evaluation dataset and
  matching expectations without implementing execution or scoring logic.

### Phase 8B.1 - Evaluation Foundation

Completed:
- Added `evaluation/__init__.py` to establish the evaluation package root.
- Added `evaluation/README.md` describing evaluation purpose, directory roles,
  backend separation, result policy, and the next Phase 8B slices.
- Ensured `evaluation/results/` exists and confirmed `evaluation/cases/` and
  `evaluation/expected/` remain present.
- Updated status docs so the repository now reflects Phase 8B.1 as complete and
  Phase 8B.2 as the next implementation slice.

Tested:
- Foundation-only task; no runtime code or evaluation runner behavior was
  changed.
- Verified that no evaluation cases, expected JSON files, or result artifacts
  were added in this slice.

Result:
- The repository now has the required evaluation directory scaffolding without
  implementing the evaluation harness or changing runtime behavior.

### Phase 8A - Evaluation Design

Completed:
- Replaced the earlier lightweight evaluation notes with a fuller approved
  Phase 8 evaluation design.
- Documented the evaluation philosophy that semantic correctness matters more
  than exact wording matches.
- Documented separate evaluation purposes for the deterministic and Gemini
  backends instead of combining them into one score.
- Documented representative supported-file coverage, case-type targets,
  matching rules, severity handling, metrics, and expected JSON structure.
- Documented the proposed `evaluation/cases`, `evaluation/expected`, and
  `evaluation/results` artifact layout.
- Recorded the policy that evaluation result artifacts should be committed as
  capstone evidence.
- Updated project status docs so Phase 8A is recorded as complete and Phase 8B
  can begin as the next implementation step.

Tested:
- Documentation-only task; no runtime code or evaluation harness behavior was
  changed.
- Re-read README, architecture, decisions, guardrails, evaluation, course
  concepts, workflow guidance, and the project plan to keep the evaluation
  design aligned with the current pipeline boundaries.

Result:
- The repository now contains a credible, repeatable evaluation design without
  claiming that evaluation runtime support already exists.

### Phase 6.97 - Submission Readiness Refinement

Completed:
- Updated the README concept framing so the ADK architecture section now
  explicitly acknowledges supported multi-language extraction coverage without
  overstating the MVP scope.
- Updated the video writeup skeleton so the demo plan explicitly includes one
  non-Python review example and report generation.
- Added a brief future-improvements note to the video writeup skeleton.

Tested:
- Documentation-only refinement; no runtime code or behavior was changed.
- Re-checked the surrounding docs to keep the wording aligned with the current
  implemented file support and roadmap.

Result:
- Submission-facing docs now present the implemented multi-language support
  more clearly while preserving the same architecture and scope boundaries.

### Phase 6.97 - Submission Readiness Foundation

Completed:
- Added a Mermaid architecture diagram to `README.md` showing supported input
  types, the extraction pipeline, config inputs, backend branching, structured
  findings, and the advisory Markdown report output.
- Added a `Key Concepts Demonstrated` section to `README.md` covering ADK agent
  architecture, security guardrails, and the agent-skills/CLI workflow story.
- Added `docs/video-writeup-skeleton.md` as planning notes for the capstone
  writeup and short demo video.
- Reviewed all current demo example files and confirmed they were already clear
  enough for submission-oriented documentation.
- Updated status docs so Phase 6.97 is recorded without claiming new runtime
  capabilities.

Tested:
- Documentation-only task; no runtime code or extraction behavior was changed.
- Re-read the current examples and implementation-facing docs to keep the new
  presentation material aligned with actual supported behavior.

Result:
- The repository now explains the architecture and capstone concept mapping
  more clearly for reviewers without expanding product scope.
- Phase 7 remains the next implementation step.

### Phase 6.96C - Markdown Extraction

Completed:
- Added `src/extractors/markdown_extractor.py`.
- Expanded `src/extractors/__init__.py` and `src/text_extractor.py` so `.md`
  now uses a dedicated Markdown extractor while `.py`, JavaScript-family, and
  HTML files keep their existing paths.
- Implemented extraction for Markdown headings, paragraphs, list items, and
  blockquotes.
- Classified TODO / FIXME / NOTE blocks after removing Markdown block syntax.
- Excluded fenced code blocks entirely for both backtick and tilde fences.
- Ignored Markdown table rows and separator-only lines in this MVP.
- Added `examples/sample_input.md` for manual end-to-end verification.
- Verified that `README.md` now runs successfully because Markdown support is
  implemented.

Tested:
- Ran `python -m compileall src`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m src.main examples/sample_input.js --backend deterministic`.
- Ran `python -m src.main examples/sample_input.html --backend deterministic`.
- Ran `python -m src.main examples/sample_input.md --backend deterministic`.
- Ran `python -m src.main README.md --backend deterministic`.

Result:
- Python extraction still works.
- JavaScript-family extraction still works.
- HTML extraction still works.
- Markdown files now flow through the existing CLI, context, review, and report
  pipeline without changing downstream components.
- The required Phase 6.96 extractor scope is now implemented.

### Phase 6.96B - HTML Extraction

Completed:
- Added `src/extractors/html_extractor.py`.
- Expanded `src/extractors/__init__.py` and `src/text_extractor.py` so `.html`
  now uses a dedicated HTML extractor while `.py` and JavaScript-family files
  keep their existing paths.
- Implemented extraction for `<!-- -->` HTML comments only, including TODO /
  FIXME / NOTE classification when the comment starts with those markers.
- Skipped script and style contents while scanning for HTML comments so
  embedded JavaScript and CSS are not treated as HTML reviewable text.
- Added `examples/sample_input.html` for manual end-to-end verification.
- Kept Markdown unsupported so `.md` still fails clearly in this slice.

Tested:
- Ran `python -m compileall src`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m src.main examples/sample_input.js --backend deterministic`.
- Ran `python -m src.main examples/sample_input.html --backend deterministic`.
- Ran `python -m src.main README.md --backend deterministic`.

Result:
- Python extraction still works.
- JavaScript-family extraction still works.
- HTML files now flow through the existing CLI, context, review, and report
  pipeline without changing downstream components.
- Markdown extraction remains deferred to a later Phase 6.96 slice.

### Phase 6.96A - JavaScript-family Extraction

Completed:
- Added `src/extractors/__init__.py` and
  `src/extractors/javascript_extractor.py`.
- Expanded `src/text_extractor.py` so `.js`, `.ts`, `.jsx`, and `.tsx` now use
  a JavaScript-family extractor while `.py` keeps the existing Python path.
- Implemented extraction for `//` comments, `/* */` block comments, `/** */`
  JSDoc blocks, and TODO / FIXME / NOTE comment types in JavaScript-family
  files.
- Preserved existing metadata fields for extracted items, including line
  numbers, language, and surrounding context.
- Added `examples/sample_input.js` for manual end-to-end verification.
- Kept unsupported-file behavior strict so Markdown still fails clearly in this
  slice.

Tested:
- Ran `python -m compileall src`.
- Ran `python -m src.main examples/sample_input.py --backend deterministic`.
- Ran `python -m src.main examples/sample_input.js --backend deterministic`.
- Ran `python -m src.main README.md --backend deterministic`.

Result:
- Python extraction still works.
- JavaScript-family files now flow through the existing CLI, context, review,
  and report pipeline without changing downstream components.
- HTML and Markdown extraction remain deferred to later Phase 6.96 slices.

### Phase 6.95 - Multi-language Extraction Design

Completed:
- Documented the approved expansion of the Text Extractor from Python-only
  extraction to human-written text extraction across common project files.
- Recorded the approved supported file set for the next implementation phase:
  `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, and `.md`.
- Documented four extractor families:
  Python, JavaScript-family, HTML, and Markdown.
- Documented the approved dispatcher role for `src/text_extractor.py` and the
  recommended `src/extractors/` module layout for Phase 6.96.
- Documented the explicit non-goals for the upcoming implementation:
  no schema changes, no Agent Review changes, no Gemini prompt changes, no
  Report Writer changes, no evaluation additions, and no clean-copy generation.
- Updated status docs so Phase 6.95 is recorded as complete and Phase 6.96
  becomes the next implementation step.

Tested:
- Documentation-only task; no runtime code was changed.
- Re-read the current extractor entry point and shared schemas to confirm the
  approved design preserves the existing component boundaries.
- Reviewed README, project plan, architecture, decisions, and workflow-facing
  docs for consistency with the new extraction design record.

Result:
- The repository now contains an explicit approved design for multi-language
  extraction before implementation begins.
- Phase 6.96 can focus on extraction-only runtime work without reopening the
  architecture boundary.

## 2026-06-20

### Repository Foundation

Completed:
- Created local repository structure.
- Added project plan.
- Added documentation skeleton.
- Added sample audit report.
- Created public GitHub repository.
- Pushed initial foundation commit.

Next:
- Begin Phase 0.5 - ADK Feasibility Spike.

### ADK Feasibility Spike Environment

Initial attempt with Python 3.14 revealed dependency-resolution friction.

Decision:
Install Python 3.12 and create a dedicated virtual environment.

Result:
google-adk 2.3.0 successfully installed.

Status:
Proceeding with ADK validation.

### ADK Feasibility Spike Implementation

Completed:
- Removed the temporary workspace write test file.
- Added a minimal ADK spike agent under `src/`.
- Added a single custom tool: `load_sensitive_terms()`.
- Added a structured `ReviewFinding` schema.
- Added a CLI entry point that accepts one review string and prints JSON.
- Verified the spike with the required example input.

Result:
- ADK runtime flow works locally for this spike.
- Tool calling works.
- Structured output parses into the project schema.

Known limitation:
- This spike uses a deterministic local test model inside ADK, so it validates
  ADK wiring and tool orchestration but does not yet validate live Gemini
  credentials or provider behavior.

### Phase 1.5 - MVP Workflow Design

Completed:
- Documented the MVP workflow from CLI through report generation.
- Added component contracts for CLI, file reader, text extractor, context loader, agent review, report writer, clean copy writer, and evaluation.
- Documented expected failure behavior for each component.
- Defined the ADK review boundary as a swappable seam.

Result:
- Phase 1.5 workflow design is documented before implementation begins.
- Component responsibilities are clearer for future phase work.

### Phase 1.75 - Foundation Review

Completed:
- Reviewed repository structure against the current implementation.
- Reviewed README, AGENTS.md, Codex workflow guidance, architecture docs, and build log alignment.
- Reviewed the ADK feasibility spike for minimal scope, tool use, orchestration, and structured output.
- Identified documentation mismatches and one stray tracked artifact before Phase 2.

Result:
- No blocker was found in the ADK spike itself.
- Documentation alignment cleanup was required before Phase 2.

### Phase 1.76 - Alignment Cleanup

Completed:
- Deleted the stray tracked root artifact left from an earlier diff capture.
- Updated the project plan to mark completed phases through Phase 1.75.
- Updated the build log and README to reflect current status and the next phase.
- Tightened the documentation sync rule in AGENTS.md and Codex workflow guidance.

Result:
- Repository state and documentation now match the actual completed foundation work.
- Phase 2 is ready to begin.

### Phase 2 - File Reader

Completed:
- Added a `FileContent` schema for file metadata plus raw text.
- Implemented `src/file_reader.py` with a focused `read_file()` function.
- Added `FileReadError` handling for missing files, directories, permission
  issues, and non-UTF-8 content.
- Replaced the CLI entry path in `src/main.py` so it now accepts one file path
  and prints file metadata.
- Added `examples/sample_input.py` for manual testing.
- Updated Phase 2 documentation and status references.

Tested:
- Ran the CLI against `examples/sample_input.py`.
- Verified the success summary prints path, extension, line count, and
  character count.

Result:
- Phase 2 now has a real MVP input component for one-file reading.
- The implementation remains intentionally narrow and does not pull in future
  extraction, review, reporting, or evaluation behavior.

### Phase 2.5 - Text Extraction Design

Completed:
- Recorded the approved Text Extraction design before Phase 3 implementation.
- Documented the `FileContent -> Text Extractor -> ReviewableText[]` flow.
- Documented the `ReviewableText` contract fields and planned source types.
- Locked the first implementation scope to Python comments, Python docstrings,
  and TODO / FIXME / NOTE comments only.
- Explicitly deferred string literal extraction to a later controlled expansion.
- Documented failure behavior: empty list for no reviewable text, and
  `ExtractionError` only for unexpected parser/runtime failures.
- Recorded the module-level docstring requirement for major components, with
  `src/text_extractor.py` called out for Phase 3.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed status and architecture docs for consistency with the approved design.

Result:
- Phase 3 implementation now has a documented contract and clear MVP boundary.
- The repository remains unchanged at runtime while the next component design is
  now approved and recorded.

## 2026-06-21

### Phase 3 - Text Extraction

Completed:
- Added a `ReviewableText` schema for extracted human-written source text.
- Added `src/text_extractor.py` with Python-only extraction for comments,
  docstrings, and TODO / FIXME / NOTE comments.
- Added `ExtractionError` for unexpected extraction failures.
- Added the missing `pydantic` dependency to `requirements.txt`.
- Updated the CLI in `src/main.py` to read a file, run extraction, and print a
  reviewable-text summary.
- Updated `examples/sample_input.py` with comment and docstring cases for manual
  testing.
- Updated architecture and README status to reflect completed Phase 3 behavior.

Tested:
- Ran the CLI against `examples/sample_input.py`.
- Verified file-read success output, extracted item count, and per-item preview
  lines.

Result:
- Phase 3 now produces `ReviewableText[]` from Python source files within the
  approved MVP scope.
- String literal extraction, agent review, and later phases remain deferred.

### Phase 3.5 - Context Loading Design

Completed:
- Recorded the approved Context Loader design before Phase 4 implementation.
- Documented the `ReviewableText[] + config files -> Context Loader -> ReviewContext`
  flow.
- Defined the `ReviewContext` contract fields:
  `sensitive_terms`, `project_name`, `project_description`, `review_focus`,
  and `config_warnings`.
- Documented the approved config inputs:
  `config/sensitive_terms.yaml` and `config/project_context.yaml`.
- Documented failure behavior for missing files, empty files, invalid YAML, and
  invalid structure/type cases.
- Documented validation rules for `sensitive_terms.yaml` and
  `project_context.yaml`, including valid and invalid examples.
- Updated status docs so Phase 3.5 is recorded as a design step and Phase 4
  remains the next implementation phase.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed README, project plan, architecture, and workflow alignment.

Result:
- Phase 4 now has an approved Context Loader contract and failure model before
  implementation begins.
- Runtime behavior remains unchanged.

### Phase 4 - Context Loading

Completed:
- Added a `ReviewContext` schema for validated project context.
- Added `src/context_loader.py` with safe YAML loading for
  `config/sensitive_terms.yaml` and `config/project_context.yaml`.
- Added `ContextLoadError` for invalid YAML and invalid config structure/type.
- Populated both config files with safe sample values for manual testing.
- Updated the CLI in `src/main.py` to load context after text extraction and
  print a short context summary.
- Added the missing `PyYAML` dependency to `requirements.txt`.
- Updated status and architecture docs to reflect completed Phase 4 behavior.

Tested:
- Ran syntax compilation for `src/`.
- Verified context loading behavior with sample config files.
- Verified CLI summary output includes context loading details.

Result:
- Phase 4 now returns a structured `ReviewContext` object within the approved
  scope.
- Agent review, risk classification, and later phases remain deferred.

### Phase 4.5 - Agent Review Design

Completed:
- Recorded the approved Agent Review design before Phase 5 implementation.
- Documented the `ReviewableText[] + ReviewContext -> Agent Review -> Finding[]`
  flow.
- Defined the clean review boundary as
  `agent_review.review(reviewable_texts, review_context) -> list[Finding]`.
- Documented the approved `Finding` fields, categories, severity values,
  confidence values, and detection methods.
- Documented the distinction between severity and confidence so the MVP does
  not conflate them.
- Documented the TERM_MATCH confidence rule, zero-findings rule, structured
  output retry rule, and suggested replacement rule.
- Updated status docs so Phase 4.5 is recorded as a design step and Phase 5
  remains the next implementation phase.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed README, project plan, architecture, and workflow alignment.

Result:
- Phase 5 now has an approved Agent Review contract and failure model before
  implementation begins.
- Runtime behavior remains unchanged.

### Phase 5 - Agent Review

Completed:
- Added a `Finding` schema for structured review output.
- Added `src/agent_review.py` with an ADK-backed review boundary.
- Added `AgentReviewError`.
- Reused the Phase 0.5 ADK pattern with an in-process deterministic fallback
  model so local behavior works without live credentials.
- Added structured finding validation plus one retry for malformed output.
- Updated the CLI in `src/main.py` to run agent review after context loading
  and print a findings summary.
- Updated status and architecture docs to reflect completed Phase 5 behavior.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py`.
- Verified zero findings is treated as a successful review result.

Result:
- Phase 5 now converts `ReviewableText[] + ReviewContext` into structured
  `Finding[]` within the approved boundary.
- Report generation, evaluation, and clean copy generation remain deferred.

### Phase 5.1 - Optional Gemini Review Path Design

Completed:
- Recorded the approved optional Gemini backend design before implementation.
- Documented that Agent Review should support two backends:
  Gemini and Deterministic.
- Documented Gemini as the approved default backend.
- Documented Deterministic as the approved explicit offline/test backend.
- Documented CLI backend selection flags:
  `--backend gemini` and `--backend deterministic`.
- Documented the failure rule that Gemini selection must fail clearly and must
  not silently fall back to Deterministic.
- Updated status docs so Phase 5.1 is recorded as a design step and Phase 5.2
  becomes the next implementation phase.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed README, project plan, architecture, and workflow alignment.

Result:
- The Gemini backend design is now recorded without changing current Agent
  Review behavior.

### Phase 5.2 - Gemini Review Path

Completed:
- Updated `src/agent_review.py` to support explicit backend selection behind
  the existing `review(reviewable_texts, review_context)` boundary.
- Kept Gemini as the default backend and Deterministic as the explicit
  offline/test backend.
- Wired the Gemini backend through ADK using the `gemini-2.5-flash` model.
- Added startup credential validation so missing Gemini credentials fail before
  file reading, text extraction, context loading, or agent review begins.
- Updated `src/main.py` to accept `--backend gemini` and
  `--backend deterministic`.
- Updated CLI output to print which backend was used.
- Added `.env.example` entries for `GOOGLE_API_KEY` and the optional
  `GEMINI_API_KEY` alias.
- Updated status and architecture docs to reflect completed Phase 5.2
  behavior.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified missing Gemini credentials fail clearly during CLI startup.
- Verified unsupported backend values are rejected by CLI argument validation.

Result:
- Phase 5.2 now supports explicit Gemini and Deterministic review backends
  without changing the public Agent Review boundary.
- Live Gemini wiring is in place, but it was not exercised in this environment
  because Gemini credentials were not available locally.

### Phase 5.25 - Live Gemini Verification

Completed:
- Recorded the successful live verification milestone for the Gemini review
  path.
- Confirmed Gemini was used as the default backend with a valid local API key.
- Confirmed the CLI completed successfully through File Reader, Text
  Extractor, Context Loader, and Agent Review.
- Confirmed Gemini returned valid findings that parsed into the `Finding`
  schema.
- Confirmed the public
  `review(reviewable_texts, review_context) -> list[Finding]` boundary works
  with a real model.
- Confirmed live Gemini output differs materially from deterministic fallback
  output.

Verified with:
- `python -m src.main examples/sample_input.py`

Observed result:
- `Backend: Gemini`
- File Reader executed successfully
- Text Extractor executed successfully
- Context Loader executed successfully
- Agent Review executed successfully
- structured output validation succeeded
- CLI completed successfully

Observed findings:
- one `HIGH SECURITY_RISK` finding for the temporary admin password TODO
- one `LOW PROFESSIONALISM_RISK` finding for the FIXME example value comment

Result:
- The project now has a verified real semantic review path through ADK and
  Gemini.
- Phase 6 design can proceed with a documented live model verification
  milestone in place.

### Phase 6 - Report Generation Design

Completed:
- Recorded the approved Report Writer design before implementation.
- Documented the component contract:
  `FileContent + ReviewableText[] + ReviewContext + Finding[] + backend metadata -> Markdown report`.
- Documented approved report sections, including the metadata table, scan
  statistics, findings, zero-findings behavior, summary matrix, finding
  reference guide, and review philosophy.
- Documented the human-readable finding reference scheme such as `SEC-001`,
  `PRO-001`, and `CDX-001`.
- Documented overwrite behavior for existing report files.
- Documented `ReportWriteError` failure behavior for output creation and write
  failures.
- Used `examples/sample-audit-report.md` as a style reference while explicitly
  constraining the real implementation to pipeline-produced data only.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed README, project plan, architecture, workflow, and sample report
  alignment.

Result:
- Phase 6 implementation now has a documented Report Writer boundary and MVP
  output contract before coding begins.
- Runtime behavior remains unchanged.

### Phase 6.5 - Report Writer Implementation

Completed:
- Added `src/report_writer.py` with a focused Markdown-only report writer.
- Added `ReportWriteError` for output-directory, write, invalid-data, and
  unexpected report-generation failures.
- Wired the CLI in `src/main.py` so it writes a report after agent review.
- Added backend and model metadata handoff from Agent Review into Report
  Writer.
- Implemented per-category finding references such as `SEC-001` and `PRO-001`
  while preserving finding order.
- Implemented zero-findings report generation and the approved audit-status
  rule.
- Wrote reports into `output/` and overwrite existing report files without
  prompting.
- Updated status and architecture docs to reflect completed Phase 6.5
  behavior.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified the CLI writes `output/sample_input-audit-report.md`.
- Verified the generated report includes only currently available pipeline
  metadata and statistics.

Result:
- Phase 6.5 now generates one human-readable Markdown audit report from the
  existing pipeline output.
- Runtime behavior remains intentionally limited to Markdown output only.

### Phase 6.6 - Report Experience & Readability Design

Completed:
- Recorded the approved report readability and experience design before
  implementation.
- Compared the current generated report with `examples/sample-audit-report.md`
  as the primary UX reference.
- Documented the approved executive summary addition, summary matrix
  placement change, narrative finding layout, diff-style suggested replacement
  presentation, and improved zero-findings experience.
- Documented the rule that Report Writer should become a better presenter of
  findings without becoming a second reviewer.
- Documented the guardrails against inventing findings, metrics, statistics,
  or new analysis.

Tested:
- Documentation-only task; no runtime code was changed.
- Reviewed README, project plan, architecture, build log, sample report, and
  current generated report alignment.

Result:
- Phase 6.7 implementation now has a clearer readability target for report UX
  without changing the underlying review pipeline contract.
- Runtime behavior remains unchanged.

### Phase 6.7 - Report Readability Implementation

Completed:
- Updated `src/report_writer.py` to improve report readability and hierarchy
  without changing underlying finding data.
- Added a stronger Executive Summary near the top of the report.
- Moved the Audit Summary Matrix before Detailed Findings.
- Reworked finding sections into a more narrative review format.
- Added diff-style suggested replacement rendering when a suggested
  replacement exists.
- Improved zero-findings report wording so successful audits still feel
  complete.
- Improved Review Philosophy wording to align more closely with the blueprint
  report.
- Regenerated `output/sample_input-audit-report.md` with the updated report
  presentation.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified the regenerated report is easier to scan and still uses only
  current pipeline data.
- Verified zero-findings report behavior with a focused local report-writer
  test.

Result:
- Phase 6.7 now improves report readability and human usefulness without
  changing finding generation or report scope.
- Runtime behavior remains limited to Markdown report presentation only.

### Phase 6.75 - Report Polish & Humanization

Completed:
- Updated `src/report_writer.py` with small presentation polish improvements
  only.
- Humanized severity, confidence, and detection-method display values.
- Added visual indicators for severity and confidence.
- Improved single-line versus multi-line location wording.
- Improved no-suggestion wording to feel more like a professional audit report.
- Regenerated `output/sample_input-audit-report.md` with the polished report
  presentation.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified the regenerated report is more human-friendly without changing
  finding order or underlying review data.

Result:
- Phase 6.75 makes the report feel more polished and professional without
  redesigning the report or changing the review pipeline.

### Agent Review Suggested Replacement Guidance

Completed:
- Tightened Gemini Agent Review instructions so `suggested_replacement` is
  included only when a safe neutral rewrite is obvious.
- Kept `suggested_replacement` optional and preserved `null` when remediation
  remains uncertain.
- Added deterministic parity for obvious HIGH-confidence replacement cases so
  report rendering can be verified locally without live Gemini credentials.
- Regenerated `output/sample_input-audit-report.md` and verified diff-style
  replacement rendering when a replacement exists.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified the regenerated report now shows a diff block for the security TODO.
- Verified the no-suggestion message still renders when
  `suggested_replacement` is `null`.

Result:
- The review layer, not the report writer, now provides safe replacement text
  more consistently for obvious HIGH-confidence cases.

### Agent Review Detection Method Guidance

Completed:
- Tightened Gemini Agent Review instructions so `detection_method` follows the
  documented TERM_MATCH / SEMANTIC_ANALYSIS / HYBRID contract more strictly.
- Added explicit negative rules stating that HYBRID must not be used just
  because semantic reasoning was involved, a finding is severe, or a suggested
  replacement exists.
- Kept the earlier suggested-replacement guidance intact.
- Regenerated `output/sample_input-audit-report.md` after verification.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Verified the deterministic report still renders diff-style suggested
  replacements when present.
- Verified the deterministic finding continues to use
  `SEMANTIC_ANALYSIS`, which matches the documented contract because no
  configured sensitive term appears in the source text.

Result:
- The Gemini review prompt now gives much clearer detection-method boundaries
  without changing schemas, backend selection, or report-writer behavior.

### Phase 6.9A - Documentation & Submission Readiness

Completed:
- Filled `docs/security-guardrails.md` with the current safety boundaries.
- Filled `docs/course-concepts.md` with an honest implemented-versus-planned
  capstone concept mapping.
- Expanded `docs/decisions.md` with the key MVP and runtime architecture
  decisions made through Phase 6.75.
- Rewrote `README.md` as a capstone-facing project front page with honest scope,
  setup, quickstart, limitations, and roadmap guidance.
- Filled `docs/evaluation-plan.md` with a Phase 8 plan without claiming
  evaluation is already implemented.
- Updated the project plan status so the roadmap reflects the documentation
  stabilization pass before later implementation phases.

Tested:
- Documentation-only task; runtime code and generated behavior were not changed.
- Reviewed README, project plan, architecture, build log, sample output, and
  capstone-facing docs for scope and status alignment.

Result:
- The repository now tells a more accurate and professional story about the
  implemented pipeline.
- Remaining gaps are now documented more clearly instead of being implied or
  left blank.

### Phase 6.9B - Runtime Cleanup

Completed:
- Updated unsupported-file handling so non-Python inputs fail clearly instead
  of appearing as zero-finding clean audits.
- Added the missing module-level docstrings to the current CLI and shared
  schema/file-reader modules, and retained the ADK spike with its own docstring.
- Kept `ReviewFinding` in place because it is still used by the retained ADK
  spike artifact and is not dead schema code.
- Updated CLI config-warning output so warnings are printed as actual messages
  rather than only as a count.
- Expanded `.gitignore` to cover common local environment and secret files.
- Updated affected docs to reflect the fail-clear unsupported-file behavior and
  the Phase 6.9B cleanup milestone.

Tested:
- Ran syntax compilation for `src/`.
- Ran the CLI against `examples/sample_input.py --backend deterministic`.
- Ran the CLI against an unsupported non-Python file in deterministic mode and
  verified that the run fails clearly before audit generation.

Result:
- The current Python-only MVP no longer presents unsupported inputs as clean
  audit results.
- Project hygiene and CLI usability improved without expanding product scope.
