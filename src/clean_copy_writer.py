"""Generate conservative clean-copy files from safe suggested replacements.

Purpose:
- Create a separate clean-copy artifact under `output/` without modifying the
  original source file.

Input:
- FileContent
- ReviewableText[]
- Finding[]

Output:
- One clean-copy file path plus an application summary.

Responsibilities:
- Apply only safe, exact suggested replacements.
- Skip ambiguous or missing replacements conservatively.
- Preserve the original file by writing only to a separate output file.

Non-responsibilities:
- Modify the original source file.
- Infer new replacements.
- Perform AST-aware transforms, formatting, or patch generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.schemas import FileContent
from src.schemas import Finding
from src.schemas import ReviewableText


@dataclass(frozen=True)
class CleanCopySkippedReplacement:
    finding_id: str
    line_start: int
    line_end: int
    source_text: str
    reason: str


@dataclass(frozen=True)
class CleanCopyResult:
    output_path: str
    applied_count: int
    skipped_count: int
    skipped_replacements: list[CleanCopySkippedReplacement]


class CleanCopyWriteError(Exception):
    """Raised when clean-copy generation cannot complete safely."""


def generate_clean_copy(
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    findings: list[Finding],
    output_dir: str = "output",
) -> CleanCopyResult:
    _validate_inputs(file_content, reviewable_texts, findings)

    reviewable_text_set = {item.text for item in reviewable_texts}
    original_text = file_content.raw_text
    updated_text = original_text
    applied_count = 0
    skipped_replacements: list[CleanCopySkippedReplacement] = []

    for finding in findings:
        skip_reason = _get_skip_reason(
            finding=finding,
            original_text=original_text,
            current_text=updated_text,
            reviewable_text_set=reviewable_text_set,
        )
        if skip_reason:
            skipped_replacements.append(
                CleanCopySkippedReplacement(
                    finding_id=finding.id,
                    line_start=finding.line_start,
                    line_end=finding.line_end,
                    source_text=finding.source_text,
                    reason=skip_reason,
                )
            )
            continue

        updated_text = updated_text.replace(
            finding.source_text,
            finding.suggested_replacement.strip(),
            1,
        )
        applied_count += 1

    output_directory = Path(output_dir)
    try:
        output_directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CleanCopyWriteError(
            f"Unable to create clean-copy output directory: {output_directory}"
        ) from exc

    output_path = output_directory / (
        f"{Path(file_content.filename).stem}-clean-copy{file_content.extension}"
    )
    try:
        output_path.write_text(updated_text, encoding="utf-8")
    except OSError as exc:
        raise CleanCopyWriteError(
            f"Unable to write clean-copy file: {output_path}"
        ) from exc
    except Exception as exc:
        raise CleanCopyWriteError(
            f"Unexpected clean-copy write failure for {output_path}"
        ) from exc

    return CleanCopyResult(
        output_path=str(output_path).replace("\\", "/"),
        applied_count=applied_count,
        skipped_count=len(skipped_replacements),
        skipped_replacements=skipped_replacements,
    )


def _validate_inputs(
    file_content: FileContent,
    reviewable_texts: list[ReviewableText],
    findings: list[Finding],
) -> None:
    if not isinstance(file_content, FileContent):
        raise CleanCopyWriteError(
            "Invalid clean-copy data received: file_content must be FileContent."
        )
    if not isinstance(reviewable_texts, list) or any(
        not isinstance(item, ReviewableText) for item in reviewable_texts
    ):
        raise CleanCopyWriteError(
            "Invalid clean-copy data received: reviewable_texts must be list[ReviewableText]."
        )
    if not isinstance(findings, list) or any(not isinstance(item, Finding) for item in findings):
        raise CleanCopyWriteError(
            "Invalid clean-copy data received: findings must be list[Finding]."
        )


def _get_skip_reason(
    *,
    finding: Finding,
    original_text: str,
    current_text: str,
    reviewable_text_set: set[str],
) -> str | None:
    source_text = finding.source_text
    suggested_replacement = (finding.suggested_replacement or "").strip()

    if not source_text:
        return "Source text is missing."
    if not suggested_replacement:
        return "Suggested replacement is missing."
    if suggested_replacement.lower() == "(none)":
        return "Suggested replacement was marked as '(none)'."
    if source_text not in reviewable_text_set:
        return "Source text does not exactly match extracted reviewable text."
    if source_text == suggested_replacement:
        return "Suggested replacement is identical to the source text."

    source_text_count = original_text.count(source_text)
    if source_text_count == 0:
        return "Source text does not appear in the original file."
    if source_text_count > 1:
        return "Source text appears more than once in the original file."

    current_text_count = current_text.count(source_text)
    if current_text_count == 0:
        return "Source text no longer appears uniquely after earlier replacements."
    if current_text_count > 1:
        return "Replacement became ambiguous after earlier replacements."

    return None
