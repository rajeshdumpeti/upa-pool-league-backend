# app/db/models.py
from sqlalchemy import String, Boolean, ForeignKey, Integer  # <-- add Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    players: Mapped[list["TeamPlayer"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    skill: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class TeamPlayer(Base):
    __tablename__ = "team_players"
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), primary_key=True)
    is_captain: Mapped[bool] = mapped_column(Boolean, default=False)

    team: Mapped[Team] = relationship(back_populates="players")
    player: Mapped[Player] = relationship()
