from fastapi import APIRouter

from ..controllers.triage_controller import router as triage_router
from ..controllers.user_controller import router as user_router
from ..controllers.doctor_controller import router as doctor_router
from ..controllers.consult_controller import router as consult_router
from ..controllers.analytics_controller import router as analytics_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(doctor_router, prefix="/doctors", tags=["doctors"])
api_router.include_router(triage_router, prefix="/triage", tags=["triage"])
api_router.include_router(consult_router, prefix="/consults", tags=["consults"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])

