"""Extract reviewable human-written text from one source file.

Purpose:
- Convert FileContent into reviewable text records for later compliance review.

Input:
- FileContent for a single source file.

Output:
- A list of ReviewableText objects.

Responsibilities:
- Extract Python comments and docstrings.
- Extract JavaScript-family comments and JSDoc blocks.
- Classify TODO, FIXME, and NOTE comments into distinct source types.
- Preserve line numbers, language, and surrounding context.

Non-responsibilities:
- Extract string literals.
- Classify risk or severity.
- Call the review agent.
- Generate reports or modify source files.
"""

from __future__ import annotations

import ast
import io
import re
import tokenize

from src.extractors import extract_javascript_family_text
from src.schemas import FileContent
from src.schemas import ReviewableText


SPECIAL_COMMENT_PATTERN = re.compile(r"^(TODO|FIXME|NOTE)\b[:\-\s]?(.*)$", re.IGNORECASE)
PYTHON_SOURCE_EXTENSIONS = (".py",)
JAVASCRIPT_FAMILY_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx")
SUPPORTED_SOURCE_EXTENSIONS = PYTHON_SOURCE_EXTENSIONS + JAVASCRIPT_FAMILY_EXTENSIONS


class ExtractionError(Exception):
    """Raised when reviewable text extraction fails unexpectedly."""


def extract_reviewable_text(file_content: FileContent) -> list[ReviewableText]:
    _validate_supported_file_type(file_content)

    if file_content.extension.lower() in JAVASCRIPT_FAMILY_EXTENSIONS:
        extracted_items = extract_javascript_family_text(file_content)
        for index, item in enumerate(extracted_items, start=1):
            item.id = _build_item_id(file_content, item, index)
        return extracted_items

    try:
        comments = _extract_comments(file_content)
        docstrings = _extract_docstrings(file_content)
    except (SyntaxError, tokenize.TokenError, OSError, ValueError) as exc:
        raise ExtractionError(f"Failed to extract reviewable text from {file_content.path}") from exc
    except Exception as exc:
        raise ExtractionError(f"Unexpected extraction failure for {file_content.path}") from exc

    extracted_items = sorted(
        comments + docstrings,
        key=lambda item: (item.line_start, item.line_end, item.source_type, item.text),
    )

    for index, item in enumerate(extracted_items, start=1):
        item.id = _build_item_id(file_content, item, index)

    return extracted_items


def _validate_supported_file_type(file_content: FileContent) -> None:
    extension = file_content.extension.lower() or "[no extension]"
    if extension in SUPPORTED_SOURCE_EXTENSIONS:
        return

    supported_types = ", ".join(SUPPORTED_SOURCE_EXTENSIONS)
    raise ExtractionError(
        f"Unsupported file type '{extension}' for semantic review. "
        f"Current supported file types: {supported_types}. "
        "No audit was performed."
    )


def _extract_comments(file_content: FileContent) -> list[ReviewableText]:
    extracted: list[ReviewableText] = []
    reader = io.StringIO(file_content.raw_text).readline

    for token in tokenize.generate_tokens(reader):
        if token.type != tokenize.COMMENT:
            continue

        cleaned_text = token.string.lstrip("#").strip()
        if not cleaned_text:
            continue

        source_type = _classify_comment_source_type(cleaned_text)
        line_start = token.start[0]
        line_end = token.end[0]

        extracted.append(
            ReviewableText(
                id="",
                source_type=source_type,
                text=cleaned_text,
                line_start=line_start,
                line_end=line_end,
                language="python",
                surrounding_context=_build_surrounding_context(
                    file_content.raw_text,
                    line_start,
                    line_end,
                ),
            )
        )

    return extracted


def _extract_docstrings(file_content: FileContent) -> list[ReviewableText]:
    tree = ast.parse(file_content.raw_text, filename=file_content.path)
    extracted: list[ReviewableText] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if not node.body:
            continue

        first_statement = node.body[0]
        if not _is_docstring_expression(first_statement):
            continue

        docstring_value = first_statement.value.value.strip()
        if not docstring_value:
            continue

        line_start = first_statement.lineno
        line_end = getattr(first_statement, "end_lineno", first_statement.lineno)

        extracted.append(
            ReviewableText(
                id="",
                source_type="DOCSTRING",
                text=docstring_value,
                line_start=line_start,
                line_end=line_end,
                language="python",
                surrounding_context=_build_surrounding_context(
                    file_content.raw_text,
                    line_start,
                    line_end,
                ),
            )
        )

    return extracted


def _is_docstring_expression(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _classify_comment_source_type(comment_text: str) -> str:
    match = SPECIAL_COMMENT_PATTERN.match(comment_text)
    if match:
        return match.group(1).upper()

    return "COMMENT"


def _build_surrounding_context(raw_text: str, line_start: int, line_end: int) -> str:
    lines = raw_text.splitlines()
    if not lines:
        return ""

    start_index = max(0, line_start - 2)
    end_index = min(len(lines), line_end + 1)
    return "\n".join(lines[start_index:end_index])


def _build_item_id(file_content: FileContent, item: ReviewableText, index: int) -> str:
    return f"{file_content.filename}:{item.source_type.lower()}:{item.line_start}:{index}"
