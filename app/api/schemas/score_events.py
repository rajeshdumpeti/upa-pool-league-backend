# app/api/schemas/score_events.py
# -----------------------------------------------------------------------------
# Purpose: Pydantic v2 schemas for batching score events for a match_game.
# -----------------------------------------------------------------------------
from typing import List, Optional, Literal, Any
from pydantic import BaseModel, Field


# Align these with your mobile ShotSymbol/types as needed
EventType = Literal[
    "X",  # striped pot
    "O",  # solid pot
    "M",  # miss
    "S",  # safety
    "F",  # foul
    "V",  # miss & foul
    "I",  # intentional foul
    "T",  # timeout
    "8",  # legal 8
]


class ScoreEventIn(BaseModel):
    ts: str = Field(..., description="Client event timestamp ISO-8601")
    actor_player_id: int = Field(..., description="Who performed the event")
    type: EventType
    # free-form extra info (we’ll store JSON in P1)
    payload_json: Optional[Any] = None
    rule_ref: Optional[str] = Field(None, description="Optional rules reference code")


class ScoreEventsBatchIn(BaseModel):
    events: List[ScoreEventIn] = Field(
        ..., min_length=1, max_length=500, description="Events for this game only"
    )


class ScoreEventsBatchAck(BaseModel):
    accepted: int
    game_id: int
