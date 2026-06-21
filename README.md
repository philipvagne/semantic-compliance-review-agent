# Semantic Compliance Review Agent

Google x Kaggle AI Agents Capstone Project

## Status

Planning complete.
Repository foundation complete.
ADK feasibility spike complete.
MVP workflow/component contracts complete.
Foundation review complete.
Phase 2 - File Reader complete.
Phase 2.5 - Text Extraction design complete.
Phase 3 - Text Extraction complete for Python comments and docstrings.
Phase 3.5 - Context Loading design complete.
Phase 4 - Context Loading complete.
Phase 4.5 - Agent Review design complete.
Phase 5 - Agent Review complete.
Phase 5.1 - Optional Gemini Review Path design complete.
Phase 5.2 - Gemini Review Path complete.
Next: Phase 6 - Report Generation.

## Purpose

An AI-assisted compliance review system that identifies potentially risky
human-written text inside source code repositories.

## Current Phase

Phase 6 - Report Generation

## Phase 3 Text Extraction

The CLI now accepts a single source file path, reads the file as UTF-8,
extracts reviewable text from Python files, loads review context from YAML
config files, runs agent review, and prints a small summary.

Run it with:

```text
python -m src.main examples/sample_input.py --backend deterministic
```

Expected output:

```text
File read successfully
Path: examples/sample_input.py
Backend: Deterministic
Reviewable text items found: 6
Context loaded successfully
Sensitive terms loaded: 3
Findings generated: 1
- DOCSTRING 1-1: Small sample file for Phase 3 manual text-extraction testing.
- TODO 3-3: TODO: remove the temporary admin password before release
- NOTE 4-4: NOTE: this sample intentionally contains several reviewable text types
- DOCSTRING 8-8: Return a friendly greeting for manual extractor testing.
- COMMENT 9-9: Friendly example content for the extractor.
- FIXME 14-14: FIXME: replace the hard-coded example value later
* HIGH SECURITY_RISK line 3: The text references a temporary or administrative secret-like value that should be reviewed before release
```

Current Text Extraction scope:

- Python comments
- Python docstrings
- TODO / FIXME / NOTE comments
- preserved line numbers, language, and surrounding context
- returns an empty list when no reviewable text is found
- raises `ExtractionError` only for unexpected extraction failures

Explicitly deferred from the first implementation:

- string literal extraction
- agent review
- risk classification
- report generation

## Phase 4 Context Loading

The CLI now loads review context after text extraction using:

`ReviewableText[] + config files -> Context Loader -> ReviewContext`

Config inputs:

- `config/sensitive_terms.yaml`
- `config/project_context.yaml`

`ReviewContext` fields:

- `sensitive_terms: list[str]`
- `project_name: str | None`
- `project_description: str | None`
- `review_focus: list[str]`
- `config_warnings: list[str]`

Current Context Loading behavior:

- missing config file -> warn and continue with defaults
- empty config file -> warn and continue with defaults
- invalid YAML -> raise `ContextLoadError`
- invalid structure/type -> raise `ContextLoadError`
- missing optional fields -> allowed

Current Context Loading scope:

- safe YAML loading only
- strict validation of expected config types
- sample config files included for manual testing
- no agent review
- no risk classification
- no report generation

## Phase 5 Agent Review

The CLI now sends all extracted text plus loaded review context into the Agent
Review boundary:

`ReviewableText[] + ReviewContext -> Agent Review -> Finding[]`

Approved review boundary:

`agent_review.review(reviewable_texts, review_context) -> list[Finding]`

The rest of the application should not care whether findings come from:

- ADK
- direct Gemini fallback
- test stub
- future local model

Approved `Finding` fields:

- `id`
- `reviewable_text_id`
- `category`
- `severity`
- `confidence`
- `detection_method`
- `source_text`
- `line_start`
- `line_end`
- `explanation`
- `recommendation`
- `suggested_replacement`

Approved MVP review behavior:

- zero findings is a successful result
- TERM_MATCH findings are HIGH confidence by construction
- retry once on malformed structured output
- send all extracted text and context in one review request
- suggested replacements stay optional

Current Phase 5 implementation note:

- the review boundary is ADK-backed
- Gemini is now the default backend
- the deterministic backend remains available as an explicit offline/test mode
- both backends stay behind the same review boundary

## Phase 5.2 Gemini Review Path

Agent Review now supports two backends behind the same review boundary:

- Gemini
- Deterministic

Current backend selection:

- default backend: Gemini
- explicit offline/test backend: Deterministic
- CLI flags:
  - `--backend gemini`
  - `--backend deterministic`

Current CLI behavior:

- `python -m src.main examples/sample_input.py` uses Gemini
- `python -m src.main examples/sample_input.py --backend deterministic` uses the deterministic backend
- the CLI prints which backend was used
- missing Gemini credentials fail during CLI startup before file reading begins
- Gemini provider failures fail clearly and do not silently fall back to deterministic
- supported environment variables are `GOOGLE_API_KEY` and `GEMINI_API_KEY`

## Phase 0.5 Spike

The repository includes a minimal local ADK feasibility spike that proves:

- an ADK agent runs locally
- review text can be passed into the runner
- the agent calls a custom `load_sensitive_terms()` tool
- the tool result is consumed before the final response is produced
- the final response is structured JSON that parses into a project schema

The spike is intentionally narrow and does not implement file reading, report
generation, evaluation, scanning, or future project phases.
