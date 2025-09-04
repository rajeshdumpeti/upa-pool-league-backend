# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt
from app.core.config import settings

ALGO = "HS256"

def create_access_token(
    *, sub: str, scope: str = "mobile", expires_minutes: Optional[int] = None, extra: Dict[str, Any] | None = None
) -> str:
    now = datetime.now(timezone.utc)
    exp_min = expires_minutes or settings.JWT_EXPIRES_MIN
    payload: Dict[str, Any] = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_min)).timestamp()),
        "sub": sub,
        "scope": scope,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGO)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[ALGO],
        issuer=settings.JWT_ISSUER,
        audience=settings.JWT_AUDIENCE,
        options={"require_exp": True, "require_iat": True, "require_sub": True},
    )