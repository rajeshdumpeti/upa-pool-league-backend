# app/api/routers/teams.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.teams import list_all_teams  # add this import
from app.api.schemas.teams import TeamOut, PlayerOut
from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.repositories.teams import list_user_teams, list_team_players

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/my", response_model=List[TeamOut])
async def get_my_teams(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    teams = await list_user_teams(db, user_email=user["email"])
    return [TeamOut(id=t.id, name=t.name) for t in teams]

@router.get("/{team_id}/players", response_model=List[PlayerOut])
async def get_team_players(
    team_id: int,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    players = await list_team_players(db, team_id=team_id)
    return [PlayerOut(id=p.id, name=p.name, skill=p.skill) for p in players]


@router.get("", response_model=List[TeamOut])
async def list_teams(
    _user=Depends(get_current_user),  # keep auth if you want
    db: AsyncSession = Depends(get_db),
):
    teams = await list_all_teams(db)
    return [TeamOut(id=t.id, name=t.name) for t in teams]