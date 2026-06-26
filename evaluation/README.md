# Evaluation Artifacts

This directory contains the evaluation dataset, expected outputs, result
artifacts, and Gemini diagnostic tooling for the Semantic Compliance Review
Agent.

## Directory Roles

- `cases/`: input files used for evaluation
- `expected/`: expected outcome JSON files
- `results/`: committed evaluation result artifacts

Important files:

- `evaluation/run.py`
- `evaluation/diagnose_gemini.py`
- `evaluation/results/deterministic-results.md`
- `evaluation/results/gemini-results.md`
- `evaluation/results/deterministic-repository_benchmark-results.md`
- `evaluation/results/gemini-repository_benchmark-results.md`

## What The Evaluation Covers

The original committed benchmark is a 10-case dataset covering:

- safe cases
- security risks
- internal codename exposure
- professionalism risks
- false-positive handling
- multi-language extraction coverage

The repository also includes a repository-style benchmark under
`evaluation/cases/repository_benchmark/` with matching expected JSON files
under `evaluation/expected/repository_benchmark/`.

The original dataset remains the small baseline benchmark. The repository
benchmark adds broader engineering evidence on coherent repository content.

Realistic sample files under `examples/` are useful for demo-style validation,
but they are not part of the scored benchmark suite.

## Run Deterministic Evaluation

Full run:

```text
python -m evaluation.run --backend deterministic
```

Repository benchmark run:

```text
python -m evaluation.run --backend deterministic --benchmark repository_benchmark
```

Single case:

```text
python -m evaluation.run --backend deterministic --case security_python
```

Selected subset:

```text
python -m evaluation.run --backend deterministic --cases security_python,security_javascript
```

Benchmark selection:

- Omit `--benchmark` or use `--benchmark default` for the original top-level dataset.
- Use `--benchmark <folder-name>` for a benchmark folder under `evaluation/cases/`
  with matching expected files under `evaluation/expected/`.

## Run Gemini Evaluation

Paced Gemini run:

```text
python -m evaluation.run --backend gemini --delay-seconds 15
```

Paced Gemini repository benchmark run:

```text
python -m evaluation.run --backend gemini --benchmark repository_benchmark --delay-seconds 15
```

Paced Gemini single-case run:

```text
python -m evaluation.run --backend gemini --case security_python --delay-seconds 15
```

Recommended reliability-sensitive run, PowerShell:

```text
$env:GEMINI_MODEL="gemini-2.5-pro"
python -m evaluation.run --backend gemini --delay-seconds 15
```

Recommended reliability-sensitive run, Bash:

```text
export GEMINI_MODEL="gemini-2.5-pro"
python -m evaluation.run --backend gemini --delay-seconds 15
```

Results are written to:

- `evaluation/results/deterministic-results.md`
- `evaluation/results/gemini-results.md`
- `evaluation/results/deterministic-repository_benchmark-results.md`
- `evaluation/results/gemini-repository_benchmark-results.md`

During execution, the runner also writes incremental progress artifacts:

- `*-progress.json`: machine-readable completed-case progress saved after each evaluated file
- `*-partial.md`: a clearly marked partial report that is updated during the run and retained if execution is interrupted

Console diagnostics now include compact failure summaries such as expected versus
returned finding counts, missing findings, unexpected findings, and backend or
JSON/schema failures.

## GEMINI_MODEL

The shared `GEMINI_MODEL` environment variable controls the Gemini model for
normal review and evaluation runs.

Default model:

- `gemini-2.5-flash`

During project evaluation, `gemini-2.5-pro` produced the most consistent
results and was therefore used for the committed Gemini evaluation snapshots
and reliability-sensitive demos:

- `gemini-2.5-pro`

The committed Gemini snapshot artifact in this repository was captured with
`gemini-2.5-pro`.

## Diagnostics

Use the Gemini diagnosis tool when you need to compare direct Gemini access
with the ADK-backed review path.

Examples:

```text
python -m evaluation.diagnose_gemini
python -m evaluation.diagnose_gemini --repeat 5 --delay-seconds 15
python -m evaluation.diagnose_gemini --model gemini-2.5-flash --repeat 3
python -m evaluation.diagnose_gemini --model gemini-2.5-pro --repeat 5 --delay-seconds 15
```

The diagnostic reports:

- PASS / FAIL by test path
- elapsed duration
- selected Gemini model
- which API-key variable is in use
- concise previews or error summaries

## Notes

- Deterministic and Gemini results are evaluated separately.
- Gemini results should be interpreted as snapshots rather than perfectly reproducible benchmarks.
- `--delay-seconds 15` is a reasonable starting point for paced Gemini runs on rate-limited accounts.

For benchmark philosophy and matching rules, see `docs/evaluation-plan.md`.

Related engineering analyses:

- `docs/repository-benchmark/repository-benchmark-review.md`
- `docs/repository-benchmark/repository-benchmark-review-gemini.md`
- `docs/repository-benchmark/repository-benchmark-backend-comparison.md`
