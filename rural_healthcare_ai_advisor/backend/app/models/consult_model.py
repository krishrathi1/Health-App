from pydantic import BaseModel
from typing import Optional, List


class Consult(BaseModel):
    id: str
    user_id: str
    doctor_id: Optional[str]
    triage_level: str
    symptoms_text: str
    status: str  # open | assigned | closed
    messages: List[dict] = []

