# Architectural Decisions

This log records the most important product and architecture decisions that
shape the current project behavior.

## 2026-06-20

### CLI-First Architecture

Decision:

Use a CLI-first architecture for the MVP.

Reason:

This keeps the project small, reproducible, and easy to explain during the
capstone. It also avoids spending time on UI concerns before the core review
pipeline is stable.

Status:

Accepted

### One File In, One Report Out MVP

Decision:

Keep the first end-to-end workflow limited to one source file in and one
Markdown audit report out.

Reason:

This establishes a narrow, testable contract and avoids overreaching into
repository-wide scanning before the core review logic is stable.

Status:

Accepted

### Python-Only Extraction for the Current MVP

Decision:

Limit current extraction support to Python files only.

Reason:

Python comments and docstrings were the fastest path to a working semantic
review demo with traceable line numbers. Multi-language support remains
required before final submission but was intentionally deferred to avoid
diluting Phase 3 quality.

Status:

Accepted for MVP

### ADK Review Boundary as a Swappable Seam

Decision:

Keep review behavior behind the boundary
`agent_review.review(reviewable_texts, review_context) -> list[Finding]`.

Reason:

The rest of the application should not care whether findings come from Gemini,
deterministic review, or a future replacement backend. This preserves
architectural flexibility without forcing broader rewrites.

Status:

Accepted

## 2026-06-21

### Gemini as the Default Backend

Decision:

Use Gemini as the default review backend.

Reason:

The capstone project needs a real semantic review path, not only a stub. Gemini
provides the model-backed path while still fitting within the current CLI
architecture.

Status:

Accepted

### Deterministic Backend as Explicit Offline/Test Mode

Decision:

Keep a deterministic backend available as an explicit offline and test mode.

Reason:

This supports local development, documentation verification, and predictable
manual checks without requiring live credentials on every run.

Status:

Accepted

### No Silent Fallback from Gemini to Deterministic

Decision:

If Gemini is selected and fails, fail clearly instead of silently switching to
deterministic mode.

Reason:

Silent fallback would hide the real runtime condition and make it unclear
whether the produced findings came from the live model or a local fallback.

Status:

Accepted

### Fail-Fast Credential Validation

Decision:

Validate Gemini credentials during CLI startup before the rest of the pipeline
runs.

Reason:

It is better to fail early than to let the user assume a full review occurred
when the selected backend could not actually run.

Status:

Accepted

### Retry Only Malformed Structured Output

Decision:

Retry once when model output cannot be parsed into the `Finding` schema, but do
not retry provider or network failures as if they were schema problems.

Reason:

Malformed structured output is a bounded format problem. Provider and network
failures are different classes of failure and should remain visible to the
user.

Status:

Accepted

### Suggested Replacements Belong to Agent Review, Not the Report Writer

Decision:

Suggested replacement text must come from the review layer, not be invented by
the report writer.

Reason:

The report writer should present findings, not generate new review judgments or
remediation content.

Status:

Accepted

### Report Writer Must Preserve Finding Order

Decision:

Do not reorder findings in the report.

Reason:

Finding order should remain traceable to the review output so the report stays
faithful to the pipeline rather than becoming a second decision-making layer.

Status:

Accepted

### Report Writer Must Not Invent Findings, Metrics, or Replacements

Decision:

The report writer may format and summarize only data already produced by the
pipeline.

Reason:

Invented statistics or remediation content would weaken trust, blur component
boundaries, and create misleading demo artifacts.

Status:

Accepted

### Human-Readable Finding References

Decision:

Use human-readable report references such as `SEC-001`, `PRO-001`, and
`CDX-001`.

Reason:

These identifiers are easier to discuss in reports, demos, and manual review
than internal object IDs.

Status:

Accepted

### Multi-Language Extraction Is Required Before Submission

Decision:

Treat broader language support as a submission requirement, but do not claim it
as implemented now.

Reason:

The current Python-only MVP is real and useful, but it is narrower than the
planned capstone deliverable. The roadmap must acknowledge that gap honestly.

Status:

Accepted as a roadmap requirement

### Unsupported File Types Must Fail Clearly

Decision:

Do not treat unsupported file types as clean zero-finding audits.

Reason:

A zero-finding report implies that a review was actually performed. For the
current Python-only MVP, unsupported inputs should fail clearly and state that
no audit was performed.

Status:

Accepted

## 2026-06-22

### Expand Only the Text Extractor for Multi-language Support

Decision:

Implement the required multi-language expansion by changing only the Text
Extractor layer and keeping the rest of the pipeline contract unchanged.

Reason:

This preserves the explainable architecture and avoids dragging schema,
review-agent, prompt, report, or context-loading changes into an extraction
scope increase.

Status:

Accepted

### Treat Multi-language Support as Human-Written Text Extraction, Not Full Parsing

Decision:

Support common project files by extracting human-written text surfaces rather
than attempting full language parsing.

Reason:

The project goal is semantic review of comments and documentation, not general
purpose source understanding. Narrow extraction rules reduce complexity and
lower the risk of accidentally reviewing executable code or unrelated syntax.

Status:

Accepted

### Keep JSX and TSX Comment-Only in the MVP

Decision:

For `.jsx` and `.tsx`, extract only JavaScript-style comments in the MVP and
do not attempt full JSX or TSX text parsing.

Reason:

Visible JSX text, nested markup, and mixed syntax introduce parsing complexity
that is outside the current extraction-only phase. Comment-only support meets
the narrow MVP goal more safely.

Status:

Accepted

### Exclude Markdown Fenced Code Blocks from Reviewable Text

Decision:

Treat Markdown prose as reviewable text, but exclude fenced code blocks from
extraction in the MVP.

Reason:

Fenced code blocks are often examples or copied snippets rather than
human-written repository guidance. Excluding them keeps Markdown extraction
focused on headings, paragraphs, lists, and blockquotes.

Status:

Accepted

### Evaluate Semantic Correctness Rather Than Exact Wording

Decision:

Judge evaluation matches based on whether the correct text or line range,
category, and concern were identified, rather than requiring exact explanation
or recommendation wording.

Reason:

The project evaluates semantic review quality, not exact sentence generation.
Strict wording equality would under-measure correct behavior and over-penalize
reasonable phrasing differences, especially for Gemini.

Status:

Accepted

### Evaluate Deterministic and Gemini Backends Separately

Decision:

Report deterministic and Gemini evaluation results separately instead of
combining them into one blended score.

Reason:

The two backends serve different goals. Deterministic evaluation validates
pipeline correctness and repeatability, while Gemini evaluation validates
semantic reasoning and contextual judgment.

Status:

Accepted

### Commit Evaluation Results as Capstone Evidence

Decision:

Commit evaluation result artifacts to the repository.

Reason:

Reviewers should be able to inspect evaluation evidence without rerunning the
project. In this project, evaluation outputs are part of the capstone evidence
package rather than disposable local runtime files.

Status:

Accepted

## 2026-06-23

### Keep Flash as Default but Recommend Pro for Reliability-Sensitive Gemini Use

Decision:

Keep `gemini-2.5-flash` as the default Gemini model, but recommend
`gemini-2.5-pro` for reliability-sensitive Gemini validation, evaluation, and
demo use.

Reason:

The documented reliability investigation found intermittent Flash
`503 UNAVAILABLE` failures, while prior manual diagnostics showed Pro
completed 5/5 cycles across direct smoke, direct realistic prompt, and
ADK-backed review-path checks. The same investigation also documented higher
observed latency for Pro and the likelihood of different cost characteristics.
Keeping Flash as the default preserves current lightweight project behavior,
while recommending Pro acknowledges the stronger reliability evidence without
overstating the latency and cost tradeoff.

Status:

Accepted
