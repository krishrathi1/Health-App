from pydantic import BaseModel
from typing import Optional


class DoctorProfile(BaseModel):
    id: str
    name: str
    specialization: Optional[str] = None
    availability: bool = True

