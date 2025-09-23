# app/db/repositories/teams.py
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.db.models import Team, Player, TeamPlayer
from types import SimpleNamespace

async def list_user_teams(db: AsyncSession, user_email: str) -> Sequence[Team]:
    # P0 rule: return all teams (until we have org/user/team mapping)
    # Replace with a proper membership filter in P1.
    result = await db.execute(select(Team).order_by(Team.name.asc()))
    return result.scalars().all()

async def list_team_players(db: AsyncSession, team_id: int) -> Sequence[SimpleNamespace]:
    """
    Return minimal player fields that we know exist in the DB (id, name, skill).
    Avoid selecting the whole Player model to prevent referencing non-existent columns
    like players.email in older schemas.
    """
    stmt = (
        select(Player.id, Player.name, Player.skill)
        .join(TeamPlayer, TeamPlayer.player_id == Player.id)
        .where(TeamPlayer.team_id == team_id)
        .order_by(Player.name.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()  # list of Row(id, name, skill)

    # Return simple structs compatible with the router's PlayerOut mapping
    return [SimpleNamespace(id=r.id, name=r.name, skill=r.skill) for r in rows]

# list all active teams
async def list_all_teams(db):
    result = await db.execute(
        text("SELECT id, name FROM teams WHERE is_active = true ORDER BY id")
    )
    return result.fetchall()
