# Security Guardrails

This document records the current safety boundaries for the Semantic
Compliance Review Agent.

The project is intentionally designed as an advisory review tool, not an
autonomous repository-editing system.

## Core Safety Position

- The tool reviews one file at a time.
- The tool produces an audit report.
- The tool may optionally produce a separate clean-copy artifact.
- The tool does not overwrite the original source file.
- The tool does not silently switch backends when Gemini fails.
- The developer remains responsible for all final decisions.

## Source Modification Boundaries

### Original Files Are Never Modified

The runtime pipeline reads a file, extracts reviewable text, loads context,
reviews the content, and writes output artifacts under `output/`.

It does not overwrite the original input file.

It does not apply suggested replacements in place.

### Clean Copies Are Separate Advisory Artifacts

When `--clean-copy` is requested, the system may write a separate clean-copy
file under `output/`.

Clean-copy generation is conservative:

- it requires source text plus a non-empty suggested replacement
- the source text must appear exactly once
- the replacement must be exact and unambiguous
- ambiguous or missing replacements are skipped

Human review is still required before adopting the clean-copy wording.

## Backend Safety

### No Silent Gemini Fallback

Gemini is the default backend.

Deterministic mode exists as an explicit offline and test backend.

If Gemini is selected and fails, the run fails clearly.

The system must not silently fall back to deterministic mode.

### Model Configuration Safety

Gemini model selection is controlled through `GEMINI_MODEL`.

Default model:

- `gemini-2.5-flash`

Recommended reliability-sensitive model:

- `gemini-2.5-pro`

Model selection changes which Gemini model is used. It does not bypass the
existing backend boundary, credential checks, or report-generation rules.

## Credential Handling

### Environment Variables Only

Gemini credentials must come from environment variables:

- `GOOGLE_API_KEY`
- `GEMINI_API_KEY`

The repository should not contain real API keys.

### No Secret Logging

Secrets must not be printed in normal console output, written into generated
reports, or committed into the repository.

### API Key Hygiene

When using Gemini, API keys should be restricted appropriately for the Gemini
API / `generativelanguage.googleapis.com`.

## Failure-Mode Safety

The system is designed to fail clearly when a core assumption is violated.

Examples:

- missing Gemini credentials
- invalid YAML configuration
- unsupported file type input
- malformed structured output
- unreadable or invalid input files

Clear failure is preferred over hidden behavior changes.

## Report Safety Boundaries

The audit report is an advisory artifact.

It is not:

- an automatic fix
- a security approval
- a source patch
- a replacement for human review

Suggested replacements are optional review outputs and should be treated as
draft remediation wording, not trusted automatic edits.

## Scope Guardrails

Current supported extraction scope:

- Python comments and docstrings
- JavaScript-family comments
- HTML comments
- Markdown prose blocks

The project does not include:

- repository-wide scanning
- web UI
- database
- authentication
- multi-agent orchestration
- autonomous code modification

## Why These Guardrails Matter

The project is meant to demonstrate useful agent behavior with clear
boundaries, visible failure modes, and human accountability.

This repo therefore prioritizes:

- explicit scope
- visible provenance
- review over automation
- safe defaults over convenience
