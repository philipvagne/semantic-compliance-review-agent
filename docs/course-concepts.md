# Course Concepts Mapping

This document maps the Semantic Compliance Review Agent to capstone and course
concepts using the current repository state as of Phase 6.9A.

The goal is to be explicit about what is already implemented versus what is
planned for later phases.

## Implemented Concepts

### 1. Agent

Implemented now.

The project includes an ADK-backed review boundary in
`src/agent_review.py`.

Current role of the agent:

- receive extracted reviewable text
- receive project context
- return structured findings

This is a single-agent design, not a multi-agent system.

That is an intentional MVP choice.

### 2. Tools and Workflow Components

Implemented now.

The project is organized as a CLI workflow with focused components:

- File Reader
- Text Extractor
- Context Loader
- Agent Review
- Report Writer

These components behave like explicit tools or stages in a controlled agent
workflow even though the user experience is CLI-first.

### 3. Structured Output

Implemented now.

The review layer validates model output against a structured `Finding` schema.

This matters for:

- predictable downstream report generation
- safer handling of model responses
- explainable and testable review outputs

### 4. Guardrails

Implemented now and documented more explicitly in Phase 6.9A.

Examples:

- no automatic source modification
- no automatic commits
- no silent Gemini fallback
- fail-fast credential validation
- human review required
- advisory suggestions only

### 5. Human-in-the-Loop

Implemented now.

The current product outcome is a Markdown audit report for developer review.

The system does not auto-apply suggestions or make release decisions.

### 6. Prompting and Instruction Design

Implemented now.

The Gemini path uses explicit review instructions that constrain:

- finding shape
- detection methods
- confidence usage
- replacement behavior

This is part of the project's explainability story, even though prompt quality
will continue to evolve.

### 7. Configuration and Context Loading

Implemented now.

The project loads context from YAML configuration files:

- `config/sensitive_terms.yaml`
- `config/project_context.yaml`

This demonstrates context injection into the review step rather than using a
stateless prompt only.

### 8. CLI Workflow

Implemented now.

The project is intentionally CLI-first.

That supports:

- reproducibility
- low operational complexity
- transparent local execution
- easy capstone demo flow

### 9. Observability and Development Record

Partially implemented now.

There is no dedicated runtime logging system yet, but the repository does have:

- clear CLI status output
- a detailed build log in `docs/build-log.md`
- recorded phase-by-phase implementation notes

This is enough to support the current project story, but runtime observability
could still improve later.

## Planned Concepts

### 10. Evaluation

Planned for Phase 8.

Evaluation is documented as a required project capability, but it is not yet
implemented in runtime code.

Planned scope includes:

- hand-built cases
- expected findings
- clean zero-finding cases
- sensitive-term match cases
- semantic-risk cases
- hybrid cases
- basic precision/recall-style review if feasible

This concept should not be claimed as complete yet.

### 11. Broader Extraction Coverage

Implemented now for the required MVP file types.

Current extraction scope includes:

- `.py`
- `.js`
- `.ts`
- `.jsx`
- `.tsx`
- `.html`
- `.md`

Required before final submission:

- `.py`
- `.js`
- `.ts`
- `.jsx`
- `.tsx`
- `.html`
- `.md`

Potential later expansion:

- `.yaml` / `.yml`
- `.json`
- `Dockerfile`
- Terraform files

This required coverage is now implemented. Broader file-family expansion
remains a roadmap item.

## Honest Current Summary

The strongest course-concept coverage today is:

- agent workflow
- structured output
- guardrails
- human-in-the-loop review
- context loading
- CLI orchestration
- prompt/instruction design

The weakest still-missing concept area is formal evaluation.

That gap is already recognized in the project plan and should be addressed in
Phase 8 rather than being overstated now.
