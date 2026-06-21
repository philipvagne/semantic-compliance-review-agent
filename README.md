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
Next: Phase 4 - Context Loading.

## Purpose

An AI-assisted compliance review system that identifies potentially risky
human-written text inside source code repositories.

## Current Phase

Phase 4 - Context Loading

## Phase 3 Text Extraction

The CLI now accepts a single source file path, reads the file as UTF-8,
extracts reviewable text from Python files, and prints a small extraction
summary.

Run it with:

```text
python -m src.main examples/sample_input.py
```

Expected output:

```text
File read successfully
Path: examples/sample_input.py
Reviewable text items found: 6
- DOCSTRING 1-1: Small sample file for Phase 3 manual text-extraction testing.
- TODO 3-3: TODO: remove the temporary admin password before release
- NOTE 4-4: NOTE: this sample intentionally contains several reviewable text types
- DOCSTRING 8-8: Return a friendly greeting for manual extractor testing.
- COMMENT 9-9: Friendly example content for the extractor.
- FIXME 14-14: FIXME: replace the hard-coded example value later
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

## Phase 0.5 Spike

The repository includes a minimal local ADK feasibility spike that proves:

- an ADK agent runs locally
- review text can be passed into the runner
- the agent calls a custom `load_sensitive_terms()` tool
- the tool result is consumed before the final response is produced
- the final response is structured JSON that parses into a project schema

The spike is intentionally narrow and does not implement file reading, report
generation, evaluation, scanning, or future project phases.
