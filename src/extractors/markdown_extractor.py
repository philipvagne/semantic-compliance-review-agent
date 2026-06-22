"""Extract reviewable text from Markdown source files.

Purpose:
- Convert Markdown prose blocks into ReviewableText records.

Input:
- FileContent for one `.md` file.

Output:
- A list of ReviewableText objects extracted from headings, paragraphs, list
  items, and blockquotes.

Responsibilities:
- Extract headings, paragraphs, list items, and blockquotes.
- Classify TODO, FIXME, and NOTE items after removing Markdown block syntax.
- Exclude fenced code blocks and table rows.
- Preserve line numbers, language, and surrounding context.

Non-responsibilities:
- Parse fenced code blocks as source code.
- Extract table rows.
- Parse YAML, JSON, Dockerfile, or Terraform formats.
- Classify risk or severity.
- Call the review agent.
- Generate reports or modify source files.
"""

from __future__ import annotations

import re

from src.schemas import FileContent
from src.schemas import ReviewableText


SPECIAL_BLOCK_PATTERN = re.compile(
    r"^(TODO|FIXME|NOTE)\b[:\-\s]?(.*)$",
    re.IGNORECASE | re.DOTALL,
)
FENCE_PATTERN = re.compile(r"^\s*([`~]{3,})")
HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s*(.*?)\s*$")
UNORDERED_LIST_PATTERN = re.compile(r"^\s*[-*+]\s+(.*)$")
ORDERED_LIST_PATTERN = re.compile(r"^\s*\d+\.\s+(.*)$")
BLOCKQUOTE_PATTERN = re.compile(r"^\s*>\s?(.*)$")
TABLE_ROW_PATTERN = re.compile(r"^\s*\|")
SEPARATOR_ONLY_PATTERN = re.compile(r"^\s*[-_*:|]+\s*$")


def extract_markdown_text(file_content: FileContent) -> list[ReviewableText]:
    lines = file_content.raw_text.splitlines()
    extracted: list[ReviewableText] = []
    line_count = len(lines)
    index = 0
    in_fence = False
    fence_character = ""
    fence_length = 0

    while index < line_count:
        line = lines[index]
        stripped_line = line.strip()

        if in_fence:
            if _is_fence_close(stripped_line, fence_character, fence_length):
                in_fence = False
                fence_character = ""
                fence_length = 0
            index += 1
            continue

        if _is_fence_open(stripped_line):
            fence_match = FENCE_PATTERN.match(stripped_line)
            assert fence_match is not None
            fence_token = fence_match.group(1)
            in_fence = True
            fence_character = fence_token[0]
            fence_length = len(fence_token)
            index += 1
            continue

        if not stripped_line or _should_ignore_line(stripped_line):
            index += 1
            continue

        heading_text = _extract_heading_text(line)
        if heading_text is not None:
            extracted.append(
                _build_reviewable_text(
                    file_content=file_content,
                    source_type=_classify_block_source_type(heading_text, "HEADING"),
                    text=heading_text,
                    line_start=index + 1,
                    line_end=index + 1,
                    language="markdown",
                )
            )
            index += 1
            continue

        list_item_text = _extract_list_item_text(line)
        if list_item_text is not None:
            extracted.append(
                _build_reviewable_text(
                    file_content=file_content,
                    source_type=_classify_block_source_type(list_item_text, "LIST_ITEM"),
                    text=list_item_text,
                    line_start=index + 1,
                    line_end=index + 1,
                    language="markdown",
                )
            )
            index += 1
            continue

        blockquote_match = BLOCKQUOTE_PATTERN.match(line)
        if blockquote_match is not None:
            line_start = index + 1
            blockquote_lines: list[str] = []

            while index < line_count:
                current_line = lines[index]
                current_match = BLOCKQUOTE_PATTERN.match(current_line)
                if current_match is None:
                    break
                blockquote_lines.append(current_match.group(1).strip())
                index += 1

            blockquote_text = "\n".join(blockquote_lines).strip()
            if blockquote_text:
                extracted.append(
                    _build_reviewable_text(
                        file_content=file_content,
                        source_type=_classify_block_source_type(blockquote_text, "BLOCKQUOTE"),
                        text=blockquote_text,
                        line_start=line_start,
                        line_end=index,
                        language="markdown",
                    )
                )
            continue

        line_start = index + 1
        paragraph_lines: list[str] = []

        while index < line_count and _is_paragraph_line(lines[index]):
            paragraph_lines.append(lines[index].strip())
            index += 1

        paragraph_text = " ".join(paragraph_lines).strip()
        if paragraph_text:
            extracted.append(
                _build_reviewable_text(
                    file_content=file_content,
                    source_type=_classify_block_source_type(paragraph_text, "PARAGRAPH"),
                    text=paragraph_text,
                    line_start=line_start,
                    line_end=index,
                    language="markdown",
                )
            )

    return extracted


def _is_fence_open(stripped_line: str) -> bool:
    return FENCE_PATTERN.match(stripped_line) is not None


def _is_fence_close(stripped_line: str, fence_character: str, fence_length: int) -> bool:
    if not stripped_line.startswith(fence_character * fence_length):
        return False

    return set(stripped_line) <= {fence_character, " "}


def _should_ignore_line(stripped_line: str) -> bool:
    return TABLE_ROW_PATTERN.match(stripped_line) is not None or (
        SEPARATOR_ONLY_PATTERN.match(stripped_line) is not None
    )


def _extract_heading_text(line: str) -> str | None:
    match = HEADING_PATTERN.match(line)
    if match is None:
        return None

    heading_text = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
    if not heading_text:
        return None

    return heading_text


def _extract_list_item_text(line: str) -> str | None:
    unordered_match = UNORDERED_LIST_PATTERN.match(line)
    if unordered_match is not None:
        return unordered_match.group(1).strip() or None

    ordered_match = ORDERED_LIST_PATTERN.match(line)
    if ordered_match is not None:
        return ordered_match.group(1).strip() or None

    return None


def _is_paragraph_line(line: str) -> bool:
    stripped_line = line.strip()
    if not stripped_line or _should_ignore_line(stripped_line):
        return False
    if _is_fence_open(stripped_line):
        return False
    if _extract_heading_text(line) is not None:
        return False
    if _extract_list_item_text(line) is not None:
        return False
    if BLOCKQUOTE_PATTERN.match(line) is not None:
        return False
    return True


def _classify_block_source_type(block_text: str, default_source_type: str) -> str:
    match = SPECIAL_BLOCK_PATTERN.match(block_text)
    if match:
        return match.group(1).upper()

    return default_source_type


def _build_reviewable_text(
    file_content: FileContent,
    source_type: str,
    text: str,
    line_start: int,
    line_end: int,
    language: str,
) -> ReviewableText:
    return ReviewableText(
        id="",
        source_type=source_type,
        text=text,
        line_start=line_start,
        line_end=line_end,
        language=language,
        surrounding_context=_build_surrounding_context(
            file_content.raw_text,
            line_start,
            line_end,
        ),
    )


def _build_surrounding_context(raw_text: str, line_start: int, line_end: int) -> str:
    lines = raw_text.splitlines()
    if not lines:
        return ""

    start_index = max(0, line_start - 2)
    end_index = min(len(lines), line_end + 1)
    return "\n".join(lines[start_index:end_index])
