# app/api/routers/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/live")
async def health_live() -> JSONResponse:
    # Liveness: process is up
    return JSONResponse({"ok": True, "service": "upa-pool-league-app", "check": "Welcome to UPA Pool League API!"})

@router.get("/ready")
async def health_ready() -> JSONResponse:
    # Readiness: dependencies OK (wire DB/Redis checks here later)
    return JSONResponse({"ok": True, "service": "upa-api", "check": "Welcome to UPA Pool League API!"})
