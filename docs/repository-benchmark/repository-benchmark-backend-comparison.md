# Repository Benchmark Backend Comparison

## Executive Summary

The project includes two evaluation backends because they serve different
engineering purposes. The deterministic backend provides a reproducible
baseline for regression checking and evaluation stability. The Gemini backend
provides the live semantic review path that interprets repository context more
like a human reviewer.

The repository benchmark shows why both remain useful. Deterministic and Gemini
did not behave like interchangeable versions of the same system. They exposed
different strengths, different failure modes, and different kinds of evidence
about the current Semantic Compliance Review Agent.

## Repository Benchmark Results

| Backend | Precision | Recall | True Positives | False Positives | False Negatives |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deterministic | `0.55` | `0.22` | `11` | `9` | `38` |
| Gemini | `0.51` | `0.82` | `40` | `38` | `9` |

## Behavioral Comparison

The deterministic backend behaved like a constrained baseline. It was
predictable, conservative in output volume, and strongest on explicit
secret-style reminders and configured internal codename references. It showed
limited semantic understanding outside those patterns and often collapsed
mixed comment blocks into one dominant finding or no finding at all.

The Gemini backend behaved like a broader semantic reviewer. It used contextual
interpretation across files, docstrings, comments, and partner-facing framing.
It surfaced findings in all supported categories and often treated the
repository as coherent review material rather than isolated benchmark lines. It
also showed a conservative disclosure mindset, especially around internal
project naming and external-sharing context, and it regularly produced
additional findings beyond the benchmark's expected JSON.

## Strengths

### Deterministic Strengths

- Reproducible and stable as an evaluation baseline.
- Reliable on explicit secret-like TODOs and direct configured codename
  references.
- Easier to interpret when investigating regressions because the behavior is
  narrow and predictable.
- Less prone to broad contextual expansion than the Gemini path.

### Gemini Strengths

- Stronger semantic repository review coverage across compliance, reputation,
  professionalism, intellectual-property, codename, and security findings.
- Better at engaging with realistic repository context instead of depending
  only on obvious trigger wording.
- More likely to surface the intended concerns in mixed or nuanced repository
  prose.
- Able to produce broader human-review style observations when the benchmark
  context suggests adjacent risks.

## Limitations

### Deterministic Limitations

- Limited semantic reach outside explicit security-style and codename-style
  patterns.
- Weak coverage for compliance, reputation, professionalism, and
  intellectual-property concerns in realistic repository language.
- Frequent dominant-finding collapse in mixed comment blocks.
- Missed entire groups of prose-heavy cases with no findings returned.

### Gemini Limitations

- High rate of additional findings that exceed benchmark expectations.
- Strong tendency to over-report internal codename exposure in file headers,
  docstrings, and externally adjacent descriptive text.
- More category drift between nearby concepts such as reputation,
  professionalism, and compliance.
- More likely to split one expected concern into multiple findings, which
  reduces strict benchmark alignment even when the observations are reasonable.

## Engineering Findings

The repository benchmark taught that repository context changes the evaluation
story substantially for both systems. The deterministic backend confirmed the
value of a reproducible baseline, but it also showed that a narrow pattern
driven path leaves much of the realistic risk surface uncovered. The Gemini
backend showed that semantic reasoning can recover most of that missing
coverage, but at the cost of looser alignment with strict benchmark counts and
category boundaries.

The comparison also highlights that benchmark realism matters. In the small
synthetic benchmark, narrow behavior can still look useful because the cases
are isolated and explicit. In the repository benchmark, contextual language,
mixed findings, and overlapping categories expose the difference between
baseline detection and broader semantic review much more clearly.

Category substitutions and additional observations were especially important
engineering signals. Deterministic mostly failed by omission. Gemini more often
failed by expansion, category drift, or finer-grained decomposition. Those are
different failure modes and they should be interpreted differently.

## Human Review Perspective

The project philosophy is not to automatically decide whether a repository is
acceptable. The goal is to surface meaningful review findings, assist a human
reviewer, and reduce the likelihood that important issues are missed.

From that perspective, the repository benchmark is useful because it shows two
different support modes. Deterministic offers a narrow, repeatable baseline
that can be trusted for consistent regression checking. Gemini offers a broader
semantic review style that is more willing to infer risk from context and
surface additional observations.

The Gemini analysis showed that some strict benchmark false positives are also
reasonable additional observations for a human reviewer. That does not change
the benchmark score, but it does matter when interpreting practical usefulness.
Broader semantic review can produce extra findings that are costly in strict
evaluation terms while still being defensible as human-review assistance.

## Why Two Backends Exist

The deterministic backend exists for reproducible evaluation, baseline
comparison, and regression testing. It makes the system measurable in a stable
way even when live model behavior is variable.

The Gemini backend exists for the actual semantic review workflow. It brings
contextual understanding, broader category coverage, and the ability to reason
about repository language that does not map cleanly to narrow patterns.

The repository benchmark validates the engineering purpose of keeping both.
Deterministic makes the system testable and explainable. Gemini makes the
system capable of the deeper repository review behavior the project is intended
to support.

## Final Conclusion

The main lesson from the repository benchmark is that the two backends provide
different but complementary forms of value. The deterministic backend gives the
project a reproducible baseline and exposes where narrow pattern-based review
stops being sufficient. The Gemini backend demonstrates the semantic repository
review capability that the project is ultimately trying to exercise, while also
showing the tradeoff that broader contextual reasoning is less tightly aligned
with strict benchmark exactness. Together, the two analyses validate why both
backends remain part of the project and why a human-in-the-loop review
philosophy is still necessary.

## Key Engineering Takeaway

The repository benchmark showed that deterministic evaluation provides a stable baseline, 
while Gemini provides substantially broader semantic reasoning. The project therefore uses 
deterministic evaluation to measure behaviour and Gemini to perform practical repository review. 
The two backends are complementary rather than interchangeable.