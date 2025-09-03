# app/api/routers/matches.py
# -----------------------------------------------------------------------------
# Purpose: Pre-Match endpoints. P0 returns a stubbed match id (no DB yet)
# so the mobile app can integrate / proceed. Later P1+ will persist to Postgres.
# -----------------------------------------------------------------------------
from fastapi import APIRouter, Body, status
from app.api.schemas.matches import (
    MatchCreateRequest,
    MatchCreateResponse,
    MatchSubmitted,
)

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post(
    "",
    response_model=MatchCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new match (stub)",
    description="Accepts Pre-Match details and returns a stub id. No DB writes in P0.",
)
async def create_match(payload: MatchCreateRequest) -> MatchCreateResponse:
    # Deterministic fake id (replace with DB in P1)
    # (e.g., hash of home/away team ids modulo a large number). In P1 we will replace this.
    fake_id = (payload.home_team.id * 10_000 + payload.away_team.id) % 1_000_000 or 42
    return MatchCreateResponse(
        id=fake_id,
        status="created",
        format=payload.format,
        home_team_id=payload.home_team.id,
        away_team_id=payload.away_team.id,
    )


@router.post(
    "/{match_id}/submit",
    response_model=MatchSubmitted,
    status_code=status.HTTP_200_OK,
    summary="Finalize/submit an entire match [stub]",
)
async def submit_match(
    match_id: int,
    _payload: dict | None = Body(default=None),  # accept/ignore body to avoid 422
) -> MatchSubmitted:
    return MatchSubmitted(id=match_id, status="submitted")