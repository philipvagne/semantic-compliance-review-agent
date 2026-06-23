"""Write one Markdown audit report from the current review pipeline output.

Purpose:
- Convert file, extraction, context, finding, and backend metadata into one
  human-readable Markdown audit report.

Input:
- FileContent
- ReviewableText[]
- ReviewContext
- Finding[]
- Backend metadata

Output:
- One Markdown report written to `output/<filename>-audit-report.md`.

Responsibilities:
- Generate Markdown report content.
- Preserve finding order, line numbers, and source text.
- Include available backend and model metadata.
- Include available clean-copy summary data when requested by the CLI.
- Write the report to the output directory.

Non-responsibilities:
- Call Gemini.
- Generate findings.
- Modify source code.
- Create clean copies, evaluations, or UI output.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC
from datetime import datetime
from pathlib import Path
import re

from src.clean_copy_writer import CleanCopyResult
from src.schemas import FileContent
from src.schemas import Finding
from src.schemas import ReviewContext
from src.schemas import ReviewableText


CATEGORY_PREFIX = {
    "SECURITY_RISK": "SEC",
    "PROFESSIONALISM_RISK": "PRO",
    "COMPLIANCE_RISK": "CMP",
    "INTERNAL_CODENAME_EXPOSURE": "CDX",
    "INTELLECTUAL_PROPERTY_RISK": "IPR",
    "REPUTATION_RISK": "REP",
}

CATEGORY_LABEL = {
    "SECURITY_RISK": "Security Risk",
    "PROFESSIONALISM_RISK": "Professionalism Risk",
    "COMPLIANCE_RISK": "Compliance Risk",
    "INTERNAL_CODENAME_EXPOSURE": "Internal Codename Exposure",
    "INTELLECTUAL_PROPERTY_RISK": "Intellectual Property Risk",
    "REPUTATION_RISK": "Reputation Risk",
}

REFERENCE_GUIDE_ROWS = [
    ("CDX", "Internal Codename Exposure"),
    ("SEC", "Security Risk"),
    ("PRO", "Professionalism Risk"),
    ("CMP", "Compliance Risk"),
    ("IPR", "Intellectual Property Risk"),
    ("REP", "Reputation Risk"),
]

SEVERITY_RANK = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

SEVERITY_DISPLAY = {
    "CRITICAL": "🔴 Critical",
    "HIGH": "🟠 High",
    "MEDIUM": "🟡 Medium",
    "LOW": "🟢 Low",
}

CONFIDENCE_DISPLAY = {
    "HIGH": "● High",
    "MEDIUM": "◐ Medium",
    "LOW": "○ Low",
}

DETECTION_METHOD_DISPLAY = {
    "TERM_MATCH": "Term Match",
    "SEMANTIC_ANALYSIS": "Semantic Analysis",
    "HYBRID": "Hybrid",
}


class ReportWriteError(Exception):
    """Raised when the audit report cannot be generated or written."""


def write_audit_report(
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    review_context: ReviewContext,
    findings: list[Finding],
    backend: str | None,
    model: str | None,
    clean_copy_result: CleanCopyResult | None = None,
    output_dir: str = "output",
) -> str:
    _validate_report_inputs(
        file_content=file_content,
        reviewable_texts=reviewable_texts,
        review_context=review_context,
        findings=findings,
    )

    output_directory = Path(output_dir)
    try:
        output_directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ReportWriteError(f"Unable to create output directory: {output_directory}") from exc

    output_path = output_directory / f"{Path(file_content.filename).stem}-audit-report.md"
    report_text = _build_report_markdown(
        file_content=file_content,
        reviewable_texts=reviewable_texts,
        review_context=review_context,
        findings=findings,
        backend=backend,
        model=model,
        clean_copy_result=clean_copy_result,
    )

    try:
        output_path.write_text(report_text, encoding="utf-8")
    except OSError as exc:
        raise ReportWriteError(f"Unable to write report file: {output_path}") from exc
    except Exception as exc:
        raise ReportWriteError(f"Unexpected report write failure for {output_path}") from exc

    return str(output_path).replace("\\", "/")


def _validate_report_inputs(
    *,
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    review_context: ReviewContext,
    findings: list[Finding],
) -> None:
    if not isinstance(file_content, FileContent):
        raise ReportWriteError("Invalid report data received: file_content must be FileContent.")
    if not isinstance(reviewable_texts, list) or any(
        not isinstance(item, ReviewableText) for item in reviewable_texts
    ):
        raise ReportWriteError(
            "Invalid report data received: reviewable_texts must be list[ReviewableText]."
        )
    if not isinstance(review_context, ReviewContext):
        raise ReportWriteError("Invalid report data received: review_context must be ReviewContext.")
    if not isinstance(findings, list) or any(not isinstance(item, Finding) for item in findings):
        raise ReportWriteError("Invalid report data received: findings must be list[Finding].")


def _build_report_markdown(
    *,
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    review_context: ReviewContext,
    findings: list[Finding],
    backend: str | None,
    model: str | None,
    clean_copy_result: CleanCopyResult | None,
) -> str:
    references = _build_references(findings)
    sections: list[str] = [
        "# Semantic Compliance Audit Report",
        "",
        _build_metadata_table(
            file_content=file_content,
            review_context=review_context,
            findings=findings,
            backend=backend,
            model=model,
        ),
        "",
        "---",
        "",
        _build_executive_summary(reviewable_texts=reviewable_texts, findings=findings),
        "",
        "---",
        "",
        _build_summary_matrix(findings=findings, references=references),
        "",
        "---",
        "",
        _build_findings_section(
            file_content=file_content,
            findings=findings,
            references=references,
        ),
    ]
    if clean_copy_result is not None:
        sections.extend(
            [
                "",
                "---",
                "",
                _build_clean_copy_section(clean_copy_result),
            ]
        )
    sections.extend(
        [
            "",
            "---",
            "",
            _build_reference_guide(),
            "",
            "---",
            "",
            _build_review_philosophy(),
        ]
    )
    return "\n".join(sections).rstrip() + "\n"


def _build_metadata_table(
    *,
    file_content: FileContent,
    review_context: ReviewContext,
    findings: list[Finding],
    backend: str | None,
    model: str | None,
) -> str:
    rows = [
        ("**Target File**", f"`{file_content.path}`"),
        ("**Generated On**", datetime.now(UTC).strftime("%Y-%m-%d · %H:%M UTC")),
    ]
    if backend:
        rows.append(("**Backend**", backend))
    if model:
        rows.append(("**Model**", f"`{model}`"))
    rows.extend(
        [
            ("**Configured Sensitive Terms**", str(len(review_context.sensitive_terms))),
            ("**Findings Count**", str(len(findings))),
            ("**Audit Status**", f"**{_get_audit_status(findings)}**"),
        ]
    )
    return _render_two_column_table(rows)


def _build_executive_summary(
    *,
    reviewable_texts: list[ReviewableText],
    findings: list[Finding],
) -> str:
    return "\n".join(
        [
            "## Executive Summary",
            "",
            f"This audit completed with status **{_get_audit_status(findings)}**.",
            "",
            f"- Reviewable text items analyzed: {len(reviewable_texts)}",
            f"- Findings generated: {len(findings)}",
            f"- Highest severity found: {_format_severity(_get_highest_severity(findings))}",
            f"- Categories detected: {_get_detected_categories(findings)}",
        ]
    )


def _build_findings_section(
    *,
    file_content: FileContent,
    findings: list[Finding],
    references: list[str],
) -> str:
    if not findings:
        return "\n".join(
            [
                "## Detailed Findings",
                "",
                "No findings were generated for this file.",
                "The audit completed successfully.",
                "Human review is still recommended before publication or release.",
            ]
        )

    sections = ["## Detailed Findings", ""]
    for index, finding in enumerate(findings):
        reference = references[index]
        sections.extend(
            [
                f"### {reference}: {CATEGORY_LABEL[finding.category]}",
                "",
                f"**Severity:** {_format_severity(finding.severity)} | **Confidence:** {_format_confidence(finding.confidence)}",
                "",
                f"**Detection Method:** {_format_detection_method(finding.detection_method)}",
                "",
                _format_location(file_content.path, finding.line_start, finding.line_end),
                "",
                "#### Source Text",
                "",
                "```text",
                finding.source_text,
                "```",
                "",
                "#### Why This Was Flagged",
                "",
                _format_explanation_text(finding.explanation),
                "",
                "#### Recommended Action",
                "",
                finding.recommendation,
                "",
                "#### Suggested Replacement",
                "",
                _build_suggested_replacement_block(finding),
                "",
            ]
        )
    return "\n".join(sections).rstrip()


def _build_summary_matrix(*, findings: list[Finding], references: list[str]) -> str:
    rows = [("Reference", "Category", "Severity", "Confidence")]
    for reference, finding in zip(references, findings):
        rows.append(
            (
                reference,
                CATEGORY_LABEL[finding.category],
                _format_severity(finding.severity),
                _format_confidence(finding.confidence),
            )
        )

    if len(rows) == 1:
        rows.append(("-", "No findings", "-", "-"))

    return "\n".join(
        [
            "## Audit Summary Matrix",
            "",
            _render_table(rows),
        ]
    )


def _build_reference_guide() -> str:
    rows = [("Prefix", "Description"), *REFERENCE_GUIDE_ROWS]
    return "\n".join(
        [
            "## Finding Reference Guide",
            "",
            _render_table(rows),
        ]
    ) 


def _build_clean_copy_section(clean_copy_result: CleanCopyResult | None) -> str:
    lines = [
        "## Clean Copy Summary",
        "",
        f"- Clean copy generated: `{clean_copy_result.output_path}`",
        f"- Replacements applied: `{clean_copy_result.applied_count}`",
        f"- Replacements skipped: `{clean_copy_result.skipped_count}`",
    ]

    if not clean_copy_result.skipped_replacements:
        lines.append("- Skipped replacement reasons: none")
        return "\n".join(lines)

    lines.extend(
        [
            "- Skipped replacement reasons:",
        ]
    )
    for skipped in clean_copy_result.skipped_replacements:
        line_label = (
            f"line {skipped.line_start}"
            if skipped.line_start == skipped.line_end
            else f"lines {skipped.line_start}-{skipped.line_end}"
        )
        lines.append(
            f"  - `{skipped.finding_id}` ({line_label}): {skipped.reason}"
        )
    return "\n".join(lines)


def _build_review_philosophy() -> str:
    return "\n".join(
        [
            "## Review Philosophy",
            "",
            "The Semantic Compliance Review Agent provides AI-assisted semantic review to help identify potentially risky human-written text.",
            "",
            "Human review is required before any action is taken.",
            "",
            "The original source file was not modified during this audit.",
            "",
            "Any generated clean copy is a separate advisory artifact under `output/` and still requires developer review.",
            "",
            "The developer remains responsible for final decisions.",
        ]
    )


def _build_references(findings: list[Finding]) -> list[str]:
    counters: dict[str, int] = defaultdict(int)
    references: list[str] = []
    for finding in findings:
        prefix = CATEGORY_PREFIX.get(finding.category)
        if not prefix:
            raise ReportWriteError(
                f"Invalid report data received: unsupported finding category '{finding.category}'."
            )
        counters[prefix] += 1
        references.append(f"{prefix}-{counters[prefix]:03d}")
    return references


def _get_audit_status(findings: list[Finding]) -> str:
    return "ISSUES FOUND" if findings else "NO ISSUES FOUND"


def _get_highest_severity(findings: list[Finding]) -> str:
    if not findings:
        return "None"
    return max(findings, key=lambda finding: SEVERITY_RANK[finding.severity]).severity


def _get_detected_categories(findings: list[Finding]) -> str:
    if not findings:
        return "None"

    seen: set[str] = set()
    ordered_labels: list[str] = []
    for finding in findings:
        if finding.category in seen:
            continue
        seen.add(finding.category)
        ordered_labels.append(CATEGORY_LABEL[finding.category])
    return ", ".join(ordered_labels)


def _build_suggested_replacement_block(finding: Finding) -> str:
    suggested_replacement = (finding.suggested_replacement or "").strip()
    if not suggested_replacement:
        return (
            "No automatic suggestion generated — confidence was not high enough "
            "for automated remediation."
        )

    return "\n".join(
        [
            "```diff",
            f"- {finding.source_text}",
            f"+ {suggested_replacement}",
            "```",
        ]
    )


def _format_severity(severity: str) -> str:
    if severity == "None":
        return "None"
    return SEVERITY_DISPLAY.get(severity, severity.title())


def _format_confidence(confidence: str) -> str:
    return CONFIDENCE_DISPLAY.get(confidence, confidence.title())


def _format_detection_method(detection_method: str) -> str:
    return DETECTION_METHOD_DISPLAY.get(detection_method, detection_method.title())


def _format_location(path: str, line_start: int, line_end: int) -> str:
    if line_start == line_end:
        return f"`{path}` — line {line_start}"
    return f"`{path}` — lines {line_start}-{line_end}"


def _format_explanation_text(explanation: str) -> str:
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", explanation.strip())
        if sentence.strip()
    ]
    bullet_points = sentences[:3] or [explanation.strip()]
    return "\n".join(f"- {bullet}" for bullet in bullet_points)


def _render_two_column_table(rows: list[tuple[str, str]]) -> str:
    table_rows = [("", ""), *rows]
    return _render_table(table_rows)


def _render_table(rows: list[tuple[str, ...]]) -> str:
    widths = [max(len(str(row[index])) for row in rows) for index in range(len(rows[0]))]

    def _render_row(row: tuple[str, ...]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)) + " |"

    header = _render_row(rows[0])
    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    body = [_render_row(row) for row in rows[1:]]
    return "\n".join([header, separator, *body])
