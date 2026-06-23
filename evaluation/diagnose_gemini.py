"""Diagnose direct and ADK-backed Gemini backend paths for this project.

Purpose:
- Compare simple direct Gemini calls with the current ADK-backed review path.

Input:
- Gemini credentials from `GOOGLE_API_KEY` or `GEMINI_API_KEY`.
- The committed `evaluation/cases/security_python.py` case file.

Output:
- Concise console-only diagnostic results for three Gemini path checks.

Responsibilities:
- Run a direct `google.genai` smoke test.
- Run a direct `google.genai` realistic review-prompt test.
- Run the existing ADK-backed Gemini review path used by the project.
- Report PASS/FAIL, elapsed duration, and short previews or error summaries.
- Report safe API-key configuration status.
- Support repeated observation cycles with optional delay between cycles.

Non-responsibilities:
- Change production backend behavior.
- Tune prompts or retry requests.
- Modify evaluation data or scoring logic.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import time

from google.genai import Client

from src.agent_review import AgentReviewError
from src.agent_review import GEMINI_MODEL_NAME
from src.agent_review import configure_backend
from src.agent_review import review
from src.context_loader import ContextLoadError
from src.context_loader import load_review_context
from src.file_reader import FileReadError
from src.file_reader import read_file
from src.text_extractor import ExtractionError
from src.text_extractor import extract_reviewable_text


REPO_ROOT = Path(__file__).resolve().parent.parent
DIAGNOSTIC_CASE_PATH = REPO_ROOT / "evaluation" / "cases" / "security_python.py"


@dataclass
class DiagnosticResult:
    test_name: str
    passed: bool
    elapsed_seconds: float
    preview: str | None = None
    error_type: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class KeyConfiguration:
    google_api_key_set: bool
    gemini_api_key_set: bool
    selected_variable: str | None
    selected_key: str | None


def main() -> None:
    args = parse_args()
    key_configuration = _resolve_key_configuration()
    case_text = DIAGNOSTIC_CASE_PATH.read_text(encoding="utf-8")

    print("Gemini Backend Diagnosis")
    print(f"Case file: {DIAGNOSTIC_CASE_PATH.as_posix()}")
    print("")
    _print_key_configuration(key_configuration)

    if not key_configuration.selected_key:
        raise SystemExit(
            "Gemini diagnosis failed: GOOGLE_API_KEY or GEMINI_API_KEY must be set."
        )

    all_results: list[list[DiagnosticResult]] = []
    for cycle_index in range(args.repeat):
        if cycle_index > 0 and args.delay_seconds > 0:
            print(
                f"Waiting {args.delay_seconds:g} seconds before the next diagnostic cycle..."
            )
            time.sleep(args.delay_seconds)

        cycle_number = cycle_index + 1
        print(f"Cycle {cycle_number}/{args.repeat}")
        cycle_results = _run_diagnostic_cycle(key_configuration.selected_key, case_text)
        all_results.append(cycle_results)
        for result in cycle_results:
            _print_result(result)
        print("")

    print("Interpretation")
    print(_build_interpretation(all_results[-1]))
    print("")
    print("Summary")
    _print_summary(all_results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diagnose direct and ADK-backed Gemini backend paths."
    )
    parser.add_argument(
        "--repeat",
        type=_parse_repeat,
        default=1,
        help="Number of full diagnostic cycles to run. Defaults to 1.",
    )
    parser.add_argument(
        "--delay-seconds",
        type=_parse_delay_seconds,
        default=0.0,
        help="Optional delay between diagnostic cycles. Defaults to 0 seconds.",
    )
    return parser.parse_args()


def _parse_repeat(value: str) -> int:
    try:
        repeat = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid repeat value '{value}'. Use an integer of 1 or greater."
        ) from exc

    if repeat < 1:
        raise argparse.ArgumentTypeError("Repeat count must be at least 1.")

    return repeat


def _parse_delay_seconds(value: str) -> float:
    try:
        delay_seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid delay value '{value}'. Use a non-negative integer or float."
        ) from exc

    if delay_seconds < 0:
        raise argparse.ArgumentTypeError("Delay seconds must be non-negative.")

    return delay_seconds


def _run_diagnostic_cycle(api_key: str, case_text: str) -> list[DiagnosticResult]:
    client = Client(api_key=api_key)
    return [
        _run_direct_smoke_test(client),
        _run_direct_realistic_test(client, case_text),
        _run_adk_backed_test(),
    ]


def _run_direct_smoke_test(client: Client) -> DiagnosticResult:
    started_at = time.perf_counter()
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents="Say hello.",
        )
        return DiagnosticResult(
            test_name="Direct google.genai smoke test",
            passed=True,
            elapsed_seconds=time.perf_counter() - started_at,
            preview=_preview_text(getattr(response, "text", None)),
        )
    except Exception as exc:
        return _build_failure_result(
            "Direct google.genai smoke test",
            exc,
            elapsed_seconds=time.perf_counter() - started_at,
        )


def _run_direct_realistic_test(client: Client, case_text: str) -> DiagnosticResult:
    prompt = (
        "Review the following Python file text for security risks, professionalism "
        "risks, and internal naming risks. Return JSON-like findings with fields "
        "category, line_start, line_end, explanation, and recommendation. "
        "Return an empty list if no findings exist.\n\n"
        "File text:\n"
        f"{case_text}"
    )

    started_at = time.perf_counter()
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
        )
        return DiagnosticResult(
            test_name="Direct google.genai realistic review prompt",
            passed=True,
            elapsed_seconds=time.perf_counter() - started_at,
            preview=_preview_text(getattr(response, "text", None)),
        )
    except Exception as exc:
        return _build_failure_result(
            "Direct google.genai realistic review prompt",
            exc,
            elapsed_seconds=time.perf_counter() - started_at,
        )


def _run_adk_backed_test() -> DiagnosticResult:
    started_at = time.perf_counter()
    try:
        configure_backend("gemini")
        review_context = load_review_context()
        file_content = read_file(str(DIAGNOSTIC_CASE_PATH))
        reviewable_texts = extract_reviewable_text(file_content)
        findings = review(reviewable_texts, review_context)
        preview = json.dumps(
            [
                {
                    "category": finding.category,
                    "line_start": finding.line_start,
                    "line_end": finding.line_end,
                }
                for finding in findings[:2]
            ]
        )
        if not findings:
            preview = "[]"
        return DiagnosticResult(
            test_name="ADK-backed review path",
            passed=True,
            elapsed_seconds=time.perf_counter() - started_at,
            preview=_preview_text(preview),
        )
    except (
        AgentReviewError,
        ContextLoadError,
        FileReadError,
        ExtractionError,
        OSError,
    ) as exc:
        return _build_failure_result(
            "ADK-backed review path",
            exc,
            elapsed_seconds=time.perf_counter() - started_at,
        )


def _resolve_key_configuration() -> KeyConfiguration:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    selected_variable: str | None = None
    selected_key: str | None = None

    if google_api_key:
        selected_variable = "GOOGLE_API_KEY"
        selected_key = google_api_key
    elif gemini_api_key:
        selected_variable = "GEMINI_API_KEY"
        selected_key = gemini_api_key

    return KeyConfiguration(
        google_api_key_set=bool(google_api_key),
        gemini_api_key_set=bool(gemini_api_key),
        selected_variable=selected_variable,
        selected_key=selected_key,
    )


def _build_failure_result(
    test_name: str,
    error: Exception,
    *,
    elapsed_seconds: float,
) -> DiagnosticResult:
    return DiagnosticResult(
        test_name=test_name,
        passed=False,
        elapsed_seconds=elapsed_seconds,
        error_type=type(error).__name__,
        error_message=str(error),
    )


def _preview_text(text: str | None) -> str:
    if not text:
        return "(empty response)"
    normalized = " ".join(text.split())
    if len(normalized) <= 160:
        return normalized
    return f"{normalized[:157]}..."


def _print_result(result: DiagnosticResult) -> None:
    status = "PASS" if result.passed else "FAIL"
    print(f"- {result.test_name}: {status}")
    print(f"  Elapsed: {result.elapsed_seconds:.2f}s")
    if result.passed:
        print(f"  Preview: {result.preview}")
        return
    print(f"  Error: {result.error_type}: {result.error_message}")


def _print_key_configuration(key_configuration: KeyConfiguration) -> None:
    print("API Key Configuration")
    print(
        f"- GOOGLE_API_KEY set: {'yes' if key_configuration.google_api_key_set else 'no'}"
    )
    print(
        f"- GEMINI_API_KEY set: {'yes' if key_configuration.gemini_api_key_set else 'no'}"
    )
    print(
        "- Selected variable: "
        f"{key_configuration.selected_variable or '(none)'}"
    )
    print(
        "- Reminder: the selected API key should be restricted to the Gemini API "
        "/ generativelanguage.googleapis.com."
    )
    print("")


def _print_summary(all_results: list[list[DiagnosticResult]]) -> None:
    if not all_results:
        return

    test_names = [result.test_name for result in all_results[0]]
    for test_name in test_names:
        flattened_results = [
            result
            for cycle_results in all_results
            for result in cycle_results
            if result.test_name == test_name
        ]
        success_count = sum(1 for result in flattened_results if result.passed)
        failure_count = len(flattened_results) - success_count
        print(f"- {test_name}: {success_count} PASS, {failure_count} FAIL")


def _build_interpretation(results: list[DiagnosticResult]) -> str:
    smoke_passed = results[0].passed
    realistic_passed = results[1].passed
    adk_passed = results[2].passed

    if not smoke_passed:
        return (
            "Basic Gemini API availability or credential configuration should be "
            "checked first."
        )
    if smoke_passed and realistic_passed and not adk_passed:
        return (
            "The issue appears more isolated to the ADK-backed path or its "
            "request shape than to general Gemini availability."
        )
    if smoke_passed and not realistic_passed and not adk_passed:
        return (
            "Both the realistic direct prompt and the ADK-backed path failed, so "
            "the issue may be related to realistic review request complexity or "
            "Gemini availability under that load."
        )
    if all(result.passed for result in results):
        return "The issue appears intermittent and was not reproduced in this diagnostic run."
    return (
        "The diagnostic outcome is mixed. Re-run the checks and compare which "
        "paths fail consistently."
    )


if __name__ == "__main__":
    main()
