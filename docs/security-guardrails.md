# Security Guardrails

This document records the current safety boundaries for the Semantic
Compliance Review Agent as of Phase 6.9A.

The project is intentionally designed as an advisory review tool, not an
autonomous repository-editing system.

## Core Safety Position

- The tool reviews one file at a time.
- The tool produces an audit report.
- The tool does not automatically fix source files.
- The tool does not automatically commit changes.
- The tool does not silently switch review backends when Gemini fails.
- The developer remains responsible for all final decisions.

## Current Guardrails

### No Automatic Source Modification

The current implemented pipeline reads a file, extracts reviewable text, loads
context, performs review, and writes a Markdown audit report.

It does not overwrite the source file.

It does not apply suggested replacements to the source file.

It does not generate a clean copy yet.

### No Automatic Commits

The project does not create commits, push branches, or modify git history as
part of normal runtime behavior.

All repository changes remain a human decision outside the review pipeline.

### Human Review Required

All findings are advisory.

All recommendations require developer review before any action is taken.

This applies to:

- finding severity
- finding confidence
- recommendations
- suggested replacements
- release decisions

### Suggested Replacements Are Advisory Only

Suggested replacements are optional review outputs.

They are not applied automatically.

They should be treated as draft wording for human review, not as trusted
automatic remediation.

The report may display a suggested replacement when Agent Review provides one,
but the report writer does not invent replacements on its own.

### No Silent Gemini Fallback

Gemini is the default backend for the current CLI.

Deterministic mode exists as an explicit offline and test backend.

If Gemini is selected and fails, the run should fail clearly.

The system must not silently fall back to deterministic mode, because silent
fallback would hide runtime conditions and make review provenance unclear.

### Fail Clearly on Unsupported or Invalid Conditions

The current pipeline is designed to fail with explicit errors when a core
assumption is violated.

Examples:

- missing Gemini credentials when Gemini is selected
- invalid YAML configuration
- unsupported file type input
- malformed structured model output after one retry
- unreadable or invalid input files

Clear failure is preferred over hidden behavior changes.

## Secrets and Credential Handling

### Environment Variables Only

Gemini credentials must come from environment variables.

Supported variables:

- `GOOGLE_API_KEY`
- `GEMINI_API_KEY`

The repository should not contain real API keys.

### No Secret Logging

Secrets must not be printed in normal console output, written into generated
reports, or committed into the repository.

The audit scope is source text review, not credential inspection of runtime
environment values.

### No Secret Commits

Real credentials must not be stored in:

- tracked source files
- documentation
- config files
- sample outputs
- commit history

`.env.example` exists only to document required variable names.

## Report Safety Boundaries

The generated report is an advisory audit artifact.

It is not:

- an automatic fix
- a code patch
- a source-of-truth security approval
- a replacement for human review

The report should be understood as a structured prompt for developer review.

## Scope Guardrails

The current implementation is intentionally limited.

Current supported extraction scope:

- Python files only
- comments
- docstrings
- TODO / FIXME / NOTE comments

Not yet implemented:

- multi-language extraction
- repository-wide scanning
- automatic clean-copy generation
- evaluation harness

These limitations are intentional MVP boundaries, not hidden capabilities.

## Why These Guardrails Matter

The capstone goal is to demonstrate a useful agent with explainable behavior,
clear boundaries, and human accountability.

This project therefore prioritizes:

- explicit scope
- visible failure modes
- review over automation
- documentation over implied behavior
- safe defaults over convenience
