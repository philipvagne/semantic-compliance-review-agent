# Architecture

## Current Implementation Status

The repository now contains:

- a completed Phase 0.5 ADK feasibility spike
- a completed Phase 2 File Reader
- a completed Phase 3 Text Extractor for Python comments and docstrings
- an approved Phase 3.5 Context Loader design
- a completed Phase 4 Context Loader
- an approved Phase 4.5 Agent Review design
- a completed Phase 5 Agent Review
- an approved Phase 5.1 Optional Gemini Review Path design
- a completed Phase 5.2 Gemini Review Path
- an approved Phase 6 Report Generation design
- a completed Phase 6.5 Report Writer
- an approved Phase 6.6 Report Experience & Readability design
- a completed Phase 6.7 Report Readability implementation
- a completed Phase 6.75 Report Polish & Humanization
- a completed Phase 6.9B Runtime Cleanup
- an approved Phase 6.95 Multi-language Extraction Design
- a completed Phase 6.96A JavaScript-family Extraction
- a completed Phase 6.96B HTML Extraction
- a completed Phase 6.96C Markdown Extraction
- a completed Phase 6.97 Submission Readiness Foundation
- a completed Phase 8A Evaluation Design
- a completed Phase 8B.1 Evaluation Foundation
- a completed Phase 8B.2 Evaluation Dataset
- a completed Phase 8B.3 Deterministic Runner and Metrics
- the documented MVP workflow for later phases

The current runnable CLI path is the File Reader plus Text Extractor plus
Context Loader plus Agent Review plus Report Writer flow.

The next approved implementation step is Phase 8B.4: Gemini Evaluation
Snapshot.

Phase 6.97 did not change runtime behavior. It improved submission readiness by
adding clearer reviewer-facing architecture explanation, concept framing, and a
video/writeup planning scaffold.

Phase 8A also did not change runtime behavior. It documented the approved
evaluation design, expected artifacts, and measurement rules for the next
implementation step.

Phase 8B.1 also did not change runtime behavior. It added evaluation directory
scaffolding only, without cases, expected outputs, results, or runner logic.

Phase 8B.2 also did not change runtime behavior. It added the initial
evaluation cases and matching expected-output JSON files without implementing
the runner, metrics, or results generation.

Phase 8B.3 did not change the normal review CLI pipeline. It added a separate
deterministic evaluation runner under `evaluation/run.py`, simple expected
finding matching, TP / FP / FN and precision / recall calculation, and a
committed Markdown results artifact under `evaluation/results/`.

Phase 8B.4 extends that separate evaluation runner so it can execute the same
dataset against the Gemini backend using the same matching logic. This still
does not change the normal review CLI pipeline.

Phase 8B.4A adds optional pacing between evaluation cases so Gemini free-tier
users can slow the evaluation runner without changing scoring, matching, or
dataset behavior.

Phase 8B.4B adds optional case selection so the same evaluation runner can
execute one case or a small subset without changing scoring, matching, or
dataset behavior.

## Implemented Flow

User
-> CLI
-> File Reader
-> Text Extractor
-> Context Loader
-> Agent Review
-> Report Writer
-> Console Summary

The current CLI accepts one source file path, reads it as UTF-8, extracts
reviewable text from Python, JavaScript-family, HTML, and Markdown source
files, loads review context from YAML config files, reviews the extracted text
through the Agent Review boundary, writes one Markdown audit report, and
prints a console summary of the extracted items, loaded context, findings, and
report path.

If the file type is unsupported, the CLI now fails clearly before review and no
audit report is generated.

## ADK Spike Status

The ADK spike remains in the repository as a narrow feasibility artifact.

Implemented in Phase 0.5:

- one ADK agent
- one custom tool
- one structured finding schema
- local deterministic orchestration validation

Not part of the current runtime path:

- report generation
- evaluation
- clean copy generation
- repository-wide scanning

## MVP Workflow v1

The MVP target remains:

> One file in -> One report out.

Planned workflow:

User
-> CLI
-> File Reader
-> Text Extractor
-> Context Loader
-> Agent Review
-> Report Writer
-> CLI Summary

The first MVP does not include:

- repository-wide scanning
- web UI
- database
- authentication
- automatic source modification
- multi-agent architecture

## Component Contracts

## CLI

Input:

- Path to a single source code file
- Optional future flags

Output:

- Console summary
- Exit code

On Failure:

- Prints clear error message
- Exits with non-zero status

Responsibility:

- Coordinate the current file-read workflow
- Validate command usage
- Display final results

Does NOT:

- Extract text
- Review content
- Generate findings

## File Reader

Input:

- Path to source file

Output:

FileContent

- path
- filename
- extension
- raw_text
- line_count

On Failure:

Raises FileReadError

Examples:

- Missing file
- Permission denied
- Directory passed instead of file
- Non-UTF-8 content

Responsibility:

- Read one source file safely
- Return raw text and basic metadata

Does NOT:

- Extract comments
- Call agent
- Generate reports
- Scan repositories

## Text Extractor

Input:

- FileContent

Output:

List[ReviewableText]

Fields:

- id
- source_type
- text
- line_start
- line_end
- language
- surrounding_context

Planned source types:

- COMMENT
- DOCSTRING
- TODO
- FIXME
- NOTE
- STRING_LITERAL

On Failure:

- Raises ExtractionError for unsupported file types
- Returns an empty list if no reviewable text exists in a supported file type
- Raises ExtractionError only for unexpected parser/runtime failures
- No reviewable text is not an error

MVP scope decision for first implementation:

- Support Python comments
- Support Python docstrings
- Support TODO / FIXME / NOTE comments
- Do not implement string literal extraction in the first implementation
- Fail clearly for unsupported file types instead of producing a zero-finding report

Reason:

- Comments and docstrings are the core promise
- String literals add complexity and higher misclassification risk
- String literal extraction should be added later as a controlled expansion

Phase 6.95 approved expansion design:

- Keep the pipeline architecture unchanged:
  `File Reader -> Text Extractor -> Context Loader -> Agent Review -> Report Writer`
- Expand only the Text Extractor component in the next implementation phase
- Treat the problem as human-written text extraction across common project
  files, not full language parsing
- Keep `FileContent`, `ReviewableText`, and `Finding` unchanged
- Keep Agent Review, Gemini prompt behavior, Report Writer, Context Loader, and
  File Reader unchanged

Approved extractor families for Phase 6.96:

- Python extractor for `.py`
  - reviewable text: comments, docstrings, TODO / FIXME / NOTE comments
  - behavior: keep current extraction behavior
- JavaScript-family extractor for `.js`, `.ts`, `.jsx`, `.tsx`
  - reviewable text: `//` comments, `/* */` block comments, `/** */` JSDoc,
    and TODO / FIXME / NOTE comments
  - do not parse: strings, imports, object keys, JSX visible text, or
    executable code
  - `.jsx` and `.tsx` remain comment-only in the MVP
- HTML extractor for `.html`
  - reviewable text: `<!-- -->` comments only
  - do not parse: visible page text, attributes, script contents, style
    contents, or meta tags
- Markdown extractor for `.md`
  - reviewable text: headings, paragraphs, list items, and blockquotes
  - granularity: one heading, paragraph, list item, or blockquote becomes one
    `ReviewableText` item
  - exclude fenced code blocks from extraction
  - retain inline code spans inside surrounding prose items

Approved dispatcher design:

- `src/text_extractor.py` remains the public entry point and dispatcher
- planned extension mapping:
  - `.py -> Python extractor`
  - `.js -> JavaScript-family extractor`
  - `.ts -> JavaScript-family extractor`
  - `.jsx -> JavaScript-family extractor`
  - `.tsx -> JavaScript-family extractor`
  - `.html -> HTML extractor`
  - `.md -> Markdown extractor`
- unsupported file types should continue to fail clearly

Recommended module layout for Phase 6.96:

- `src/extractors/__init__.py`
- `src/extractors/python_extractor.py`
- `src/extractors/javascript_extractor.py`
- `src/extractors/html_extractor.py`
- `src/extractors/markdown_extractor.py`
- `src/text_extractor.py` as dispatcher

Responsibility:

- Preserve line numbers
- Preserve source type
- Preserve surrounding context
- Extract comments
- Extract TODO/FIXME notes
- Extract reviewable human-written text

Does NOT:

- Classify risk
- Call ADK
- Assign severity
- Generate findings
- Generate reports
- Modify source files

Phase 3 implementation note:

- `src/text_extractor.py` now includes the required module-level docstring
- The implementation uses tokenization for comments and AST parsing for
  docstrings so line numbers remain traceable without touching executable code
- unsupported non-Python inputs now fail clearly with a message that lists the
  current supported file type and states that no audit was performed

Phase 6.96A implementation note:

- `src/text_extractor.py` now dispatches `.js`, `.ts`, `.jsx`, and `.tsx` to
  `src/extractors/javascript_extractor.py`
- the JavaScript-family extractor scans only comment surfaces:
  `//`, `/* */`, and `/** */`
- `.js` and `.jsx` items use `language="javascript"`
- `.ts` and `.tsx` items use `language="typescript"`
- unsupported file types still fail clearly
- `.html` and `.md` extraction remain unimplemented in this slice

Phase 6.96B implementation note:

- `src/text_extractor.py` now dispatches `.html` to
  `src/extractors/html_extractor.py`
- the HTML extractor scans only `<!-- -->` comment surfaces
- script and style contents are skipped while scanning for HTML comments
- HTML reviewable items use `language="html"`
- `.md` extraction remains unimplemented in this slice
- unsupported file types still fail clearly

Phase 6.96C implementation note:

- `src/text_extractor.py` now dispatches `.md` to
  `src/extractors/markdown_extractor.py`
- the Markdown extractor scans headings, paragraphs, list items, and
  blockquotes
- fenced code blocks are excluded entirely, including triple-backtick and
  triple-tilde fences
- Markdown table rows are ignored in this MVP
- Markdown reviewable items use `language="markdown"`
- the required Phase 6.96 extractor families are now implemented

Example design input:

```python
# TODO: remove temporary admin password before production

def login():
    """Authenticate user against internal Project Titan service."""
    pass
```

Example design output:

```json
[
  {
    "source_type": "TODO",
    "text": "TODO: remove temporary admin password before production",
    "line_start": 1,
    "line_end": 1,
    "language": "python"
  },
  {
    "source_type": "DOCSTRING",
    "text": "Authenticate user against internal Project Titan service.",
    "line_start": 4,
    "line_end": 4,
    "language": "python"
  }
]
```

## Context Loader

Input:

- `config/sensitive_terms.yaml`
- `config/project_context.yaml`

Output:

ReviewContext

- sensitive_terms
- project_name
- project_description
- review_focus
- config_warnings

On Failure:

- Missing config file -> warn and continue with empty/default context values
- Empty config file -> warn and continue with empty/default context values
- Invalid YAML -> raise ContextLoadError and stop the CLI run
- Invalid structure/type -> raise ContextLoadError and stop the CLI run
- Missing optional fields -> allowed; use default values

Validation rules:

For `config/sensitive_terms.yaml`:

- Valid:

```yaml
sensitive_terms:
  - Project Titan
  - Falcon
  - NovaPay
```

- Also valid:

```yaml
[]
```

- Also valid:
  - empty file

- Invalid:

```yaml
sensitive_terms: Project Titan
```

- Invalid:

```yaml
sensitive_terms:
  - name: Project Titan
```

Expected resolution:

- `sensitive_terms` must resolve to a list of strings

For `config/project_context.yaml`:

- All fields are optional

- Valid partial config:

```yaml
project_name: Semantic Compliance Review Agent
```

- Valid partial config:

```yaml
review_focus:
  - confidential information
  - internal project names
```

- Invalid:

```yaml
review_focus: confidential information
```

Expected resolution:

- `review_focus` must resolve to a list of strings
- error messages for invalid YAML should include file path, config type, the
  underlying YAML parser error, and line/column when available
- error messages for invalid structure/type should explain the expected
  structure

Responsibility:

- Load YAML safely
- Load project context
- Load organization-defined sensitive terms
- Validate expected types
- Return ReviewContext
- Collect concise config warnings

Does NOT:

- Classify findings
- Call ADK
- Modify configuration
- Generate reports

Phase 4 implementation note:

- `src/context_loader.py` now includes the required module-level docstring
- The implementation uses `yaml.safe_load()` plus explicit schema validation
- Missing or empty config files produce warnings instead of hard failures
- Invalid YAML or invalid structure/type raises `ContextLoadError`

## Agent Review

Input:

- ReviewableText[]
- ReviewContext

Output:

List[Finding]

Fields:

- id
- reviewable_text_id
- category
- severity
- confidence
- detection_method
- source_text
- line_start
- line_end
- explanation
- recommendation
- suggested_replacement

Approved finding categories:

- SECURITY_RISK
- PROFESSIONALISM_RISK
- COMPLIANCE_RISK
- INTERNAL_CODENAME_EXPOSURE
- INTELLECTUAL_PROPERTY_RISK
- REPUTATION_RISK

Approved severity values:

- LOW
- MEDIUM
- HIGH
- CRITICAL

MVP severity note:

- Avoid CRITICAL unless the finding is clearly credential/security related

Approved confidence values:

- LOW
- MEDIUM
- HIGH

Important distinction:

- Severity describes how dangerous the issue may be
- Confidence describes how certain the agent is that the text should be reviewed
- Severity and confidence must not be conflated

Approved detection methods:

- TERM_MATCH
- SEMANTIC_ANALYSIS
- HYBRID

Detection method definitions:

- TERM_MATCH: a known sensitive term from config was detected
- SEMANTIC_ANALYSIS: the agent flagged risk based on meaning, tone, or implication
- HYBRID: a configured sensitive term is present and surrounding language adds semantic risk

Detection method guardrails:

- do not use HYBRID when no configured sensitive term is present
- do not use HYBRID only because the finding is severe or high confidence
- do not use HYBRID only because a suggested replacement exists
- if a configured term match alone is sufficient, use TERM_MATCH
- if no configured term match exists, use SEMANTIC_ANALYSIS

HYBRID example:

`TODO: remove the Project Titan workaround before launch`

Reason:

- `Project Titan` matches a configured sensitive term
- `remove`, `workaround`, and `before launch` add semantic risk

TERM_MATCH confidence rule:

- TERM_MATCH findings are HIGH confidence by construction

Zero findings rule:

- An empty findings list is a successful review result
- `Findings generated: 0` is valid CLI output
- Zero findings is not an AgentReviewError

On Failure:

- Raises AgentReviewError when:
  - the ADK agent fails
  - the model call fails
  - structured output cannot be parsed after one retry
  - an unexpected runtime failure occurs

Responsibility:

- Perform semantic review
- Use project context
- Generate structured findings
- Explain why each item was flagged
- Recommend safe human-reviewed remediation

MVP behavior:

- Use ADK-backed review if available
- Keep structured output validation
- Return findings only
- Print findings summary in the CLI
- Send all `ReviewableText` items and `ReviewContext` in one review request
- Do not call the model once per item

Structured output retry rule:

- Retry once if the first agent response cannot be parsed into the `Finding` schema
- Raise AgentReviewError if the second attempt also fails

Suggested replacement rule:

- `suggested_replacement` is optional
- Include it only when the remediation is clearly safe
- Use `null` when uncertain
- For HIGH-confidence findings, include a safe neutral replacement when one is
  obvious from the source text alone
- Suggested replacements must preserve comment intent while removing risky,
  sensitive, or unprofessional wording
- Suggested replacements must not introduce secrets, internal codenames,
  credentials, or speculative information

Does NOT:

- Read files
- Extract text
- Load config files
- Write reports
- Modify source code
- Create clean copies
- Commit changes

Important Boundary:

`agent_review.review(reviewable_texts, review_context) -> list[Finding]`

This boundary should remain isolated so ADK can be replaced later if required.

The rest of the application should not care whether findings come from:

- ADK
- direct Gemini fallback
- test stub
- future local model

Phase 5 implementation note:

- `src/agent_review.py` now implements the review boundary behind ADK
- the current working local behavior uses a deterministic in-process fallback
  model so Phase 5 can be tested without live model credentials
- structured finding validation remains enforced
- all extracted text and context are sent in one review request for the MVP

Phase 5.1 backend design note:

- the `agent_review.review(reviewable_texts, review_context) -> list[Finding]`
  boundary remains unchanged
- Agent Review should support two backends:
  - Gemini
  - Deterministic
- Gemini is the approved default backend
- Deterministic is the approved explicit offline/test backend
- backend selection should happen via CLI flags:
  - `--backend gemini`
  - `--backend deterministic`
- one review request should still be used per file
- if Gemini is selected and fails, the CLI must fail clearly and must not
  silently fall back to Deterministic
- the CLI should print which backend was used

Phase 5.2 implementation note:

- `src/main.py` now accepts `--backend gemini` and `--backend deterministic`
- unsupported backend values are rejected by CLI argument validation
- Gemini is the default backend
- Deterministic remains the explicit offline/test backend
- missing Gemini credentials fail during CLI startup before file reading, text
  extraction, context loading, or agent review begins
- supported environment variables are `GOOGLE_API_KEY` and `GEMINI_API_KEY`
- Gemini model selection is currently `gemini-2.5-flash`
- one review request is still used per file
- malformed structured output still retries once
- provider failures do not silently fall back to Deterministic
- Gemini is now explicitly instructed to include `suggested_replacement` only
  when a safe neutral rewrite is obvious; otherwise it should return `null`
- Gemini is also explicitly instructed to keep `detection_method` aligned with
  the TERM_MATCH / SEMANTIC_ANALYSIS / HYBRID contract and not overuse HYBRID
- the `agent_review.review(reviewable_texts, review_context) -> list[Finding]`
  boundary remains unchanged

## Report Writer

Input:

- FileContent
- ReviewableText[]
- Findings
- ReviewContext
- Backend metadata

Output:

`output/<filename>-audit-report.md`

On Failure:

Raises ReportWriteError

Responsibility:

- Generate Markdown audit report
- Summarize findings
- Preserve finding order
- Preserve line numbers
- Preserve source text
- Include backend/model metadata
- Write report to output directory

Does NOT:

- Call Gemini
- Generate findings
- Modify source files
- Re-run agent review
- Create clean copies
- Evaluate quality
- Scan repositories
- Rewrite files

Approved report sections:

1. Report Header
   - `Semantic Compliance Audit Report`
2. Metadata Table
   - include only available metadata such as target file, generated timestamp,
     backend, model, configured sensitive terms, findings count, and audit
     status
3. Executive Summary
   - include only currently available top-level summary values such as audit
     status, findings count, highest severity present, and detected categories
4. Audit Summary Matrix
   - include reference, category, severity, and confidence
5. Findings
   - one section per finding, preserving input order
   - include reference, category, severity, confidence, detection method,
     line numbers, source text, explanation, recommendation, and suggested
     replacement when present
6. Zero Findings Section
   - zero findings is a successful report result
   - generate the report anyway and state that no findings were generated
7. Finding Reference Guide
   - include category legend for CDX, SEC, PRO, CMP, IPR, and REP
8. Review Philosophy
   - include AI-assisted review, human review required, no automatic source
     modification, and developer responsibility

Approved MVP rules:

- use `examples/sample-audit-report.md` as a structure and style guide only
- do not invent metrics, placeholder findings, fake statistics, or fabricated
  counts
- `Findings > 0` maps to `ISSUES FOUND`
- `Findings == 0` maps to `NO ISSUES FOUND`
- report references must use category prefixes:
  - `SECURITY_RISK -> SEC`
  - `PROFESSIONALISM_RISK -> PRO`
  - `COMPLIANCE_RISK -> CMP`
  - `INTERNAL_CODENAME_EXPOSURE -> CDX`
  - `INTELLECTUAL_PROPERTY_RISK -> IPR`
  - `REPUTATION_RISK -> REP`
- numbering is per category, starts at `001`, and follows the existing
  `Finding[]` order without reordering
- when `suggested_replacement` is null, display a human-friendly
  no-suggestion message without inventing remediation content
- if the report file already exists, overwrite it without prompting or creating
  copy files

Failure behavior:

- raise `ReportWriteError` when:
  - the output directory cannot be created
  - the report file cannot be written
  - invalid report data is received
  - an unexpected write failure occurs

Phase 6 design note:

- the first implementation should keep the MVP intentionally simple:
  one file in, one review, one Markdown report out

Phase 6.5 implementation note:

- `src/report_writer.py` now writes one Markdown report into `output/`
- the report uses only data already produced by the current pipeline
- existing report files are overwritten instead of versioned
- the CLI now fails clearly on `ReportWriteError`
- the CLI prints the written report path after successful report generation

Phase 6.6 readability design note:

- report readability should improve without changing the underlying review data
- the report should add a stronger executive summary near the top using only:
  - findings count
  - highest severity present
  - detected categories
  - audit status
- the Audit Summary Matrix should move closer to the top of the report
- detailed finding sections should become more narrative and easier to scan
- if `suggested_replacement` exists, it should be shown in a diff-style block
- if `suggested_replacement` is null, keep a human-friendly no-suggestion
  message rather than fabricating a replacement
- zero-findings reports should still feel complete and successful
- the report must not invent findings, statistics, or new analysis
- the report must not reorder findings or recalculate severity/confidence

Phase 6.7 implementation note:

- the report now presents a stronger Executive Summary near the top
- the Audit Summary Matrix now appears before Detailed Findings
- detailed findings use a more narrative layout for location, explanation, and recommended action
- suggested replacements render as diff-style blocks when present
- zero-findings reports now read as successful completed audits
- the readability improvements do not change finding order or underlying review data

Phase 6.9B cleanup note:

- unsupported file types now fail clearly instead of appearing as zero-finding
  clean audits
- `src/main.py`, `src/schemas.py`, and `src/file_reader.py` now include the
  required module-level docstrings
- CLI config warnings now print the warning messages instead of only a count
- `.gitignore` now blocks common local environment and secret files more safely

Phase 6.95 design note:

- the next extraction expansion remains a documentation-approved design only
- only the Text Extractor is allowed to expand in Phase 6.96
- multi-language support is limited to human-written text surfaces, not full
  parsing of Python, JavaScript, TypeScript, JSX, TSX, HTML, or Markdown
- unsupported file types should continue to fail clearly after the expansion

Phase 6.75 implementation note:

- category labels remain human-readable throughout the report
- detection methods now display as human-readable labels
- severity and confidence now use approved visual indicators
- location display now uses `line` for single-line findings and `lines` for ranges
- no-suggestion messaging is more human-friendly while preserving meaning
- this phase improves presentation only and does not change report structure or review data

## Clean Copy Writer

Input:

- FileContent
- Findings

Output:

`output/<filename>-clean-copy.<ext>`

On Failure:

Raises CleanCopyWriteError

Responsibility:

- Generate optional suggested clean copy

Does NOT:

- Overwrite original files
- Modify executable code

## Evaluation

Input:

- Evaluation cases
- Expected outputs

Output:

Evaluation metrics

- precision
- recall
- false positives
- false negatives

On Failure:

Raises EvaluationError

Responsibility:

- Evaluate agent quality
- Compare actual findings against committed expected outputs
- Report backend-specific evaluation metrics and artifacts

Does NOT:

- Modify source files
- Affect normal scans
- Change review behavior for the main CLI pipeline
