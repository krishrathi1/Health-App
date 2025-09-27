from app.services.symptom_service import get_symptom_service
from app.models.symptom_model import SymptomInput


def test_emergency_rule_triggers():
    svc = get_symptom_service()
    res = svc.triage(SymptomInput(text="Patient has severe chest pain"))
    assert res.level == "emergency"

