# Video Writeup Skeleton

Planning notes for the capstone writeup and short demo video.

This is a structure and idea scaffold, not a final script.

## Problem

- Developers often leave risky human-written text in source files.
- That text can expose internal names, shortcuts, unprofessional wording, or
  security concerns.
- Traditional code-focused review tools often do not prioritize this layer of
  repository risk.

## Solution

- Read one supported file at a time.
- Extract reviewable human-written text from approved text surfaces.
- Load project context and sensitive terms from YAML config.
- Send the extracted text through the review boundary.
- Produce a structured Markdown audit report for human review.

## Why Agents?

Traditional linters and pattern-matching tools can find exact terms, but they
struggle to understand meaning, context, and intent. An LLM-powered review
agent can review human-written comments, documentation, and notes semantically,
allowing it to identify professionalism risks, security concerns, internal
naming issues, and contextual concerns that simple static rules may miss.

Useful talking points:

- The project uses an agent because the task depends on interpretation, not
  only exact syntax matching.
- The agent still works inside clear boundaries instead of acting autonomously.
- Structured findings keep the output inspectable and explainable.

## Architecture

- CLI-first workflow
- File Reader
- Text Extractor
- Context Loader
- Agent Review
- Report Writer
- Markdown audit report as the final advisory artifact

Points to highlight:

- Multi-file support exists at the extraction layer, not through a broader
  architecture rewrite.
- Context files help the review step understand organization-specific risk.
- Gemini and deterministic review paths share the same review boundary.

## Demo Plan

- Show one supported input file.
- Run the CLI in deterministic mode for a stable demo path.
- Point out the extracted reviewable text count.
- Show that project context and sensitive terms are loaded.
- Open the generated Markdown audit report.
- Highlight one finding, its explanation, and the human-review disclaimer.

Optional backup demo notes:

- Keep one Python example and one non-Python example ready.
- Mention that unsupported behavior was intentionally fail-clear until support
  was implemented for each file family.

## Reflection / What I Learned

- Narrow scope made the architecture easier to finish and explain.
- Guardrails improved trust more than extra automation would have.
- Documentation-first phase planning reduced rework across implementation
  slices.
- Expanding extraction carefully was safer than trying to parse every language
  deeply.
