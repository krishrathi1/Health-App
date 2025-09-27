from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..utils.security_utils import AuthService, get_auth_service


router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    phone: str
    password: str


class LoginRequest(BaseModel):
    phone: str
    password: str


@router.post("/register")
def register(data: RegisterRequest, auth: AuthService = Depends(get_auth_service)):
    created = auth.register_user(name=data.name, phone=data.phone, password=data.password)
    if not created:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"ok": True}


@router.post("/login")
def login(data: LoginRequest, auth: AuthService = Depends(get_auth_service)):
    token = auth.login(phone=data.phone, password=data.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

