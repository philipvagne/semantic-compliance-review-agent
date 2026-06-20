from pydantic import BaseModel


class ReviewFinding(BaseModel):
    category: str
    severity: str
    confidence: str
    explanation: str
    recommendation: str
