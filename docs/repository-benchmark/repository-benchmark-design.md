# Repository Benchmark Design

## Purpose

The original benchmark successfully verified that the evaluation pipeline
worked end to end, including expected-output matching, metric calculation, and
artifact generation. It also provided a small, understandable dataset for early
validation of the project.

That benchmark, however, is built from small synthetic examples. The next
benchmark design aims to represent more realistic repository usage for the
Semantic Compliance Review Agent.

The objective of this redesign is not simply to add more cases. The goal is to
produce more meaningful evaluation evidence by using inputs that better reflect
how the agent would be used on believable software project files.

## Design Goals

- Simulate realistic repository review
- Measure semantic understanding instead of keyword matching
- Increase variety of findings
- Exercise all supported finding categories
- Include both positive and negative examples
- Produce evaluation evidence that is representative of real usage

## Benchmark Philosophy

The redesigned benchmark should evaluate both strengths and limitations of the
current system.

It is not designed to maximize benchmark scores or to make the agent appear
stronger than it is. False negatives and false positives are useful
observations because they show where the review system succeeds, where it is
fragile, and where further refinement may be needed.

Realistic repository content is preferred over artificial examples. Benchmark
files should resemble source files and documentation that a developer might
actually write, review, and commit. The benchmark should therefore prioritize
believable content, plausible project structure, and natural writing patterns
over exaggerated toy cases.

## Repository Structure

The planned benchmark should use a repository-style layout rather than a
collection of isolated micro-cases.

Target shape:

- 20 repository-style files
- approximately 100 to 200 lines per file
- mixed supported file types
- believable project content
- consistent formatting and naming conventions

Suggested file types:

- Python (`.py`)
- TypeScript (`.ts`)
- JavaScript (`.js`)
- Markdown (`.md`)
- HTML (`.html`)

Additional text-based formats may be added later if they fit the project scope
and the extraction rules remain clear.

## Finding Distribution

Each file should contain between 0 and 4 expected findings.

Across the full benchmark, the expected total should be approximately 45 to 60
findings.

All supported categories should appear multiple times:

- `CDX` - Internal Codename Exposure
- `SEC` - Security Risk
- `PRO` - Professionalism Risk
- `CMP` - Compliance Risk
- `IPR` - Intellectual Property Risk
- `REP` - Reputation Risk

No single category should dominate the benchmark. The benchmark should remain
balanced enough to show whether the system performs across the supported risk
surface rather than only on the easiest or most common finding type.

## Difficulty Levels

The redesigned benchmark should intentionally include multiple difficulty
levels.

### Easy

Obvious findings that should be identified reliably when the system is working
as intended.

### Medium

Context-dependent findings where wording alone is not enough and surrounding
file meaning helps determine whether a finding should be reported.

### Hard

Semantic findings that require interpretation rather than simple keyword
recognition. These cases should test whether the agent can reason about
implication, tone, disclosure risk, or intent in a more realistic way.

### False Positive Scenarios

Files or sections that intentionally resemble risky content but should not be
reported.

These scenarios are important for evaluating precision. A benchmark that only
contains obvious positives can overstate capability by failing to test whether
the system can avoid over-reporting harmless repository text.

## Evaluation Metrics

The evaluation methodology remains unchanged.

Metrics continue to include:

- True Positives
- False Positives
- False Negatives
- Precision
- Recall
- Cases Passed
- Cases Failed

This redesign changes the benchmark inputs, not the metric definitions or the
overall evaluation method. The goal is to improve the realism and meaning of
the measured evidence while keeping the scoring approach stable.

## Expected Benefits

Expected benefits of the redesigned benchmark include:

- more representative evaluation coverage
- greater finding diversity
- better semantic coverage
- more realistic repository simulation
- stronger evaluation evidence
- clearer demonstration of the agent's capabilities and limitations

These benefits should not be interpreted as a promise of higher scores. The
value of the redesign is that it is intended to make benchmark results more
meaningful and more aligned with realistic usage.

## Out of Scope

This document does not include:

- benchmark implementation
- repository benchmark files
- expected JSON outputs
- evaluation code changes
- metric calculation changes

Those items belong to later implementation phases rather than this design
specification.
