# Architecture

## Current Implementation Status

The repository now contains:

- a completed Phase 0.5 ADK feasibility spike
- a completed Phase 2 File Reader
- a completed Phase 3 Text Extractor for Python comments and docstrings
- an approved Phase 3.5 Context Loader design
- a completed Phase 4 Context Loader
- an approved Phase 4.5 Agent Review design
- the documented MVP workflow for later phases

The current runnable CLI path is the File Reader plus Text Extractor plus
Context Loader flow.

The next approved implementation step is Phase 5: Agent Review.

## Implemented Flow

User
-> CLI
-> File Reader
-> Text Extractor
-> Context Loader
-> Console Summary

The current CLI accepts one source file path, reads it as UTF-8, extracts
reviewable text from Python files, loads review context from YAML config files,
and prints a console summary of the extracted items and loaded context.

## ADK Spike Status

The ADK spike remains in the repository as a narrow feasibility artifact.

Implemented in Phase 0.5:

- one ADK agent
- one custom tool
- one structured finding schema
- local deterministic orchestration validation

Not part of the Phase 2 runtime path:

- agent review from the CLI
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

## Report Writer

Input:

- FileContent
- Findings
- ReviewContext

Output:

`output/<filename>-audit-report.md`

On Failure:

Raises ReportWriteError

Responsibility:

- Generate Markdown audit report
- Write report to output directory

Does NOT:

- Modify source files
- Re-run agent review

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
