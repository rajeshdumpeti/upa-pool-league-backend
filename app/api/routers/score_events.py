# app/api/routers/score_events.py
# -----------------------------------------------------------------------------
# Purpose: Accept a batch of score events for a given match_game (rack). P0 stub.
# -----------------------------------------------------------------------------
from fastapi import APIRouter, Depends
from app.api.schemas.score_events import ScoreEventsBatchIn, ScoreEventsBatchAck
from app.api.deps import require_user

router = APIRouter(prefix="/match-games", tags=["score_events"], dependencies=[Depends(require_user)])


@router.post("/{game_id}/score-events:batch", response_model=ScoreEventsBatchAck)
async def create_score_events_batch(
    game_id: int, body: ScoreEventsBatchIn
) -> ScoreEventsBatchAck:
    # P0: pretend we persisted; just acknowledge count so mobile can proceed.
    return ScoreEventsBatchAck(accepted=len(body.events), game_id=game_id)
