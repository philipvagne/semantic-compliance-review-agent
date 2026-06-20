# Semantic Compliance Review Agent

Google x Kaggle AI Agents Capstone Project

## Status

Planning complete.
Repository foundation complete.
ADK feasibility spike implemented.

## Purpose

An AI-assisted compliance review system that identifies potentially risky
human-written text inside source code repositories.

## Current Phase

Phase 0.5 - ADK Feasibility Spike

## Phase 0.5 Spike

The repository includes a minimal local ADK feasibility spike that proves:

- an ADK agent runs locally
- review text can be passed in from the CLI
- the agent calls a custom `load_sensitive_terms()` tool
- the tool result is consumed before the final response is produced
- the final response is structured JSON that parses into a project schema

Run it with:

```text
.venv\Scripts\python -m src.main "# TODO: remove temporary admin password before production"
```

The spike is intentionally narrow and does not implement file reading, report
generation, evaluation, scanning, or future project phases.
