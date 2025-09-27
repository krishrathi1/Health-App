from fastapi import APIRouter, Depends
from ..models.symptom_model import SymptomInput
from ..models.triage_model import TriageResult
from ..services.symptom_service import SymptomService, get_symptom_service


router = APIRouter()


@router.post("/classify", response_model=TriageResult)
def classify_symptoms(payload: SymptomInput, service: SymptomService = Depends(get_symptom_service)) -> TriageResult:
    return service.triage(payload)

