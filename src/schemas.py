"""Define the structured data contracts used by the review pipeline.

Purpose:
- Provide shared schemas for file input, extracted text, review context, and
  structured findings.

Input:
- Data created by the file reader, extractor, context loader, and review layer.

Output:
- Validated schema objects used across the CLI pipeline.

Responsibilities:
- Centralize runtime data contracts.
- Constrain structured review output fields and allowed values.

Non-responsibilities:
- Read files.
- Extract text.
- Call models.
- Write reports.
"""

from typing import Literal

from pydantic import BaseModel


class FileContent(BaseModel):
    path: str
    filename: str
    extension: str
    raw_text: str
    line_count: int


class ReviewableText(BaseModel):
    id: str
    source_type: str
    text: str
    line_start: int
    line_end: int
    language: str
    surrounding_context: str


class ReviewContext(BaseModel):
    sensitive_terms: list[str]
    project_name: str | None
    project_description: str | None
    review_focus: list[str]
    config_warnings: list[str]


class Finding(BaseModel):
    id: str
    reviewable_text_id: str
    category: Literal[
        "SECURITY_RISK",
        "PROFESSIONALISM_RISK",
        "COMPLIANCE_RISK",
        "INTERNAL_CODENAME_EXPOSURE",
        "INTELLECTUAL_PROPERTY_RISK",
        "REPUTATION_RISK",
    ]
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    confidence: Literal["LOW", "MEDIUM", "HIGH"]
    detection_method: Literal["TERM_MATCH", "SEMANTIC_ANALYSIS", "HYBRID"]
    source_text: str
    line_start: int
    line_end: int
    explanation: str
    recommendation: str
    suggested_replacement: str | None


class ReviewFinding(BaseModel):
    category: str
    severity: str
    confidence: str
    explanation: str
    recommendation: str
