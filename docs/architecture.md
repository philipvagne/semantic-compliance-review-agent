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
- the documented MVP workflow for later phases

The current runnable CLI path is the File Reader plus Text Extractor plus
Context Loader plus Agent Review flow.

The next approved implementation step is Phase 6.5: Report Writer implementation.

## Implemented Flow

User
-> CLI
-> File Reader
-> Text Extractor
-> Context Loader
-> Agent Review
-> Console Summary

The current CLI accepts one source file path, reads it as UTF-8, extracts
reviewable text from Python files, loads review context from YAML config files,
reviews the extracted text through the Agent Review boundary, and prints a
console summary of the extracted items, loaded context, and findings.

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

- Returns an empty list if no reviewable text exists
- Raises ExtractionError only for unexpected parser/runtime failures
- No reviewable text is not an error

MVP scope decision for first implementation:

- Support Python comments
- Support Python docstrings
- Support TODO / FIXME / NOTE comments
- Do not implement string literal extraction in the first implementation

Reason:

- Comments and docstrings are the core promise
- String literals add complexity and higher misclassification risk
- String literal extraction should be added later as a controlled expansion

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
- Collect config warnings

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
3. Scan Statistics
   - include only statistics currently available from the pipeline, such as
     reviewable text items analyzed and findings generated
4. Findings
   - one section per finding, preserving input order
   - include reference, category, severity, confidence, detection method,
     line numbers, source text, explanation, recommendation, and suggested
     replacement when present
5. Zero Findings Section
   - zero findings is a successful report result
   - generate the report anyway and state that no findings were generated
6. Audit Summary Matrix
   - include reference, category, severity, and confidence
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
- when `suggested_replacement` is null, display:
  - `No automatic suggestion generated.`
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

Does NOT:

- Modify source files
- Affect normal scans
