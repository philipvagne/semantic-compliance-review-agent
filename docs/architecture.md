# Architecture

## Current System Shape

The Semantic Compliance Review Agent is a CLI-first review pipeline with a
clean separation between extraction, review, reporting, and optional
clean-copy generation.

Current runtime flow:

```text
User
-> CLI
-> File Reader
-> Text Extractor
-> Context Loader
-> Agent Review
-> Optional Clean Copy Writer
-> Report Writer
-> Console Summary + Output Artifacts
```

The architecture is intentionally narrow:

- one file per run
- no repository-wide scanning
- no automatic source modification
- no silent backend fallback

## Runtime Components

### CLI

Primary module:

- `src/main.py`

Responsibilities:

- parse command-line arguments
- coordinate the runtime flow
- select the review backend
- trigger optional clean-copy generation
- print a concise console summary

Does not:

- extract text
- review content directly
- generate findings itself
- modify the original source file

### File Reader

Primary module:

- `src/file_reader.py`

Responsibilities:

- read one source file safely as UTF-8
- return raw content plus basic metadata

Does not:

- scan repositories
- extract comments or prose
- review content

### Text Extractor

Primary modules:

- `src/text_extractor.py`
- `src/extractors/javascript_extractor.py`
- `src/extractors/html_extractor.py`
- `src/extractors/markdown_extractor.py`

Responsibilities:

- extract reviewable human-written text
- preserve line numbers and surrounding context
- fail clearly for unsupported file types

Supported scope:

- Python comments and docstrings
- JavaScript-family comments
- HTML comments
- Markdown headings, paragraphs, list items, and blockquotes

Non-responsibilities:

- code execution analysis
- full language parsing
- risk classification
- report generation

### Context Loader

Primary module:

- `src/context_loader.py`

Responsibilities:

- load `config/sensitive_terms.yaml`
- load `config/project_context.yaml`
- validate structure and types
- return review context plus warnings when appropriate

Does not:

- call Gemini
- generate findings
- modify configuration

### Agent Review

Primary module:

- `src/agent_review.py`

Responsibilities:

- review extracted text using project context
- return structured findings
- support both Gemini and deterministic backends
- preserve a clean backend boundary
- validate structured output
- retry bounded transient Gemini provider failures only

Important boundary:

```text
review(reviewable_texts, review_context) -> list[Finding]
```

This boundary keeps the rest of the system independent from backend details.

### Clean Copy Writer

Primary module:

- `src/clean_copy_writer.py`

Responsibilities:

- generate a separate advisory clean-copy artifact under `output/`
- apply only safe, exact, unambiguous replacements
- skip ambiguous replacements conservatively

Does not:

- overwrite the original file
- edit files in place
- generate source patches

### Report Writer

Primary module:

- `src/report_writer.py`

Responsibilities:

- write one Markdown audit report
- summarize findings
- preserve finding order and line references
- include backend and model metadata
- include clean-copy summary information when applicable

Does not:

- invent findings
- re-run review
- modify source files

## Data Contracts

Core shared structures live in `src/schemas.py`.

Important runtime objects:

- `FileContent`
- `ReviewableText`
- `ReviewContext`
- `Finding`

These structures provide stable contracts between pipeline stages.

## Backend Abstraction

The project supports two review backends:

- Gemini
- deterministic

Gemini is the default semantic-review backend.

Deterministic is the explicit offline and test backend used for predictable
local checks and evaluation verification.

Key rules:

- no silent Gemini fallback
- credentials are required for Gemini
- backend selection should not change the surrounding pipeline structure

## Safety Boundaries

The architecture is intentionally advisory.

Implemented safety constraints:

- original input files are never modified
- clean-copy generation is opt-in and writes separate artifacts
- unsupported files fail clearly
- invalid configuration fails clearly
- human review remains required for any remediation

## Evaluation And Diagnostics

Evaluation and diagnostics are separate from the normal review CLI path.

Primary evaluation modules:

- `evaluation/run.py`
- `evaluation/diagnose_gemini.py`

Evaluation responsibilities:

- load committed cases and expected JSON files
- run deterministic or Gemini evaluation
- calculate TP, FP, FN, precision, and recall
- write committed result artifacts

Diagnostic responsibilities:

- compare direct Gemini calls with the ADK-backed review path
- report model, API-key variable, timing, and PASS / FAIL status
- support repeated observation cycles

These tools do not change the normal application pipeline.

## Repository Boundaries

The architecture explicitly does not include:

- repository-wide scanning
- web UI
- database
- authentication
- multi-agent orchestration
- autonomous code modification

Those exclusions are part of the design, not missing hidden features.
