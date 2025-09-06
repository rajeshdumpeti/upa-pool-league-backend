# add at top if missing
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

# REPLACE your existing create_access_token with:
def create_access_token(*, sub: str, email: str, scope: str = "mobile", expires_minutes: int | None = None) -> str:
    now = datetime.utcnow()
    exp_mins = expires_minutes or settings.JWT_EXPIRES_MIN
    payload = {
        "sub": sub,
        "email": email.lower(),
        "scope": scope,
        "iss": settings.JWT_ISSUER,   # <- must match decode
        "aud": settings.JWT_AUDIENCE, # <- must match decode
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_mins)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

# REPLACE your existing decode_token (ensure issuer/audience verified):
def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=["HS256"],
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
    )