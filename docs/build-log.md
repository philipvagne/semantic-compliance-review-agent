# Build Log

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
