# scripts/seed_dev.py
"""
Dev seed: insert a few teams, players, and roster links.
- Idempotent (safe to re-run)
- Respects NOT NULL constraints (is_active, is_captain, etc.)
- Uses Postgres ON CONFLICT upserts
"""

import asyncio
from typing import Sequence

from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import text
from app.core.config import settings

# ---- Data --------------------------------------------------------------------

TEAMS = [
    # id, name, is_active
    (101, "Bulleyes Breaker", True),
    (202, "Stripes", True),
    (303, "Bank Rollers", True),
]

PLAYERS = [
    # id, name, skill, is_active
    (1,  "Rajesh Dumpeti",  5, True),
    (2,  "Sandeep Prasad",  7, True),
    (3,  "Sanjeev Tegula",  5, True),
    (4,  "Shina",  3, True),
    (5,  "Rangi",  5, True),
    

    (11, "Eve Evans",       4, True),
    (12, "Frank Foster",    5, True),
    (13, "Grace Green",     6, True),
    (14, "Hank Harris",     7, True),

    (21, "Ivy Irving",      4, True),
    (22, "Jack Johnson",    6, True),
    (23, "Kara King",       5, True),
    (24, "Liam Lewis",      3, True),
]

# team_id, player_id, is_captain
ROSTER = [
    (101, 1,  True), (101, 11, False), (101, 12, False), (101, 13, False),
    (202, 2,  True), (202, 21, False), (202, 22, False), (202, 23, False),
    (303, 3,  True), (303, 4,  False), (303, 14, False), (303, 24, False),
]

# ---- SQL templates (Postgres) -----------------------------------------------

UPSERT_TEAM = text("""
INSERT INTO teams (id, name, is_active)
VALUES (:id, :name, :is_active)
ON CONFLICT (id) DO UPDATE
    SET name = EXCLUDED.name,
        is_active = EXCLUDED.is_active
""")

UPSERT_PLAYER = text("""
INSERT INTO players (id, name, skill, is_active)
VALUES (:id, :name, :skill, :is_active)
ON CONFLICT (id) DO UPDATE
    SET name = EXCLUDED.name,
        skill = EXCLUDED.skill,
        is_active = EXCLUDED.is_active
""")

UPSERT_TEAM_PLAYER = text("""
INSERT INTO team_players (team_id, player_id, is_captain)
VALUES (:team_id, :player_id, :is_captain)
ON CONFLICT (team_id, player_id) DO UPDATE
    SET is_captain = EXCLUDED.is_captain
""")

COUNT_TEAMS = text("SELECT COUNT(*) FROM teams")
COUNT_PLAYERS = text("SELECT COUNT(*) FROM players")
COUNT_TP = text("SELECT COUNT(*) FROM team_players")

# ---- Seed runner -------------------------------------------------------------

async def upsert_many(conn: AsyncConnection, sql: text, rows: Sequence[dict]):
    if not rows:
        return
    await conn.execute(sql, rows)

async def seed():
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        # teams
        await upsert_many(conn, UPSERT_TEAM, [
            {"id": t[0], "name": t[1], "is_active": t[2]} for t in TEAMS
        ])

        # players
        await upsert_many(conn, UPSERT_PLAYER, [
            {"id": p[0], "name": p[1], "skill": p[2], "is_active": p[3]} for p in PLAYERS
        ])

        # roster links (captains)
        await upsert_many(conn, UPSERT_TEAM_PLAYER, [
            {"team_id": r[0], "player_id": r[1], "is_captain": r[2]} for r in ROSTER
        ])

        # quick counts
        t = (await conn.execute(COUNT_TEAMS)).scalar_one()
        p = (await conn.execute(COUNT_PLAYERS)).scalar_one()
        tp = (await conn.execute(COUNT_TP)).scalar_one()

    await engine.dispose()
    print(f"✓ Seed complete → teams={t}, players={p}, team_players={tp}")

if __name__ == "__main__":
    asyncio.run(seed())
