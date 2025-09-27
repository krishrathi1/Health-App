import uuid
from typing import List, Dict


class ConsultService:
    def __init__(self):
        self._consults: Dict[str, dict] = {}

    def create_consult(self, user_id: str, symptoms_text: str, triage_level: str) -> dict:
        consult_id = str(uuid.uuid4())
        consult = {
            "id": consult_id,
            "user_id": user_id,
            "doctor_id": None,
            "triage_level": triage_level,
            "symptoms_text": symptoms_text,
            "status": "open",
            "messages": [],
        }
        self._consults[consult_id] = consult
        return consult

    def list_consults(self, user_id: str) -> List[dict]:
        return [c for c in self._consults.values() if c["user_id"] == user_id]


_global_consult_service: ConsultService | None = None


def get_consult_service() -> ConsultService:
    global _global_consult_service
    if _global_consult_service is None:
        _global_consult_service = ConsultService()
    return _global_consult_service

