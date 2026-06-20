from pydantic import BaseModel


class FileContent(BaseModel):
    path: str
    filename: str
    extension: str
    raw_text: str
    line_count: int


class ReviewFinding(BaseModel):
    category: str
    severity: str
    confidence: str
    explanation: str
    recommendation: str
