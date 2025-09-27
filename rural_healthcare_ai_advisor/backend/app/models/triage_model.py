from pydantic import BaseModel
from typing import List, Optional


class TriageResult(BaseModel):
    level: str  # emergency | urgent | homecare
    reasons: List[str]
    advice: str
    language: str = "en"
    confidence: Optional[float] = None

