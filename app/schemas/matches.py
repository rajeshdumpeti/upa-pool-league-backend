# app/api/schemas/matches.py
# -----------------------------------------------------------------------------
# Purpose: Pydantic models for Pre‑Match creation. These mirror what the mobile
# Pre‑Match screen will send, while staying DB‑agnostic for P0.
# -----------------------------------------------------------------------------
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, conlist

GameFormat = Literal["8-ball", "9-ball", "10-ball"]

class PlayerRef(BaseModel):
    id: int = Field(..., description="Player id from roster/lookup")
    name: Optional[str] = Field(None, description="Optional display name")
    skill: Optional[int] = Field(None, ge=1, le=10, description="Optional UPA skill (1-10)")

class TeamRef(BaseModel):
    id: int
    name: Optional[str] = None

class LineupEntry(BaseModel):
    order: int = Field(..., ge=1, description="1-based order in tonight's lineup")
    player: PlayerRef

class MatchCreateRequest(BaseModel):
    division_id: Optional[int] = Field(None, description="Division this match belongs to")
    date: Optional[str] = Field(None, description="ISO date (server may override)")
    format: GameFormat = "8-ball"
    home_team: TeamRef
    away_team: TeamRef
    # Exactly up to 5 entries per team is common; allow 1..8 for flexibility.
    home_lineup: conlist(LineupEntry, min_items=1, max_items=8)
    away_lineup: conlist(LineupEntry, min_items=1, max_items=8)
    coin_toss_winner_team_id: Optional[int] = Field(None, description="Team id that won toss")
    notes: Optional[str] = None

class MatchCreateResponse(BaseModel):
    id: int
    status: Literal["created", "accepted"] = "created"
    # Echo basic facts useful to the client
    format: GameFormat
    home_team_id: int
    away_team_id: int
