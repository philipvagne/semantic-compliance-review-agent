# Architecture

Developer
-> CLI
-> ADK Spike Runner
-> Minimal ADK Agent
-> Custom Tool: `load_sensitive_terms()`
-> Structured Finding JSON

## Phase 0.5 Scope

This document currently reflects the feasibility spike only.

Implemented in Phase 0.5:

- CLI review text input
- one ADK agent
- one custom tool
- one structured finding schema

Not implemented in Phase 0.5:

- file reading
- text extraction
- report generation
- evaluation
- clean copy generation
- repository-wide scanning
