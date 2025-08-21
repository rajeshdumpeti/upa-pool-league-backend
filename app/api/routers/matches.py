# app/api/routers/matches.py
# -----------------------------------------------------------------------------
# Purpose: Pre‑Match endpoints. P0 returns a stubbed match id (no DB yet)
# so the mobile app can integrate / proceed. Later P1+ will persist to Postgres.
# -----------------------------------------------------------------------------
from fastapi import APIRouter, status
from app.api.schemas.matches import MatchCreateRequest, MatchCreateResponse

router = APIRouter(prefix="/matches", tags=["matches"])

# In P0 we do not hit the DB. We return a deterministic fake id so mobile can proceed.
# Use 201 Created to signal resource creation semantics.
@router.post(
    "",
    response_model=MatchCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new match (stub)",
    description="Accepts Pre‑Match details and returns a stub id. No DB writes in P0."
)
async def create_match(payload: MatchCreateRequest) -> MatchCreateResponse:
    # Simple deterministic fake id so each request is distinguishable without a DB.
    # (e.g., hash of home/away team ids modulo a large number). In P1 we will replace this.
    fake_id = (payload.home_team.id * 10_000 + payload.away_team.id) % 1_000_000 or 42
    return MatchCreateResponse(
        id=fake_id,
        status="created",
        format=payload.format,
        home_team_id=payload.home_team.id,
        away_team_id=payload.away_team.id,
    )
