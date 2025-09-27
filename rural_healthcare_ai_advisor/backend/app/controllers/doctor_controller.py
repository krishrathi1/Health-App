from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..utils.security_utils import get_current_user


router = APIRouter()


class DoctorProfile(BaseModel):
    name: str
    specialization: str | None = None
    availability: bool = True


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"user": user}


@router.post("/profile")
def update_profile(profile: DoctorProfile, user=Depends(get_current_user)):
    return {"ok": True, "profile": profile.dict(), "user": user}

