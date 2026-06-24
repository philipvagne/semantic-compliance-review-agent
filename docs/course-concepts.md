# Course Concepts Mapping

This document maps the current Semantic Compliance Review Agent implementation
to capstone and course concepts.

## 1. Agent

The project includes a real ADK-backed review boundary in `src/agent_review.py`.

The agent receives:

- extracted reviewable text
- project context

The agent returns:

- structured findings

This is a single-agent design by choice. The project favors clarity and
submission-ready scope over multi-agent complexity.

## 2. Gemini And Deterministic Backends

The system includes backend abstraction for:

- Gemini for the live semantic-review path
- deterministic mode for repeatable offline and test runs

This supports demo, evaluation, and validation workflows even when live
credentials are unavailable.

## 3. Structured Output

The review layer validates findings against shared schemas.

That supports:

- explainable outputs
- safer downstream report generation
- evaluation matching
- reproducible artifacts

## 4. Tool Use And Workflow Design

The project is organized as an explicit workflow of focused components:

- File Reader
- Text Extractor
- Context Loader
- Agent Review
- optional Clean Copy Writer
- Report Writer
- Evaluation Runner
- Gemini Diagnostic Tool

These components form the project workflow used by the CLI and evaluation
tooling.

## 5. Context Loading

The project loads review context from:

- `config/sensitive_terms.yaml`
- `config/project_context.yaml`

This provides contextual review inputs rather than a stateless prompt-only
design.

## 6. Safety And Guardrails

The project includes several safety concepts:

- no automatic source modification
- no silent Gemini fallback
- environment-variable credential handling
- human review required
- conservative clean-copy generation
- fail-clear behavior for unsupported or invalid conditions

## 7. Evaluation

The repository includes:

- a committed 10-case evaluation dataset
- matching expected JSON files
- deterministic evaluation artifacts
- Gemini evaluation artifacts
- precision and recall reporting

These artifacts provide benchmark and result evidence alongside the runtime
implementation.

## 8. Diagnostics And Reliability Investigation

The repository also includes targeted diagnostics for Gemini path comparison and
reliability investigation.

These diagnostics support reliability investigation by allowing the project to:

- compare direct Gemini calls with the ADK-backed path
- observe repeated runs
- inspect model selection and API-key configuration safely

## 9. Human-In-The-Loop Design

The project produces advisory outputs for developer review.

Even when clean-copy generation is requested:

- the original file is preserved
- ambiguous changes are skipped
- final adoption remains a human decision

## 10. Documentation And Process Discipline

The repository includes:

- architecture documentation
- evaluation documentation
- security guardrails
- archived build-log history
- code and documentation audit artifacts

These materials document implementation, safety, evaluation, and review
processes for the project.

## Intentional Scope Exclusions

The project intentionally does not include:

- multi-agent orchestration
- deployment architecture
- repository-wide autonomous remediation

Those omissions are scope decisions, not hidden missing features.
