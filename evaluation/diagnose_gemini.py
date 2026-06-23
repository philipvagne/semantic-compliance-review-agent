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
- Report PASS/FAIL plus short previews or error summaries.

Non-responsibilities:
- Change production backend behavior.
- Tune prompts or retry requests.
- Modify evaluation data or scoring logic.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path

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
    preview: str | None = None
    error_type: str | None = None
    error_message: str | None = None


def main() -> None:
    api_key = _resolve_gemini_api_key()
    if not api_key:
        raise SystemExit(
            "Gemini diagnosis failed: GOOGLE_API_KEY or GEMINI_API_KEY must be set."
        )

    case_text = DIAGNOSTIC_CASE_PATH.read_text(encoding="utf-8")
    client = Client(api_key=api_key)

    results = [
        _run_direct_smoke_test(client),
        _run_direct_realistic_test(client, case_text),
        _run_adk_backed_test(),
    ]

    print("Gemini Backend Diagnosis")
    print(f"Case file: {DIAGNOSTIC_CASE_PATH.as_posix()}")
    print("")
    for result in results:
        _print_result(result)

    print("Interpretation")
    print(_build_interpretation(results))


def _run_direct_smoke_test(client: Client) -> DiagnosticResult:
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents="Say hello.",
        )
        return DiagnosticResult(
            test_name="Direct google.genai smoke test",
            passed=True,
            preview=_preview_text(getattr(response, "text", None)),
        )
    except Exception as exc:
        return _build_failure_result("Direct google.genai smoke test", exc)


def _run_direct_realistic_test(client: Client, case_text: str) -> DiagnosticResult:
    prompt = (
        "Review the following Python file text for security risks, professionalism "
        "risks, and internal naming risks. Return JSON-like findings with fields "
        "category, line_start, line_end, explanation, and recommendation. "
        "Return an empty list if no findings exist.\n\n"
        "File text:\n"
        f"{case_text}"
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
        )
        return DiagnosticResult(
            test_name="Direct google.genai realistic review prompt",
            passed=True,
            preview=_preview_text(getattr(response, "text", None)),
        )
    except Exception as exc:
        return _build_failure_result(
            "Direct google.genai realistic review prompt",
            exc,
        )


def _run_adk_backed_test() -> DiagnosticResult:
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
            preview=_preview_text(preview),
        )
    except (
        AgentReviewError,
        ContextLoadError,
        FileReadError,
        ExtractionError,
        OSError,
    ) as exc:
        return _build_failure_result("ADK-backed review path", exc)


def _resolve_gemini_api_key() -> str | None:
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


def _build_failure_result(test_name: str, error: Exception) -> DiagnosticResult:
    return DiagnosticResult(
        test_name=test_name,
        passed=False,
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
    if result.passed:
        print(f"  Preview: {result.preview}")
        return
    print(f"  Error: {result.error_type}: {result.error_message}")


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
