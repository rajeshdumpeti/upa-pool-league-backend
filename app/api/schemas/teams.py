from pydantic import BaseModel
from typing import Optional, List

class PlayerOut(BaseModel):
    id: int
    name: str
    skill: Optional[int] = None

class TeamOut(BaseModel):
    id: int
    name: str