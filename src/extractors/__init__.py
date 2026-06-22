"""Extraction helpers for language-specific reviewable text handling.

Purpose:
- Provide narrow extractor modules for supported source-language families.

Input:
- FileContent objects from the file reader.

Output:
- Lists of ReviewableText items for each supported extractor family.

Responsibilities:
- Keep language-specific extraction logic isolated from the dispatcher.
- Preserve the extraction-only boundary of the pipeline.

Non-responsibilities:
- Read files.
- Review risk.
- Write reports.
- Modify source files.
"""

from src.extractors.javascript_extractor import extract_javascript_family_text

__all__ = ["extract_javascript_family_text"]
