# app/api/schemas/match_games.py
# -----------------------------------------------------------------------------
# Purpose: Pydantic v2 schemas for creating & completing a match game (rack).
# -----------------------------------------------------------------------------
from typing import Literal, Optional
from pydantic import BaseModel, Field

GameFormat = Literal["8-ball", "9-ball", "10-ball"]


class CreateMatchGame(BaseModel):
    match_id: int = Field(..., description="Server match id")
    game_no: int = Field(..., ge=1, description="1-based rack number")
    format: GameFormat = "8-ball"
    home_player_id: int
    away_player_id: int
    breaker_player_id: Optional[int] = None
    started_at: Optional[str] = Field(None, description="ISO timestamp")


class MatchGameCreated(BaseModel):
    id: int
    match_id: int
    game_no: int


class CompleteMatchGame(BaseModel):
    winner_player_id: int
    innings: int = 0
    defensive_shots: int = 0
    timeouts: int = 0
    fouls: int = 0
    ended_at: Optional[str] = Field(None, description="ISO timestamp")


class MatchGamePatched(BaseModel):
    id: int
    status: Literal["completed"] = "completed"