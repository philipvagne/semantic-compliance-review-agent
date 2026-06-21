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


class ReviewFinding(BaseModel):
    category: str
    severity: str
    confidence: str
    explanation: str
    recommendation: str
