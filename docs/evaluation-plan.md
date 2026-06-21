# Evaluation Plan

This document describes the planned evaluation approach for the Semantic
Compliance Review Agent.

Evaluation is not implemented yet.

Formal evaluation is planned for Phase 8.

## Current Status

Implemented now:

- manual sample input
- manual sample output
- deterministic backend for stable local checks
- live Gemini verification documented in the build log

Not implemented yet:

- evaluation harness
- evaluation CLI command
- expected-output comparison
- precision/recall reporting
- committed evaluation cases

This plan is intentionally honest about that gap.

## Evaluation Goal

The evaluation phase should demonstrate that the agent produces useful,
traceable findings on a hand-built set of review cases.

The primary goal is not benchmark scale.

The primary goal is submission-quality evidence that:

- the system catches obvious risky text
- the system can return zero findings when appropriate
- structured findings are inspectable
- the review behavior is explainable

## Planned Evaluation Scope

Phase 8 should include hand-built evaluation cases covering at least:

- clean zero-finding case
- configured sensitive-term match case
- semantic security-risk case
- hybrid case combining term match and semantic risk
- suggested-replacement case
- professionalism-risk case
- compliance-risk case if a stable example is available

Once broader file support is implemented, evaluation should also include:

- unsupported file behavior case
- non-Python supported-file cases

## Planned Evaluation Structure

Planned repository structure:

```text
evaluation/
  cases/
  expected/
```

Planned approach:

1. Create a small set of hand-written inputs.
2. Define expected findings or expected no-finding outcomes.
3. Run the pipeline against each case.
4. Compare actual findings with expected results.
5. Record a simple evaluation summary.

## Expected Case Types

### Zero-Finding Clean Case

Purpose:

Show that obviously safe comments and docstrings do not automatically produce
findings.

### Sensitive Term Match Case

Purpose:

Verify that configured sensitive terms can trigger a high-confidence
term-driven finding.

### Semantic Risk Case

Purpose:

Verify that risky wording can be flagged even when no configured sensitive term
is present.

### Hybrid Case

Purpose:

Verify that the system can distinguish a plain term match from a term match
plus added semantic risk.

### Suggested Replacement Case

Purpose:

Verify that obvious high-confidence cases may include a safe suggested
replacement and that the report displays it clearly.

### Unsupported File Behavior Case

Purpose:

Once broader extraction support is added, verify that unsupported file types
fail or skip in the documented way rather than behaving ambiguously.

## Planned Metrics

If feasible within capstone scope, Phase 8 should report simple review metrics
such as:

- correct detections
- false positives
- false negatives
- approximate precision
- approximate recall

These should be treated as small-project evaluation signals, not as formal
scientific claims.

## Evaluation Constraints

The evaluation phase should remain aligned with the rest of the project:

- no automatic source modification
- findings remain advisory
- deterministic mode may be used for stable local checks
- Gemini may be used for live-path verification where appropriate

## What This Document Does Not Claim

This document does not claim that evaluation is already complete.

It does not claim that metrics are already available.

It does not claim that the current repository contains a finished benchmark
suite.

Those items belong to Phase 8 work.
