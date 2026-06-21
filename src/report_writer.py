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
- Write the report to the output directory.

Non-responsibilities:
- Call Gemini.
- Generate findings.
- Modify source code.
- Create clean copies, evaluations, or UI output.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from datetime import UTC
from pathlib import Path

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


class ReportWriteError(Exception):
    """Raised when the audit report cannot be generated or written."""


def write_audit_report(
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    review_context: ReviewContext,
    findings: list[Finding],
    backend: str | None,
    model: str | None,
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
        _build_scan_statistics(reviewable_texts=reviewable_texts, findings=findings),
        "",
        "---",
        "",
        _build_findings_section(findings=findings, references=references),
        "",
        "---",
        "",
        _build_summary_matrix(findings=findings, references=references),
        "",
        "---",
        "",
        _build_reference_guide(),
        "",
        "---",
        "",
        _build_review_philosophy(),
    ]
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
        ("Target File", f"`{file_content.path}`"),
        ("Generated On", datetime.now(UTC).strftime("%Y-%m-%d · %H:%M UTC")),
    ]
    if backend:
        rows.append(("Backend", backend))
    if model:
        rows.append(("Model", f"`{model}`"))
    rows.extend(
        [
            ("Configured Sensitive Terms", str(len(review_context.sensitive_terms))),
            ("Findings Count", str(len(findings))),
            ("Audit Status", f"**{_get_audit_status(findings)}**"),
        ]
    )
    return _render_two_column_table(rows)


def _build_scan_statistics(
    *,
    reviewable_texts: list[ReviewableText],
    findings: list[Finding],
) -> str:
    rows = [
        ("Metric", "Value"),
        ("Reviewable text items analyzed", str(len(reviewable_texts))),
        ("Findings generated", str(len(findings))),
    ]
    return "\n".join(
        [
            "## Scan Statistics",
            "",
            _render_table(rows),
        ]
    )


def _build_findings_section(
    *,
    findings: list[Finding],
    references: list[str],
) -> str:
    if not findings:
        return "\n".join(
            [
                "## Findings",
                "",
                "No findings were generated for this file.",
            ]
        )

    sections = ["## Findings", ""]
    for index, finding in enumerate(findings):
        reference = references[index]
        sections.extend(
            [
                f"### {reference}: {CATEGORY_LABEL[finding.category]}",
                "",
                f"- Category: {CATEGORY_LABEL[finding.category]}",
                f"- Severity: {finding.severity}",
                f"- Confidence: {finding.confidence}",
                f"- Detection Method: {finding.detection_method}",
                f"- Line Numbers: {finding.line_start}-{finding.line_end}",
                "",
                "#### Source Text",
                "",
                "```text",
                finding.source_text,
                "```",
                "",
                "#### Explanation",
                "",
                finding.explanation,
                "",
                "#### Recommendation",
                "",
                finding.recommendation,
                "",
                "#### Suggested Replacement",
                "",
                finding.suggested_replacement or "No automatic suggestion generated.",
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
                finding.severity,
                finding.confidence,
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


def _build_review_philosophy() -> str:
    return "\n".join(
        [
            "## Review Philosophy",
            "",
            "- AI-assisted review",
            "- Human review required",
            "- No automatic source modification",
            "- Developer remains responsible",
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
