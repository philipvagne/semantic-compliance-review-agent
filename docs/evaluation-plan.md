# Evaluation Plan

This document describes the approved evaluation design for the Semantic
Compliance Review Agent.

Phase 8A documented the design.

Phase 8B is implementing the evaluation harness and artifacts described here in
small slices.

The repository now contains the Phase 8B.1 foundation structure:

- `evaluation/__init__.py`
- `evaluation/README.md`
- `evaluation/cases/`
- `evaluation/expected/`
- `evaluation/results/`

The repository now also contains the initial Phase 8B.2 dataset:

- 10 evaluation case files in `evaluation/cases/`
- 10 matching expected-output JSON files in `evaluation/expected/`

The repository now also contains the initial Phase 8B.3 runner output:

- `evaluation/run.py`
- `evaluation/results/deterministic-results.md`

## Current Status

Implemented now:

- manual sample input
- manual sample output
- deterministic backend for stable local checks
- live Gemini verification documented in the build log
- approved evaluation design for the next implementation step
- committed initial evaluation cases
- committed initial expected-output JSON files
- deterministic evaluation runner
- deterministic expected-output comparison
- deterministic precision and recall reporting
- committed deterministic evaluation results artifact

Not implemented yet:

- Gemini evaluation execution
- committed Gemini evaluation snapshot

This document is intentionally honest about that gap.

## Evaluation Goal

The evaluation phase should provide credible, repeatable evidence that:

- the extraction pipeline works correctly
- the review pipeline works correctly
- the agent can identify expected risks
- the agent can avoid obvious false positives
- the results can be measured and reported

The goal is not benchmark scale.

The goal is submission-quality evidence for a small, explainable capstone
project.

## Evaluation Philosophy

The evaluation should measure whether the agent understood the risk, not
whether it produced exact expected wording.

Exact explanation and recommendation text matches should not be required.

Evaluation should focus on semantic correctness:

- whether the right text or line range was targeted
- whether the right category was identified
- whether the explanation is meaningfully related to the expected concern

## Backend Strategy

The deterministic and Gemini backends should be evaluated separately.

### Deterministic Backend Purpose

- validate pipeline correctness
- validate extraction behavior
- validate repeatable rule-based findings
- provide committed precision and recall evidence

### Gemini Backend Purpose

- validate semantic reasoning
- validate contextual understanding
- validate category selection

Deterministic and Gemini results should not be collapsed into one vague score.

## Supported Evaluation Coverage

The evaluation should cover the currently supported file types:

- `.py`
- `.js`
- `.ts` / `.tsx` through JavaScript-family coverage
- `.html`
- `.md`

Coverage does not need to be equal.

Coverage does need to be representative.

The target size is 10 to 14 total evaluation cases.

The goal is credible coverage, not a large benchmark suite.

## Evaluation Case Types

### 1. Clean File

Purpose:

Verify that safe content produces zero findings.

Expected:

`0` findings.

### 2. Security Risk

Examples:

- temporary password
- hard-coded secret
- sensitive credential reference

Expected:

`SECURITY_RISK` finding.

### 3. Internal Naming Risk

Examples:

- confidential project names
- internal codenames
- restricted initiatives

Expected:

`INTERNAL_CODENAME_EXPOSURE` finding.

### 4. Professionalism Risk

Examples:

- unfinished TODO comments
- placeholder release notes
- unprofessional language

Expected:

`PROFESSIONALISM_RISK` finding.

### 5. Suggested Replacement Case

Purpose:

Verify recommendation quality for obvious high-confidence cases.

Expected:

The finding includes a reasonable `suggested_replacement`.

### 6. Documentation False-Positive Case

Purpose:

Measure whether the agent incorrectly flags safe documentation.

Example:

README-style documentation containing:

- `GOOGLE_API_KEY`
- `GEMINI_API_KEY`
- API endpoint references
- credential setup instructions

in safe instructional context.

Expected:

Zero findings or near-zero findings.

This case is important because README self-review during development exposed
possible over-flagging of safe instructional credential examples.

### 7. Multi-Language Coverage Cases

Purpose:

Verify extraction and review behavior across supported file types.

Include:

- Python
- JavaScript-family
- HTML
- Markdown

Expected:

Expected findings are produced consistently regardless of file type.

### Optional Additional Cases

If time allows and examples remain stable:

- configured sensitive-term match case
- hybrid case combining term match and semantic risk
- compliance-risk case

## Matching Rules

Evaluation should not require exact wording matches.

A finding should count as a match when:

1. The expected reviewable text was identified, or the correct line range was
   targeted.
2. The expected category was identified.
3. The explanation is meaningfully related to the expected concern.

## Severity Rules

Severity is secondary.

Example:

- expected: `HIGH`
- actual: `MEDIUM`

This may still count as a successful detection.

Primary concern:

Was the correct risk detected?

Secondary concern:

Was the severity reasonable?

## Evaluation Metrics

The evaluation should report at least:

- True Positive (TP): expected finding exists and the agent correctly
  identifies it
- False Positive (FP): agent reports a finding that should not exist
- False Negative (FN): expected finding exists and the agent fails to identify
  it
- Precision: `TP / (TP + FP)`
- Recall: `TP / (TP + FN)`

Metric purpose:

- Precision answers: how trustworthy are reported findings?
- Recall answers: how many expected findings were detected?

If time allows, the final evaluation writeup may also include supporting counts
such as:

- total cases run
- total findings expected
- total findings produced

These metrics should be treated as small-project evaluation signals, not as
formal scientific claims.

## Expected Output Schema

Phase 8B should implement expected-case JSON files against a small, explicit
schema.

Example risky case:

```json
{
  "case_id": "security_python",
  "expected_findings": [
    {
      "category": "SECURITY_RISK",
      "target_text_contains": "temporary password",
      "line_start": 3,
      "line_end": 3,
      "line_range_approximate": true,
      "requires_suggested_replacement": false
    }
  ],
  "expected_finding_count_min": 1,
  "expected_finding_count_max": 2
}
```

Example clean or false-positive case:

```json
{
  "case_id": "documentation_false_positive",
  "expected_findings": [],
  "expected_finding_count_min": 0,
  "expected_finding_count_max": 0
}
```

Field meanings:

- `case_id`: stable identifier for the evaluation case
- `expected_findings`: expected matched findings for the case
- `category`: expected finding category
- `target_text_contains`: short anchor text that should appear in the matched
  source text
- `line_start`: expected start line for the matched finding
- `line_end`: expected end line for the matched finding
- `line_range_approximate`: whether near-line matching is acceptable
- `requires_suggested_replacement`: whether the finding should include a
  reasonable suggested replacement
- `expected_finding_count_min`: lower bound for acceptable finding count
- `expected_finding_count_max`: upper bound for acceptable finding count

## Evaluation Artifact Structure

Planned repository structure:

```text
evaluation/
  cases/
  expected/
  results/
```

Examples:

- `evaluation/cases/security_python.py`
- `evaluation/cases/security_javascript.js`
- `evaluation/cases/internal_codename_markdown.md`
- `evaluation/cases/clean_html.html`
- `evaluation/cases/documentation_false_positive.md`

- `evaluation/expected/security_python.json`
- `evaluation/expected/security_javascript.json`
- `evaluation/expected/clean_html.json`
- `evaluation/expected/documentation_false_positive.json`

- `evaluation/results/deterministic-results.md`
- `evaluation/results/gemini-results.md`

## Result Policy

Evaluation results should be committed to the repository.

Reason:

Capstone reviewers should be able to inspect evaluation evidence without
rerunning the project.

Evaluation artifacts are capstone evidence, not temporary runtime files.

## Evaluation Constraints

The evaluation phase should remain aligned with the rest of the project:

- no automatic source modification
- findings remain advisory
- deterministic mode may be used for stable local checks
- Gemini may be used for live-path verification where appropriate
- no prompt tuning as part of the baseline evaluation implementation
- no extraction-behavior changes as part of the baseline evaluation implementation

## Explicit Non-Goals for Phase 8A

Phase 8A does not:

- implement the evaluation harness
- create evaluation cases
- create expected JSON files
- generate metrics
- tune prompts
- modify Gemini behavior
- modify extraction behavior
- modify report generation
- modify runtime architecture

## What This Document Does Not Claim

This document does not claim that evaluation is already complete.

It does not claim that metrics are already available.

It does not claim that the current repository contains a finished benchmark
suite.

Those items belong to later Phase 8 implementation work.
