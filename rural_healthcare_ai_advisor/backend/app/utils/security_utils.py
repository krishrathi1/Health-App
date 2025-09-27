import base64
import hashlib
import hmac
import json
import time
import os
from typing import Optional, Dict
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config.settings import settings


_users_db: Dict[str, dict] = {}
_password_salt = os.getenv("PASSWORD_SALT", "static-salt").encode()


def _hash_password(password: str) -> str:
    return hashlib.sha256(_password_salt + password.encode()).hexdigest()


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _sign(data: bytes, key: bytes) -> str:
    return _b64url(hmac.new(key, data, hashlib.sha256).digest())


def _jwt_encode(payload: dict, secret: str) -> str:
    header = {"alg": settings.JWT_ALGORITHM, "typ": "JWT"}
    header_b64 = _b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    to_sign = f"{header_b64}.{payload_b64}".encode()
    signature = _sign(to_sign, secret.encode())
    return f"{header_b64}.{payload_b64}.{signature}"


def _jwt_decode(token: str, secret: str) -> Optional[dict]:
    try:
        header_b64, payload_b64, signature = token.split(".")
        to_sign = f"{header_b64}.{payload_b64}".encode()
        expected = _sign(to_sign, secret.encode())
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
        if payload.get("exp") and payload["exp"] < int(time.time()):
            return None
        return payload
    except Exception:
        return None


class AuthService:
    def register_user(self, name: str, phone: str, password: str) -> bool:
        if phone in _users_db:
            return False
        user_id = f"u_{len(_users_db)+1}"
        _users_db[phone] = {
            "id": user_id,
            "name": name,
            "phone": phone,
            "password_hash": _hash_password(password),
            "role": "patient",
        }
        return True

    def login(self, phone: str, password: str) -> Optional[str]:
        user = _users_db.get(phone)
        if not user or user["password_hash"] != _hash_password(password):
            return None
        now = int(time.time())
        exp = now + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        payload = {"sub": user["id"], "phone": phone, "role": user["role"], "exp": exp}
        return _jwt_encode(payload, settings.SECRET_KEY)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        for u in _users_db.values():
            if u["id"] == user_id:
                return {k: u[k] for k in ("id", "name", "phone", "role")}
        return None


_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), auth: AuthService = Depends(get_auth_service)):
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = _jwt_decode(creds.credentials, settings.SECRET_KEY)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = auth.get_user_by_id(payload["sub"]) or {"id": payload["sub"], "phone": payload.get("phone"), "role": payload.get("role")}
    return user


def encrypt_sensitive(data: bytes) -> str:
    key = settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else settings.SECRET_KEY.encode()
    mac = hmac.new(key, data, hashlib.sha256).digest()
    return _b64url(mac + data)


def decrypt_sensitive(token: str) -> bytes:
    raw = base64.urlsafe_b64decode(token + "==")
    return raw[32:]

