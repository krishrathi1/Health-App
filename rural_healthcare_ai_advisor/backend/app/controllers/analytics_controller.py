from fastapi import APIRouter, Depends
from ..services.analytics_service import AnalyticsService, get_analytics_service
from ..utils.security_utils import get_current_user


router = APIRouter()


@router.get("/overview")
def overview(svc: AnalyticsService = Depends(get_analytics_service), user=Depends(get_current_user)):
    return svc.get_overview_metrics()

