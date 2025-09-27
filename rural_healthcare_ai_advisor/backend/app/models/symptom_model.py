from pydantic import BaseModel
from typing import Optional, List


class SymptomInput(BaseModel):
    text: str
    language: str = "en"
    audio_base64: Optional[str] = None
    symptoms: Optional[List[str]] = None

