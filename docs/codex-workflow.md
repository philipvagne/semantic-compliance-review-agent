# Codex Workflow

This document defines how Codex should be used for the Semantic Compliance
Review Agent project.

The goal is to keep implementation controlled, understandable, and aligned
with the archived planning artifact and current documentation set.

## Core Rule

Codex should implement one small, clearly defined task at a time.

Do not ask Codex to build the entire agent in one request.

## Required Context

Before making changes, Codex should read:

* `AGENTS.md`
* `docs/archive/development-journal.txt`
* `docs/architecture.md`
* This file

For task-specific work, Codex should also read the relevant documentation file.

Examples:

* Evaluation work -> `docs/evaluation-plan.md`
* Security/guardrails work -> `docs/security-guardrails.md`
* Architecture changes -> `docs/architecture.md`
* Course concept mapping -> `docs/course-concepts.md`

## Conversation Strategy

Use separate Codex conversations for major implementation areas.

Recommended conversations:

1. `Phase 0.5 - ADK Feasibility Spike`
2. `CLI and File Reader`
3. `Text Extraction`
4. `Context Loading`
5. `ADK Agent Review`
6. `Audit Report Generation`
7. `Clean Copy Generation`
8. `Evaluation Harness`
9. `Final Documentation and Submission Prep`

Each conversation should stay focused on its assigned area.

Do not mix unrelated implementation tasks in the same conversation.

## Task Prompt Template

Use this structure when prompting Codex:

```text
Task:
Implement [specific task].

Context:
Read:
- AGENTS.md
- docs/archive/development-journal.txt
- docs/architecture.md
- docs/codex-workflow.md
- [task-specific docs]

Current Phase:
[Phase name]

Goal:
[What this task should prove or complete]

Constraints:
- Implement only this task.
- Do not implement future phases.
- Do not add unrelated files.
- Do not change architecture unless explicitly requested.
- Do not add a web UI, database, authentication, repository-wide scanning, deployment, or multi-agent architecture.
- Preserve the project philosophy: boring, safe, but finished.

Documentation Rule:
If this task changes behavior, commands, architecture, evaluation, setup, or user-facing output, update the relevant documentation.

Expected Deliverables:
- [File or feature]
- [Test or command]
- [Documentation update if needed]

When complete, report:
1. Files changed
2. What changed
3. Why it changed
4. How to test it
5. Whether the task success criteria were met
```

## Review Checklist

After Codex completes a task, manually check:

* Did it implement only the requested task?
* Did it avoid future phases?
* Did it respect the MVP constraints?
* Did it update relevant documentation?
* Did it explain changed files?
* Did it provide test commands?
* Can the changes be explained clearly?

If the answer is no, revise before committing.

## Commit Strategy

Commit after each completed and verified slice.

Use clear commit messages.

Examples:

```text
Initialize repository foundation
Add ADK feasibility spike
Add CLI file reader
Add text extraction for Python comments
Add context loader for sensitive terms
Generate markdown audit reports
Add evaluation harness
```

## Documentation Sync Rule

For every non-trivial task, Codex must identify which documentation files are
affected and update them in the same task.

Codex must check at minimum:
- README.md
- docs/archive/development-journal.txt
- docs/archive/build-log.md
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

Codex must not defer documentation synchronization to a later cleanup step
unless the user explicitly asks for that.

The user reviews the diff. The user does not manually synchronize
documentation unless needed.

## Scope Control

Interesting ideas that are not required should go into future enhancements.

Do not implement them during the MVP.

Default answer to scope creep:

```text
Future enhancement.
```

## Project Standard

The final project should be:

* Working
* Explainable
* Documented
* Evaluated
* Safe
* Portfolio-ready

The goal is not to build the most complex agent.

The goal is to build a useful agent that can be understood, demonstrated, and
defended.
