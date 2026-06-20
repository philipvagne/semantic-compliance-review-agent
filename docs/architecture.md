# Architecture

## Current Implementation Status

The repository now contains:

- a completed Phase 0.5 ADK feasibility spike
- a completed Phase 2 File Reader
- the documented MVP workflow for later phases

The current runnable CLI path is the File Reader flow.

The next approved design step is Phase 2.5: Text Extraction Design.

## Implemented Flow

User
-> CLI
-> File Reader
-> Console Summary

The File Reader is the first real MVP input component. It accepts one source
file path, reads the file as UTF-8, and returns structured file metadata plus
raw text.

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

- `src/text_extractor.py` should include a short module-level docstring covering
  purpose, input, output, responsibilities, and non-responsibilities
- Avoid noisy implementation comments; use comments and docstrings to explain
  component boundaries rather than obvious code

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

- sensitive_terms.yaml
- project_context.yaml

Output:

ReviewContext

- sensitive_terms
- project_context
- config_warnings

On Failure:

- Missing config -> warn and continue
- Empty sensitive terms -> semantic-only mode
- Invalid config -> raise ContextLoadError

Responsibility:

- Load project context
- Load organization-defined sensitive terms

Does NOT:

- Classify findings
- Modify configuration

## Agent Review

Input:

- ReviewableText
- ReviewContext

Output:

List[Finding]

Fields:

- id
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

On Failure:

Raises AgentReviewError

Responsibility:

- Perform semantic review
- Use project context
- Generate structured findings

Does NOT:

- Read files
- Write reports
- Modify source code

Important Boundary:

`agent.review(reviewable_text, context) -> findings`

This boundary should remain isolated so ADK can be replaced later if required.

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
