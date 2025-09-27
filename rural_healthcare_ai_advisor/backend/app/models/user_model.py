from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: str
    name: str
    phone: str
    role: str = Field(default="patient")


class Doctor(BaseModel):
    id: str
    name: str
    phone: str
    specialization: Optional[str] = None
    role: str = Field(default="doctor")

