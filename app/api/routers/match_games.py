# app/api/routers/match_games.py
# -----------------------------------------------------------------------------
# Purpose: Stub endpoints for creating & completing match games (racks).
# These return deterministic fake IDs so the mobile app can integrate now.
# -----------------------------------------------------------------------------
from fastapi import APIRouter, status
from app.api.schemas.match_games import (
    CreateMatchGame,
    MatchGameCreated,
    CompleteMatchGame,
    MatchGamePatched,
)

router = APIRouter(prefix="/match-games", tags=["match_games"])


@router.post(
    "",
    response_model=MatchGameCreated,
    status_code=status.HTTP_201_CREATED,
    summary="Create a match game (rack) [stub]",
)
async def create_match_game(payload: CreateMatchGame) -> MatchGameCreated:
    # Deterministic fake id for now (keeps results stable)
    fake_id = payload.match_id * 10_000 + payload.game_no
    return MatchGameCreated(
        id=fake_id, match_id=payload.match_id, game_no=payload.game_no
    )


@router.patch(
    "/{game_id}/complete",
    response_model=MatchGamePatched,
    summary="Complete a match game with summary stats [stub]",
)
async def complete_match_game(
    game_id: int, patch: CompleteMatchGame
) -> MatchGamePatched:
    # In P1 we will persist and validate. For P0 we just echo success.
    return MatchGamePatched(id=game_id, status="completed")
