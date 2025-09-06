from fastapi import APIRouter, Depends
from app.api.schemas.teams import TeamOut, PlayerOut
from app.api.deps import get_current_user  # Adjusted import to match typical FastAPI project structure

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/my", response_model=list[TeamOut])
async def list_my_teams(user=Depends(get_current_user)):
    # P0 stub; later query DB by user/org/season
    return [
        TeamOut(id=101, name="Sharks"),
        TeamOut(id=202, name="Stripes"),
        TeamOut(id=303, name="Bank Rollers"),
    ]

@router.get("/{team_id}/players", response_model=list[PlayerOut])
async def list_team_players(team_id: int, user=Depends(get_current_user)):
    rosters = {
        101: [PlayerOut(id=1, name="Home Player 1", skill=5),
              PlayerOut(id=11, name="Home Player 2", skill=4)],
        202: [PlayerOut(id=2, name="Away Player 1", skill=4),
              PlayerOut(id=22, name="Away Player 2", skill=6)],
        303: [PlayerOut(id=3, name="Alt Player 1", skill=5)],
    }
    return rosters.get(team_id, [])