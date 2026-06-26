"""Run committed evaluation cases against the existing review pipeline.

Purpose:
- Execute the committed evaluation dataset through the supported evaluation backends.

Input:
- Evaluation case files from `evaluation/cases/`.
- Matching expected JSON files from `evaluation/expected/`.
- One required backend flag for deterministic or Gemini evaluation.
- One optional benchmark selection for the default or a named benchmark folder.
- The current Gemini model selection when the Gemini backend is used.
- One optional delay value between evaluation cases.
- Optional selection of one case or multiple cases by case ID.

Output:
- Concise console progress lines and summary metrics.
- One Markdown results file under `evaluation/results/`.
- Incremental progress artifacts that preserve completed case results.

Responsibilities:
- Validate the supported evaluation CLI mode.
- Resolve the selected benchmark case and expected-output directories.
- Load evaluation cases and matching expected outputs.
- Run the existing pipeline with the selected backend.
- Preserve backend and model metadata in the committed results artifact.
- Persist completed evaluation progress after each successfully evaluated case.
- Optionally pause between cases when the user requests pacing.
- Optionally limit the run to selected cases.
- Compare actual findings to expected findings with simple matching rules.
- Calculate TP, FP, FN, precision, and recall.
- Write a human-readable committed evaluation artifact.

Non-responsibilities:
- Modify runtime review behavior.
- Create new evaluation cases automatically.
- Tune prompts or schemas.
- Change evaluation methodology.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone
from pathlib import Path
import json
import time

from pydantic import BaseModel
from pydantic import ValidationError

from src.agent_review import AgentReviewError
from src.agent_review import configure_backend
from src.agent_review import get_backend_display_name
from src.agent_review import get_model_display_name
from src.agent_review import review
from src.context_loader import ContextLoadError
from src.context_loader import load_review_context
from src.file_reader import FileReadError
from src.file_reader import read_file
from src.schemas import Finding
from src.text_extractor import ExtractionError
from src.text_extractor import extract_reviewable_text


REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = REPO_ROOT / "evaluation" / "cases"
EXPECTED_DIR = REPO_ROOT / "evaluation" / "expected"
RESULTS_DIR = REPO_ROOT / "evaluation" / "results"
SUPPORTED_EVALUATION_BACKENDS = ("deterministic", "gemini")
SUPPORTED_CASE_SUFFIXES = {".py", ".ts", ".js", ".md", ".html"}


class ExpectedFinding(BaseModel):
    category: str
    target_text_contains: str
    line_start: int
    line_end: int
    line_range_approximate: bool
    requires_suggested_replacement: bool


class ExpectedCase(BaseModel):
    case_id: str
    expected_findings: list[ExpectedFinding]
    expected_finding_count_min: int
    expected_finding_count_max: int


@dataclass
class MatchResult:
    matched: bool
    reason: str


@dataclass
class ExpectedFindingOutcome:
    expected: ExpectedFinding
    matched: bool
    matched_actual: Finding | None
    reason: str


@dataclass
class ActualFindingOutcome:
    actual: Finding
    matched: bool
    reason: str


@dataclass
class CaseResult:
    case_filename: str
    case_id: str
    case_path: str
    expected_path: str
    expected_case: ExpectedCase
    actual_findings: list[Finding]
    expected_outcomes: list[ExpectedFindingOutcome]
    actual_outcomes: list[ActualFindingOutcome]
    tp: int
    fp: int
    fn: int
    case_passed: bool
    count_in_range: bool


@dataclass(frozen=True)
class BenchmarkPaths:
    benchmark_name: str
    cases_dir: Path
    expected_dir: Path
    recursive: bool


@dataclass
class RunArtifacts:
    results_path: Path
    partial_report_path: Path
    progress_path: Path


@dataclass
class EvaluationRunState:
    backend: str
    benchmark_name: str
    selected_case_ids: list[str] | None
    planned_case_ids: list[str]
    artifacts: RunArtifacts
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    )
    completed_results: list[CaseResult] = field(default_factory=list)
    interruption_reason: str | None = None
    completed_at: str | None = None

    @property
    def model(self) -> str:
        return get_model_display_name() or "(unknown)"

    @property
    def remaining_case_ids(self) -> list[str]:
        completed_case_ids = {
            result.case_id for result in self.completed_results
        }
        return [
            case_id for case_id in self.planned_case_ids
            if case_id not in completed_case_ids
        ]


def _parse_delay_seconds(value: str) -> float:
    try:
        delay_seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid delay value '{value}'. Use a non-negative integer or float."
        ) from exc

    if delay_seconds < 0:
        raise argparse.ArgumentTypeError(
            "Delay seconds must be non-negative."
        )

    return delay_seconds


def _parse_case_list(value: str) -> list[str]:
    case_ids = [item.strip() for item in value.split(",")]
    normalized_case_ids = [item for item in case_ids if item]
    if not normalized_case_ids:
        raise argparse.ArgumentTypeError(
            "Cases list must include at least one non-empty case ID."
        )
    return normalized_case_ids


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run committed evaluation cases through a supported backend."
    )
    parser.add_argument(
        "--backend",
        required=True,
        help="Evaluation backend to use. Supported values: deterministic, gemini.",
    )
    parser.add_argument(
        "--benchmark",
        default="default",
        help=(
            "Benchmark to run. Use 'default' for the original top-level dataset "
            "or the name of a benchmark folder under evaluation/cases/."
        ),
    )
    selection_group = parser.add_mutually_exclusive_group()
    selection_group.add_argument(
        "--case",
        help="Run exactly one evaluation case by case ID or file stem.",
    )
    selection_group.add_argument(
        "--cases",
        type=_parse_case_list,
        help="Run multiple evaluation cases by comma-separated case IDs or file stems.",
    )
    parser.add_argument(
        "--delay-seconds",
        type=_parse_delay_seconds,
        default=0.0,
        help="Optional pause between evaluation cases. Defaults to 0 seconds.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.backend not in SUPPORTED_EVALUATION_BACKENDS:
        raise SystemExit(
            "Unsupported evaluation backend. Supported values are "
            "'deterministic' and 'gemini'."
        )

    run_state: EvaluationRunState | None = None

    try:
        configure_backend(args.backend)
        review_context = load_review_context()
        benchmark_paths = _resolve_benchmark_paths(args.benchmark)
        selected_case_ids = _resolve_selected_case_ids(args)
        case_results, run_state = _run_all_cases(
            review_context,
            backend=args.backend,
            benchmark_paths=benchmark_paths,
            delay_seconds=args.delay_seconds,
            selected_case_ids=selected_case_ids,
        )
        summary = _build_summary(
            case_results,
            backend=args.backend,
            benchmark_name=benchmark_paths.benchmark_name,
            selected_case_ids=selected_case_ids,
        )
        _write_results_markdown(
            case_results,
            summary,
            backend=args.backend,
            benchmark_name=benchmark_paths.benchmark_name,
        )
        _finalize_successful_run(run_state)
        _clear_partial_artifacts(run_state.artifacts)
    except KeyboardInterrupt as exc:
        raise SystemExit("Evaluation interrupted: Keyboard interrupt.") from exc
    except (
        AgentReviewError,
        ContextLoadError,
        FileReadError,
        ExtractionError,
        ValidationError,
        ValueError,
        OSError,
    ) as exc:
        if run_state is not None:
            _finalize_interrupted_run(
                run_state,
                interruption_reason=_format_exception_summary(exc),
            )
        raise SystemExit(f"Evaluation failed: {exc}") from exc

    print(
        f"{summary['cases_run']} {_pluralize_case(summary['cases_run'])} run - Precision: "
        f"{summary['precision']:.2f}, Recall: {summary['recall']:.2f}"
    )


def _resolve_selected_case_ids(args: argparse.Namespace) -> list[str] | None:
    if args.case:
        return [args.case.strip()]
    if args.cases:
        return args.cases
    return None


def _resolve_benchmark_paths(benchmark_name: str) -> BenchmarkPaths:
    normalized_name = benchmark_name.strip()
    if not normalized_name:
        raise ValueError("Benchmark name must not be empty.")

    if normalized_name == "default":
        return BenchmarkPaths(
            benchmark_name="default",
            cases_dir=CASES_DIR,
            expected_dir=EXPECTED_DIR,
            recursive=False,
        )

    cases_dir = CASES_DIR / normalized_name
    expected_dir = EXPECTED_DIR / normalized_name
    if not cases_dir.exists():
        raise ValueError(
            f"Benchmark cases directory not found: {cases_dir.as_posix()}"
        )
    if not expected_dir.exists():
        raise ValueError(
            f"Benchmark expected directory not found: {expected_dir.as_posix()}"
        )

    return BenchmarkPaths(
        benchmark_name=normalized_name,
        cases_dir=cases_dir,
        expected_dir=expected_dir,
        recursive=True,
    )


def _run_all_cases(
    review_context,
    *,
    backend: str,
    benchmark_paths: BenchmarkPaths,
    delay_seconds: float,
    selected_case_ids: list[str] | None,
) -> tuple[list[CaseResult], EvaluationRunState]:
    all_case_paths = _list_case_paths(benchmark_paths)
    case_paths = _select_case_paths(
        all_case_paths,
        selected_case_ids,
        benchmark_paths=benchmark_paths,
    )
    run_state = _initialize_run_state(
        backend=backend,
        case_paths=case_paths,
        benchmark_paths=benchmark_paths,
        selected_case_ids=selected_case_ids,
    )

    _print_selection_summary(
        case_paths,
        selected_case_ids,
        benchmark_paths=benchmark_paths,
    )

    try:
        for index, case_path in enumerate(case_paths):
            if index > 0 and delay_seconds > 0:
                print(f"Waiting {delay_seconds:g} seconds before the next case...")
                time.sleep(delay_seconds)

            try:
                result = _run_single_case(
                    case_path,
                    review_context,
                    benchmark_paths=benchmark_paths,
                )
            except KeyboardInterrupt:
                print(f"Running {case_path.name}... ERROR - keyboard interrupt")
                raise
            except Exception as exc:
                print(
                    f"Running {case_path.name}... ERROR - "
                    f"{_format_exception_summary(exc)}"
                )
                raise

            status = "PASS" if result.case_passed else "FAIL"
            diagnostic_summary = _build_case_diagnostic_summary(result)
            print(f"Running {case_path.name}... {status} - {diagnostic_summary}")
            run_state.completed_results.append(result)
            _persist_run_progress(run_state)
    except KeyboardInterrupt:
        _finalize_interrupted_run(
            run_state,
            interruption_reason="Keyboard interrupt.",
        )
        raise
    except Exception as exc:
        _finalize_interrupted_run(
            run_state,
            interruption_reason=_format_exception_summary(exc),
        )
        raise

    return run_state.completed_results, run_state


def _list_case_paths(benchmark_paths: BenchmarkPaths) -> list[Path]:
    if benchmark_paths.recursive:
        return sorted(
            path
            for path in benchmark_paths.cases_dir.rglob("*")
            if path.is_file() and path.suffix in SUPPORTED_CASE_SUFFIXES
        )
    return sorted(
        path
        for path in benchmark_paths.cases_dir.iterdir()
        if path.is_file() and path.suffix in SUPPORTED_CASE_SUFFIXES
    )


def _select_case_paths(
    all_case_paths: list[Path],
    selected_case_ids: list[str] | None,
    *,
    benchmark_paths: BenchmarkPaths,
) -> list[Path]:
    if not selected_case_ids:
        return all_case_paths

    path_by_identifier = _build_case_identifier_map(
        all_case_paths,
        benchmark_paths=benchmark_paths,
    )
    selected_paths: list[Path] = []
    missing_case_ids: list[str] = []

    for case_id in selected_case_ids:
        case_path = path_by_identifier.get(case_id)
        if case_path is None:
            missing_case_ids.append(case_id)
            continue
        selected_paths.append(case_path)

    if missing_case_ids:
        available_case_ids = ", ".join(sorted(path_by_identifier))
        missing_label = ", ".join(missing_case_ids)
        raise ValueError(
            f"Selected evaluation case(s) not found: {missing_label}. "
            f"Available case IDs: {available_case_ids}"
        )

    return selected_paths


def _build_case_identifier_map(
    case_paths: list[Path],
    *,
    benchmark_paths: BenchmarkPaths,
) -> dict[str, Path]:
    path_by_identifier: dict[str, Path] = {}
    stem_counts: dict[str, int] = {}

    for case_path in case_paths:
        stem_counts[case_path.stem] = stem_counts.get(case_path.stem, 0) + 1

    for case_path in case_paths:
        case_id = _case_id_for_path(case_path, benchmark_paths=benchmark_paths)
        path_by_identifier[case_id] = case_path
        if stem_counts[case_path.stem] == 1:
            path_by_identifier[case_path.stem] = case_path

    return path_by_identifier


def _case_id_for_path(case_path: Path, *, benchmark_paths: BenchmarkPaths) -> str:
    relative_path = case_path.relative_to(benchmark_paths.cases_dir)
    return relative_path.with_suffix("").as_posix()


def _print_selection_summary(
    case_paths: list[Path],
    selected_case_ids: list[str] | None,
    *,
    benchmark_paths: BenchmarkPaths,
) -> None:
    if not selected_case_ids:
        return

    if len(case_paths) == 1:
        print(
            "Running selected case: "
            f"{_case_id_for_path(case_paths[0], benchmark_paths=benchmark_paths)}"
        )
        return

    selected_summary = ", ".join(
        _case_id_for_path(path, benchmark_paths=benchmark_paths)
        for path in case_paths
    )
    print(f"Running {len(case_paths)} selected cases: {selected_summary}")


def _initialize_run_state(
    *,
    backend: str,
    case_paths: list[Path],
    benchmark_paths: BenchmarkPaths,
    selected_case_ids: list[str] | None,
) -> EvaluationRunState:
    case_ids = [
        _case_id_for_path(case_path, benchmark_paths=benchmark_paths)
        for case_path in case_paths
    ]
    artifacts = _build_run_artifacts(
        backend,
        benchmark_name=benchmark_paths.benchmark_name,
    )
    return EvaluationRunState(
        backend=backend,
        benchmark_name=benchmark_paths.benchmark_name,
        selected_case_ids=selected_case_ids,
        planned_case_ids=case_ids,
        artifacts=artifacts,
    )


def _build_run_artifacts(backend: str, *, benchmark_name: str) -> RunArtifacts:
    results_path = _build_results_path(backend, benchmark_name=benchmark_name)
    if benchmark_name == "default":
        artifact_stem = backend
    else:
        artifact_stem = f"{backend}-{benchmark_name.replace('/', '-')}"

    return RunArtifacts(
        results_path=results_path,
        partial_report_path=RESULTS_DIR / f"{artifact_stem}-partial.md",
        progress_path=RESULTS_DIR / f"{artifact_stem}-progress.json",
    )


def _run_single_case(
    case_path: Path,
    review_context,
    *,
    benchmark_paths: BenchmarkPaths,
) -> CaseResult:
    relative_case_path = case_path.relative_to(benchmark_paths.cases_dir)
    expected_path = benchmark_paths.expected_dir / relative_case_path.with_suffix(".json")
    if not expected_path.exists():
        raise ValueError(
            f"Missing expected evaluation file for {case_path.name}: "
            f"{expected_path.as_posix()}"
        )

    expected_case = _load_expected_case(expected_path)
    case_id = _case_id_for_path(case_path, benchmark_paths=benchmark_paths)
    if expected_case.case_id != case_path.stem:
        raise ValueError(
            f"Expected case_id mismatch for {case_path.name}: "
            f"expected '{case_path.stem}' but found '{expected_case.case_id}'."
        )

    file_content = read_file(str(case_path))
    reviewable_texts = extract_reviewable_text(file_content)
    actual_findings = review(reviewable_texts, review_context)

    expected_outcomes, actual_outcomes = _match_findings(
        expected_findings=expected_case.expected_findings,
        actual_findings=actual_findings,
    )

    tp = sum(1 for outcome in expected_outcomes if outcome.matched)
    fn = sum(1 for outcome in expected_outcomes if not outcome.matched)
    fp = sum(1 for outcome in actual_outcomes if not outcome.matched)
    count_in_range = (
        expected_case.expected_finding_count_min
        <= len(actual_findings)
        <= expected_case.expected_finding_count_max
    )
    case_passed = fn == 0 and fp == 0 and count_in_range

    return CaseResult(
        case_filename=case_path.name,
        case_id=case_id,
        case_path=case_path.as_posix(),
        expected_path=expected_path.as_posix(),
        expected_case=expected_case,
        actual_findings=actual_findings,
        expected_outcomes=expected_outcomes,
        actual_outcomes=actual_outcomes,
        tp=tp,
        fp=fp,
        fn=fn,
        case_passed=case_passed,
        count_in_range=count_in_range,
    )


def _load_expected_case(expected_path: Path) -> ExpectedCase:
    try:
        raw_data = json.loads(expected_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid expected JSON at {expected_path.as_posix()}: {exc}"
        ) from exc

    try:
        return ExpectedCase.model_validate(raw_data)
    except ValidationError as exc:
        raise ValueError(
            f"Expected JSON schema validation failed for {expected_path.as_posix()}: {exc}"
        ) from exc


def _match_findings(
    *,
    expected_findings: list[ExpectedFinding],
    actual_findings: list[Finding],
) -> tuple[list[ExpectedFindingOutcome], list[ActualFindingOutcome]]:
    actual_match_states: list[ActualFindingOutcome] = [
        ActualFindingOutcome(actual=finding, matched=False, reason="Unmatched actual finding.")
        for finding in actual_findings
    ]
    expected_outcomes: list[ExpectedFindingOutcome] = []

    for expected in expected_findings:
        matched_index: int | None = None
        best_reason = "No actual finding matched the expected category and text/line rule."

        for index, actual_outcome in enumerate(actual_match_states):
            if actual_outcome.matched:
                continue

            match_result = _is_expected_match(expected, actual_outcome.actual)
            if match_result.matched:
                matched_index = index
                best_reason = match_result.reason
                break

            if actual_outcome.actual.category == expected.category:
                best_reason = match_result.reason

        if matched_index is None:
            expected_outcomes.append(
                ExpectedFindingOutcome(
                    expected=expected,
                    matched=False,
                    matched_actual=None,
                    reason=best_reason,
                )
            )
            continue

        matched_actual = actual_match_states[matched_index].actual
        actual_match_states[matched_index] = ActualFindingOutcome(
            actual=matched_actual,
            matched=True,
            reason=f"Matched expected finding '{expected.target_text_contains}'.",
        )
        expected_outcomes.append(
            ExpectedFindingOutcome(
                expected=expected,
                matched=True,
                matched_actual=matched_actual,
                reason=best_reason,
            )
        )

    return expected_outcomes, actual_match_states


def _is_expected_match(expected: ExpectedFinding, actual: Finding) -> MatchResult:
    if actual.category != expected.category:
        return MatchResult(
            matched=False,
            reason=(
                f"Category mismatch: expected {expected.category}, got {actual.category}."
            ),
        )

    if expected.requires_suggested_replacement and not _has_suggested_replacement(actual):
        return MatchResult(
            matched=False,
            reason="Suggested replacement required but missing from actual finding.",
        )

    text_match = _expected_text_in_actual(expected.target_text_contains, actual)
    line_match = _line_match(expected, actual)
    if text_match or line_match:
        if text_match and line_match:
            reason = "Category matched, target text matched, and line range matched."
        elif text_match:
            reason = "Category matched and target text matched."
        else:
            reason = "Category matched and line range matched."
        return MatchResult(matched=True, reason=reason)

    return MatchResult(
        matched=False,
        reason=(
            "Category matched but neither target text nor line range matched the expected finding."
        ),
    )


def _expected_text_in_actual(target_text: str, actual: Finding) -> bool:
    haystacks = [
        actual.source_text,
        actual.explanation,
        actual.recommendation,
        actual.suggested_replacement or "",
    ]
    target_lower = target_text.lower()
    return any(target_lower in haystack.lower() for haystack in haystacks)


def _line_match(expected: ExpectedFinding, actual: Finding) -> bool:
    if expected.line_range_approximate:
        return _line_ranges_overlap(
            expected.line_start,
            expected.line_end,
            actual.line_start,
            actual.line_end,
        )
    return (
        expected.line_start == actual.line_start
        and expected.line_end == actual.line_end
    )


def _line_ranges_overlap(
    expected_start: int,
    expected_end: int,
    actual_start: int,
    actual_end: int,
) -> bool:
    return not (actual_end < expected_start or actual_start > expected_end)


def _has_suggested_replacement(actual: Finding) -> bool:
    return bool(actual.suggested_replacement and actual.suggested_replacement.strip())


def _build_summary(
    case_results: list[CaseResult],
    *,
    backend: str,
    benchmark_name: str,
    selected_case_ids: list[str] | None,
) -> dict[str, float | int | str]:
    tp = sum(result.tp for result in case_results)
    fp = sum(result.fp for result in case_results)
    fn = sum(result.fn for result in case_results)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    passed_cases = sum(1 for result in case_results if result.case_passed)

    return {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "backend": backend,
        "benchmark": benchmark_name,
        "model": get_model_display_name() or "(unknown)",
        "cases_run": len(case_results),
        "cases_passed": passed_cases,
        "cases_failed": len(case_results) - passed_cases,
        "partial_run": bool(selected_case_ids),
        "selected_cases": ", ".join(result.case_id for result in case_results),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
    }


def _persist_run_progress(run_state: EvaluationRunState) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    progress_payload = _build_progress_payload(run_state)
    run_state.artifacts.progress_path.write_text(
        json.dumps(progress_payload, indent=2),
        encoding="utf-8",
    )
    _write_partial_report_markdown(run_state)


def _finalize_interrupted_run(
    run_state: EvaluationRunState,
    *,
    interruption_reason: str,
) -> None:
    run_state.interruption_reason = interruption_reason
    run_state.completed_at = None
    _persist_run_progress(run_state)


def _finalize_successful_run(run_state: EvaluationRunState) -> None:
    run_state.interruption_reason = None
    run_state.completed_at = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    )
    _persist_run_progress(run_state)


def _build_progress_payload(run_state: EvaluationRunState) -> dict[str, object]:
    status = "completed"
    if run_state.interruption_reason:
        status = "interrupted"
    elif run_state.completed_at is None:
        status = "in_progress"

    return {
        "status": status,
        "backend": run_state.backend,
        "benchmark": run_state.benchmark_name,
        "model": run_state.model,
        "run_started_at": run_state.started_at,
        "run_completed_at": run_state.completed_at,
        "last_updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "interruption_reason": run_state.interruption_reason,
        "selected_case_ids": run_state.selected_case_ids or [],
        "planned_case_ids": run_state.planned_case_ids,
        "completed_case_ids": [result.case_id for result in run_state.completed_results],
        "remaining_case_ids": run_state.remaining_case_ids,
        "completed_case_count": len(run_state.completed_results),
        "remaining_case_count": len(run_state.remaining_case_ids),
        "completed_results": [
            _serialize_case_result(result) for result in run_state.completed_results
        ],
    }


def _serialize_case_result(result: CaseResult) -> dict[str, object]:
    return {
        "case_filename": result.case_filename,
        "case_id": result.case_id,
        "case_path": result.case_path,
        "expected_path": result.expected_path,
        "status": "PASS" if result.case_passed else "FAIL",
        "tp": result.tp,
        "fp": result.fp,
        "fn": result.fn,
        "count_in_range": result.count_in_range,
        "expected_case": result.expected_case.model_dump(),
        "actual_findings": [finding.model_dump() for finding in result.actual_findings],
        "expected_outcomes": [
            {
                "expected": outcome.expected.model_dump(),
                "matched": outcome.matched,
                "matched_actual": (
                    outcome.matched_actual.model_dump()
                    if outcome.matched_actual is not None
                    else None
                ),
                "reason": outcome.reason,
            }
            for outcome in result.expected_outcomes
        ],
        "actual_outcomes": [
            {
                "actual": outcome.actual.model_dump(),
                "matched": outcome.matched,
                "reason": outcome.reason,
            }
            for outcome in result.actual_outcomes
        ],
    }


def _write_results_markdown(
    case_results: list[CaseResult],
    summary: dict[str, float | int | str],
    *,
    backend: str,
    benchmark_name: str,
) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results_path = _build_results_path(backend, benchmark_name=benchmark_name)
    title = _build_results_title(benchmark_name=benchmark_name)
    notes = _build_notes(backend)

    lines: list[str] = [
        title,
        "",
        f"- Backend: `{summary['backend']}`",
        f"- Benchmark: `{summary['benchmark']}`",
        f"- Model: `{summary['model']}`",
        f"- Timestamp: `{summary['timestamp']}`",
        f"- Cases run: `{summary['cases_run']}`",
    ]

    if summary["partial_run"]:
        lines.extend(
            [
                "- Run type: `partial evaluation`",
                f"- Selected cases: `{summary['selected_cases']}`",
                f"- Selected case count: `{summary['cases_run']}`",
            ]
        )
    else:
        lines.append("- Run type: `full evaluation`")

    lines.extend(
        [
            "",
            "## Overall Metrics",
            "",
            f"- True Positives (TP): `{summary['tp']}`",
            f"- False Positives (FP): `{summary['fp']}`",
            f"- False Negatives (FN): `{summary['fn']}`",
            f"- Precision: `{summary['precision']:.2f}`",
            f"- Recall: `{summary['recall']:.2f}`",
            f"- Cases passed: `{summary['cases_passed']}`",
            f"- Cases failed: `{summary['cases_failed']}`",
            "",
            "## Per-Case Summary",
            "",
            "| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )

    for result in case_results:
        lines.append(
            "| "
            f"`{result.case_filename}` | "
            f"{'PASS' if result.case_passed else 'FAIL'} | "
            f"{result.tp} | {result.fp} | {result.fn} | "
            f"{len(result.actual_findings)} | "
            f"{result.expected_case.expected_finding_count_min}-"
            f"{result.expected_case.expected_finding_count_max} |"
        )

    lines.extend(
        [
            "",
            "## Detailed Case Results",
            "",
        ]
    )

    for result in case_results:
        lines.extend(_render_case_result(result, backend=backend))

    lines.extend(
        [
            "## Notes",
            "",
            *notes,
            "",
        ]
    )

    results_path.write_text("\n".join(lines), encoding="utf-8")


def _write_partial_report_markdown(run_state: EvaluationRunState) -> None:
    completed_results = run_state.completed_results
    completed_summary = _build_summary(
        completed_results,
        backend=run_state.backend,
        benchmark_name=run_state.benchmark_name,
        selected_case_ids=run_state.selected_case_ids,
    )
    interruption_reason = run_state.interruption_reason or "Run still in progress."
    status_label = "interrupted" if run_state.interruption_reason else "in progress"
    title = _build_results_title(benchmark_name=run_state.benchmark_name)

    lines: list[str] = [
        f"{title} - Partial Report",
        "",
        "> Partial report: completed evaluations were preserved before the run finished.",
        "",
        f"- Status: `{status_label}`",
        f"- Backend: `{run_state.backend}`",
        f"- Benchmark: `{run_state.benchmark_name}`",
        f"- Model: `{run_state.model}`",
        f"- Run started: `{run_state.started_at}`",
        f"- Last updated: `{completed_summary['timestamp']}`",
        f"- Completed cases: `{len(completed_results)}`",
        f"- Remaining cases: `{len(run_state.remaining_case_ids)}`",
        f"- Interruption reason: `{interruption_reason}`",
    ]

    if run_state.selected_case_ids:
        lines.append(
            f"- Selected cases: `{', '.join(run_state.planned_case_ids)}`"
        )

    lines.extend(
        [
            "",
            "## Completed Metrics",
            "",
            f"- True Positives (TP): `{completed_summary['tp']}`",
            f"- False Positives (FP): `{completed_summary['fp']}`",
            f"- False Negatives (FN): `{completed_summary['fn']}`",
            f"- Precision: `{completed_summary['precision']:.2f}`",
            f"- Recall: `{completed_summary['recall']:.2f}`",
            f"- Cases passed: `{completed_summary['cases_passed']}`",
            f"- Cases failed: `{completed_summary['cases_failed']}`",
            "",
            "## Completed Cases",
            "",
        ]
    )

    if not completed_results:
        lines.extend(
            [
                "- No completed cases were available when the run stopped.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "| Case | Status | TP | FP | FN | Actual Count | Expected Count Range |",
                "| --- | --- | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for result in completed_results:
            lines.append(
                "| "
                f"`{result.case_filename}` | "
                f"{'PASS' if result.case_passed else 'FAIL'} | "
                f"{result.tp} | {result.fp} | {result.fn} | "
                f"{len(result.actual_findings)} | "
                f"{result.expected_case.expected_finding_count_min}-"
                f"{result.expected_case.expected_finding_count_max} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Remaining Cases",
            "",
        ]
    )

    if not run_state.remaining_case_ids:
        lines.extend(
            [
                "- None.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                *(f"- `{case_id}`" for case_id in run_state.remaining_case_ids),
                "",
            ]
        )

    if completed_results:
        lines.extend(
            [
                "## Detailed Completed Case Results",
                "",
            ]
        )
        for result in completed_results:
            lines.extend(_render_case_result(result, backend=run_state.backend))

    run_state.artifacts.partial_report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def _render_case_result(result: CaseResult, *, backend: str) -> list[str]:
    lines = [
        f"### {result.case_filename}",
        "",
        f"- Status: `{'PASS' if result.case_passed else 'FAIL'}`",
        f"- Case file: `{result.case_path}`",
        f"- Expected file: `{result.expected_path}`",
        f"- Metrics: `TP={result.tp}`, `FP={result.fp}`, `FN={result.fn}`",
        f"- Actual finding count: `{len(result.actual_findings)}`",
        f"- Expected finding count range: "
        f"`{result.expected_case.expected_finding_count_min}` to "
        f"`{result.expected_case.expected_finding_count_max}`",
        f"- Count range satisfied: `{'yes' if result.count_in_range else 'no'}`",
        "",
        "#### Expected Findings",
        "",
    ]

    if not result.expected_outcomes:
        lines.extend(
            [
                "- None expected.",
                "",
            ]
        )
    else:
        for index, outcome in enumerate(result.expected_outcomes, start=1):
            expected = outcome.expected
            lines.extend(
                [
                    f"{index}. Category: `{expected.category}`",
                    f"   Target text contains: `{expected.target_text_contains}`",
                    f"   Lines: `{expected.line_start}-{expected.line_end}`",
                    f"   Approximate line match allowed: `{str(expected.line_range_approximate).lower()}`",
                    f"   Suggested replacement required: `{str(expected.requires_suggested_replacement).lower()}`",
                    f"   Outcome: `{'TP' if outcome.matched else 'FN'}`",
                    f"   Reasoning: {outcome.reason}",
                ]
            )
            if outcome.matched_actual is not None:
                lines.append(
                    "   Matched actual: "
                    f"`{outcome.matched_actual.category}` on lines "
                    f"`{outcome.matched_actual.line_start}-{outcome.matched_actual.line_end}`"
                )
            lines.append("")

    lines.extend(
        [
            "#### Actual Findings",
            "",
        ]
    )

    if not result.actual_outcomes:
        lines.extend(
            [
                f"- No findings returned by the {backend} backend.",
                "",
            ]
        )
        return lines

    for index, actual_outcome in enumerate(result.actual_outcomes, start=1):
        actual = actual_outcome.actual
        lines.extend(
            [
                f"{index}. Category: `{actual.category}`",
                f"   Severity: `{actual.severity}`",
                f"   Confidence: `{actual.confidence}`",
                f"   Detection method: `{actual.detection_method}`",
                f"   Lines: `{actual.line_start}-{actual.line_end}`",
                f"   Source text: `{_inline_text(actual.source_text)}`",
                f"   Explanation: `{_inline_text(actual.explanation)}`",
                f"   Recommendation: `{_inline_text(actual.recommendation)}`",
                "   Suggested replacement: "
                f"`{_inline_text(actual.suggested_replacement) if actual.suggested_replacement else '(none)'}`",
                f"   Outcome: `{'Matched' if actual_outcome.matched else 'FP'}`",
                f"   Reasoning: {actual_outcome.reason}",
                "",
            ]
        )

    return lines


def _build_case_diagnostic_summary(result: CaseResult) -> str:
    if result.case_passed:
        return (
            f"expected {len(result.expected_outcomes)}, returned "
            f"{len(result.actual_findings)}, no missing or unexpected findings"
        )

    missing_categories = [
        outcome.expected.category
        for outcome in result.expected_outcomes
        if not outcome.matched
    ]
    unexpected_categories = [
        outcome.actual.category
        for outcome in result.actual_outcomes
        if not outcome.matched
    ]

    summary_parts = [
        f"expected {len(result.expected_outcomes)}",
        f"returned {len(result.actual_findings)}",
        f"missing {result.fn}",
        f"unexpected {result.fp}",
    ]

    if not result.count_in_range:
        summary_parts.append(
            "count out of range "
            f"({result.expected_case.expected_finding_count_min}-"
            f"{result.expected_case.expected_finding_count_max})"
        )

    if missing_categories:
        summary_parts.append(
            f"missing categories: {', '.join(missing_categories)}"
        )

    if unexpected_categories:
        summary_parts.append(
            f"unexpected categories: {', '.join(unexpected_categories)}"
        )

    return "; ".join(summary_parts)


def _format_exception_summary(exc: Exception) -> str:
    message = str(exc).strip() or exc.__class__.__name__
    normalized_message = " ".join(message.split())
    lowered = normalized_message.lower()

    if isinstance(exc, json.JSONDecodeError):
        return f"malformed JSON: {normalized_message}"
    if isinstance(exc, ValidationError):
        return f"schema validation failure: {normalized_message}"
    if isinstance(exc, AgentReviewError):
        return f"backend/API failure: {normalized_message}"
    if isinstance(exc, (ContextLoadError, FileReadError, ExtractionError)):
        return normalized_message
    if "json" in lowered:
        return f"malformed JSON: {normalized_message}"
    if "expected case_id mismatch" in lowered or "match" in lowered:
        return f"matching failure: {normalized_message}"

    return normalized_message


def _clear_partial_artifacts(artifacts: RunArtifacts) -> None:
    for artifact_path in (artifacts.partial_report_path,):
        if artifact_path.exists():
            artifact_path.unlink()


def _inline_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def _pluralize_case(case_count: int) -> str:
    return "case" if case_count == 1 else "cases"


def _build_results_path(backend: str, *, benchmark_name: str) -> Path:
    if benchmark_name == "default":
        return RESULTS_DIR / f"{backend}-results.md"
    benchmark_suffix = benchmark_name.replace("/", "-")
    return RESULTS_DIR / f"{backend}-{benchmark_suffix}-results.md"


def _build_results_title(*, benchmark_name: str) -> str:
    display_backend = get_backend_display_name()
    if benchmark_name == "default":
        return f"# {display_backend} Evaluation Results"
    benchmark_label = benchmark_name.replace("_", " ")
    return f"# {display_backend} Evaluation Results ({benchmark_label})"


def _build_notes(backend: str) -> list[str]:
    common_notes = [
        "- Suggested replacement matching is required only for expected findings that explicitly demand it.",
        "- Severity is displayed for context but does not determine TP, FP, or FN in this evaluation implementation.",
    ]

    if backend == "deterministic":
        return [
            "- Deterministic results validate repeatable pipeline behavior, not Gemini semantic reasoning.",
            *common_notes,
        ]

    return [
        "- Gemini evaluation results represent a snapshot captured at a specific point in time. Because LLM outputs may vary between runs, these results should be interpreted as evaluation evidence rather than a perfectly reproducible benchmark.",
        "- Gemini results validate the current live semantic review path without changing prompts, matching rules, or the dataset.",
        *common_notes,
    ]


if __name__ == "__main__":
    main()
