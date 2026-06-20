# Semantic Compliance Review Agent

Google x Kaggle AI Agents Capstone Project

## Status

Planning complete.
Repository foundation complete.
ADK feasibility spike complete.
MVP workflow/component contracts complete.
Foundation review complete.
Phase 2 - File Reader complete.
Next: Phase 3 - Text Extraction.

## Purpose

An AI-assisted compliance review system that identifies potentially risky
human-written text inside source code repositories.

## Current Phase

Phase 3 - Text Extraction

## Phase 2 File Reader

The CLI now accepts a single source file path, reads the file as UTF-8, and
prints a small metadata summary.

Run it with:

```text
python -m src.main examples/sample_input.py
```

Expected output:

```text
File read successfully
Path: examples/sample_input.py
Extension: .py
Lines: 10
Characters: 226
```

Current File Reader scope:

- reads one file only
- returns file metadata plus raw text internally
- rejects missing files
- rejects directories passed instead of files
- rejects non-UTF-8 content
- does not extract text
- does not call the agent
- does not generate reports

## Phase 0.5 Spike

The repository includes a minimal local ADK feasibility spike that proves:

- an ADK agent runs locally
- review text can be passed into the runner
- the agent calls a custom `load_sensitive_terms()` tool
- the tool result is consumed before the final response is produced
- the final response is structured JSON that parses into a project schema

The spike is intentionally narrow and does not implement file reading, report
generation, evaluation, scanning, or future project phases.
