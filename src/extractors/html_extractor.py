"""Extract reviewable text from HTML source files.

Purpose:
- Convert HTML comments into ReviewableText records.

Input:
- FileContent for one `.html` file.

Output:
- A list of ReviewableText objects extracted from HTML comments.

Responsibilities:
- Extract `<!-- ... -->` comments.
- Classify TODO, FIXME, and NOTE comments into distinct source types.
- Ignore script and style contents while scanning for HTML comments.
- Preserve line numbers, language, and surrounding context.

Non-responsibilities:
- Parse visible page text, attributes, meta tags, or executable code.
- Parse JavaScript inside script tags or CSS inside style tags.
- Classify risk or severity.
- Call the review agent.
- Generate reports or modify source files.
"""

from __future__ import annotations

import re

from src.schemas import FileContent
from src.schemas import ReviewableText


SPECIAL_COMMENT_PATTERN = re.compile(
    r"^(TODO|FIXME|NOTE)\b[:\-\s]?(.*)$",
    re.IGNORECASE | re.DOTALL,
)
SCRIPT_OR_STYLE_OPEN_PATTERN = re.compile(r"<(script|style)\b", re.IGNORECASE)
SCRIPT_OR_STYLE_CLOSE_TEMPLATE = r"</{tag}\s*>"


def extract_html_text(file_content: FileContent) -> list[ReviewableText]:
    raw_text = file_content.raw_text
    extracted: list[ReviewableText] = []
    length = len(raw_text)
    index = 0

    while index < length:
        if raw_text.startswith("<!--", index):
            comment_start = index
            content_start = index + 4
            content_end = raw_text.find("-->", content_start)
            if content_end == -1:
                content_end = length
                index = length
            else:
                index = content_end + 3

            cleaned_text = raw_text[content_start:content_end].strip()
            if cleaned_text:
                line_start = _line_number_at(raw_text, comment_start)
                line_end = _line_number_at(raw_text, content_end)
                extracted.append(
                    ReviewableText(
                        id="",
                        source_type=_classify_comment_source_type(cleaned_text),
                        text=cleaned_text,
                        line_start=line_start,
                        line_end=line_end,
                        language="html",
                        surrounding_context=_build_surrounding_context(
                            raw_text,
                            line_start,
                            line_end,
                        ),
                    )
                )
            continue

        script_or_style_match = SCRIPT_OR_STYLE_OPEN_PATTERN.match(raw_text, index)
        if script_or_style_match:
            tag_name = script_or_style_match.group(1).lower()
            tag_open_end = raw_text.find(">", script_or_style_match.end())
            if tag_open_end == -1:
                break

            close_pattern = re.compile(
                SCRIPT_OR_STYLE_CLOSE_TEMPLATE.format(tag=tag_name),
                re.IGNORECASE,
            )
            close_match = close_pattern.search(raw_text, tag_open_end + 1)
            if close_match is None:
                break

            index = close_match.end()
            continue

        index += 1

    return extracted


def _classify_comment_source_type(comment_text: str) -> str:
    match = SPECIAL_COMMENT_PATTERN.match(comment_text)
    if match:
        return match.group(1).upper()

    return "COMMENT"


def _line_number_at(raw_text: str, index: int) -> int:
    return raw_text.count("\n", 0, index) + 1


def _build_surrounding_context(raw_text: str, line_start: int, line_end: int) -> str:
    lines = raw_text.splitlines()
    if not lines:
        return ""

    start_index = max(0, line_start - 2)
    end_index = min(len(lines), line_end + 1)
    return "\n".join(lines[start_index:end_index])
