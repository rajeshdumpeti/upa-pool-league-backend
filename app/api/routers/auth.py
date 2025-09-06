# app/api/routers/auth.py
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from app.api.schemas.auth import LoginRequest, TokenResponse, MeResponse
from app.core.config import settings
from app.core.security import create_access_token, decode_token
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer(auto_error=False)

# P0: static dev user. In P1 we'll check DB.
DEV_USER = {
    "email": "dev@example.com",
    "password": "password123",  # replace later with hashed DB value
}
now = datetime.utcnow()
user_id = DEV_USER["email"]  # Using email as a stable user identifier for dev
user_email = DEV_USER["email"]

DEV_USER = {
    "email": "dev@example.com",  # (or change to dev@upa.test if you prefer)
    "password": "password123",
}

@router.post("/login", response_model=TokenResponse, summary="Login (P0 stub)")
async def login(body: LoginRequest) -> TokenResponse:
    if body.email != DEV_USER["email"] or body.password != DEV_USER["password"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # REMOVE the unused manual payload you built earlier.

    # MINT a token that includes email/iss/aud/scope and matches decoder:
    token = create_access_token(sub=body.email, email=body.email, scope="mobile")
    return TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRES_MIN)

def get_current_subject(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        claims = decode_token(creds.credentials)
        return claims
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



@router.get("/me", response_model=MeResponse)
async def me(user=Depends(get_current_user)):
    return user