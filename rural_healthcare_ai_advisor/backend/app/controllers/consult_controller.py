from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services.consult_service import ConsultService, get_consult_service
from ..utils.security_utils import get_current_user


router = APIRouter()


class CreateConsultRequest(BaseModel):
    symptoms_text: str
    triage_level: str


@router.post("")
def create_consult(req: CreateConsultRequest, svc: ConsultService = Depends(get_consult_service), user=Depends(get_current_user)):
    return svc.create_consult(user_id=user["id"], symptoms_text=req.symptoms_text, triage_level=req.triage_level)


@router.get("")
def list_consults(svc: ConsultService = Depends(get_consult_service), user=Depends(get_current_user)):
    return svc.list_consults(user_id=user["id"]) 

