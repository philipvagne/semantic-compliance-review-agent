# AGENTS.md

## Project Goal

Build the Semantic Compliance Review Agent according to the project-plan-v4.txt specification.

## Core Principles

- Boring, safe, but finished
- Review before modification
- Human responsibility remains final
- Explainable over magical

## MVP Constraints

Do NOT add:

- Web UI
- Database
- Authentication
- Repository-wide scanning
- Multi-agent architecture
- Cloud deployment

unless explicitly requested.

## Documentation Sync Rule

For every non-trivial task, Codex must identify which documentation files are affected and update them in the same task.

Codex must check at minimum:
- README.md
- specs/project-plan-v4.txt
- docs/build-log.md
- docs/architecture.md
- docs/codex-workflow.md
- docs/security-guardrails.md
- docs/evaluation-plan.md
- docs/course-concepts.md

Codex should only update files affected by the task.

Before finishing, Codex must report:
1. Which documentation files were checked
2. Which documentation files were updated
3. Which documentation files were intentionally left unchanged
4. Why each unchanged file did not need an update

Codex must not defer documentation synchronization to a later cleanup step unless the user explicitly asks for that.

The user reviews the diff. The user does not manually synchronize documentation unless needed.

## Code Documentation Rule

Each major component should contain a short
module-level docstring describing:

- Purpose
- Inputs
- Outputs
- Responsibilities
- Non-responsibilities

Avoid implementation comments unless they
clarify non-obvious logic.
