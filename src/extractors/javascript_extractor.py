"""Extract reviewable text from JavaScript-family source files.

Purpose:
- Convert JavaScript-family comments into ReviewableText records.

Input:
- FileContent for one `.js`, `.ts`, `.jsx`, or `.tsx` file.

Output:
- A list of ReviewableText objects extracted from comments and JSDoc blocks.

Responsibilities:
- Extract `//` line comments.
- Extract `/* ... */` block comments and `/** ... */` JSDoc blocks.
- Classify TODO, FIXME, and NOTE comments into distinct source types.
- Preserve line numbers, language, and surrounding context.

Non-responsibilities:
- Parse strings, imports, object keys, JSX visible text, or executable code.
- Classify risk or severity.
- Call the review agent.
- Generate reports or modify source files.
"""

from __future__ import annotations

import re

from src.schemas import FileContent
from src.schemas import ReviewableText


SPECIAL_COMMENT_PATTERN = re.compile(r"^(TODO|FIXME|NOTE)\b[:\-\s]?(.*)$", re.IGNORECASE)
JAVASCRIPT_EXTENSIONS = (".js", ".jsx")
TYPESCRIPT_EXTENSIONS = (".ts", ".tsx")


def extract_javascript_family_text(file_content: FileContent) -> list[ReviewableText]:
    language = _detect_language(file_content.extension.lower())
    raw_text = file_content.raw_text
    extracted: list[ReviewableText] = []

    index = 0
    line_number = 1
    length = len(raw_text)

    while index < length:
        current = raw_text[index]
        next_char = raw_text[index + 1] if index + 1 < length else ""

        if current == "\n":
            line_number += 1
            index += 1
            continue

        if current in ("'", '"'):
            index, line_number = _consume_quoted_string(raw_text, index, line_number, current)
            continue

        if current == "`":
            index, line_number = _consume_template_string(raw_text, index, line_number)
            continue

        if current == "/" and next_char == "/":
            comment_start = index
            comment_line_start = line_number
            index += 2
            while index < length and raw_text[index] != "\n":
                index += 1

            comment_text = raw_text[comment_start + 2 : index]
            cleaned_text = comment_text.strip()
            if cleaned_text:
                extracted.append(
                    _build_reviewable_text(
                        file_content=file_content,
                        source_type=_classify_comment_source_type(cleaned_text),
                        text=cleaned_text,
                        line_start=comment_line_start,
                        line_end=comment_line_start,
                        language=language,
                    )
                )
            continue

        if current == "/" and next_char == "*":
            is_jsdoc = index + 2 < length and raw_text[index + 2] == "*"
            comment_start = index
            comment_line_start = line_number
            index += 2
            comment_closed = False

            while index < length - 1:
                if raw_text[index] == "\n":
                    line_number += 1
                if raw_text[index] == "*" and raw_text[index + 1] == "/":
                    comment_body_end = index
                    index += 2
                    comment_closed = True
                    break
                index += 1

            if not comment_closed:
                comment_body_end = length
                index = length

            comment_line_end = line_number
            comment_body = raw_text[comment_start + 2 : comment_body_end]
            cleaned_text = _clean_block_comment_text(comment_body)
            if cleaned_text:
                extracted.append(
                    _build_reviewable_text(
                        file_content=file_content,
                        source_type=_classify_block_source_type(cleaned_text, is_jsdoc),
                        text=cleaned_text,
                        line_start=comment_line_start,
                        line_end=comment_line_end,
                        language=language,
                    )
                )
            continue

        index += 1

    return extracted


def _detect_language(extension: str) -> str:
    if extension in JAVASCRIPT_EXTENSIONS:
        return "javascript"
    if extension in TYPESCRIPT_EXTENSIONS:
        return "typescript"
    return "javascript"


def _consume_quoted_string(
    raw_text: str,
    index: int,
    line_number: int,
    quote_char: str,
) -> tuple[int, int]:
    index += 1
    length = len(raw_text)

    while index < length:
        current = raw_text[index]
        if current == "\\":
            index += 2
            continue
        if current == "\n":
            line_number += 1
        if current == quote_char:
            index += 1
            break
        index += 1

    return index, line_number


def _consume_template_string(raw_text: str, index: int, line_number: int) -> tuple[int, int]:
    index += 1
    length = len(raw_text)

    while index < length:
        current = raw_text[index]
        if current == "\\":
            index += 2
            continue
        if current == "\n":
            line_number += 1
        if current == "`":
            index += 1
            break
        index += 1

    return index, line_number


def _clean_block_comment_text(comment_body: str) -> str:
    cleaned_lines: list[str] = []
    for line in comment_body.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("*"):
            stripped_line = stripped_line[1:].lstrip()
        cleaned_lines.append(stripped_line)

    cleaned_text = "\n".join(cleaned_lines).strip()
    return cleaned_text


def _classify_comment_source_type(comment_text: str) -> str:
    match = SPECIAL_COMMENT_PATTERN.match(comment_text)
    if match:
        return match.group(1).upper()

    return "COMMENT"


def _classify_block_source_type(comment_text: str, is_jsdoc: bool) -> str:
    match = SPECIAL_COMMENT_PATTERN.match(comment_text)
    if match:
        return match.group(1).upper()

    if is_jsdoc:
        return "DOCSTRING"

    return "COMMENT"


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
