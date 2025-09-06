# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
import logging

# The same login path your router exposes
log = logging.getLogger("uvicorn")
_http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def require_user(
    creds: HTTPAuthorizationCredentials = Depends(_http_bearer),
):
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = creds.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"verify_aud": True, "verify_signature": True},
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    scope = payload.get("scope")
    if scope != "mobile":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope")

    # Minimal identity object for handlers to use if they want
    return {"sub": payload.get("sub"), "email": payload.get("email")}



def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        claims = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
        email = claims.get("email")
        scope = claims.get("scope")
        if not isinstance(email, str) or not email:
            raise ValueError("missing email")
        if scope != "mobile":  # <- match what we minted at login
            raise ValueError("invalid scope")

        return {"sub": claims.get("sub"), "email": email, "scope": scope}
    except JWTError as e:
        log.warning("JWT decode failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        log.warning("JWT claims invalid: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )