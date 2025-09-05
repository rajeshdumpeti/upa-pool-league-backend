# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# app/main.py (only showing the new lines)
from app.api.routers import auth, health, matches, match_games, score_events, teams

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="upa-api",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# --- CORS ---
# Note: Native mobile apps are not subject to CORS, but enabling it helps for:
# - Web previews (Expo web), admin tools, embedded webviews, etc.
# We use regex to allow any Render subdomain and ngrok tunnel.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^(https?://localhost(:\d+)?|https?://127\.0\.0\.1(:\d+)?|https://[a-z0-9\-]+\.onrender\.com|https://[a-z0-9\-]+\.ngrok-free\.app)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers (versioned API) ---
app.include_router(health.router, prefix="/api/v1")


# --- Root ping (non-versioned) ---
@app.get("/", tags=["root"])
def root():
    """
    Lightweight root ping so platform health checks (or a browser) get an immediate response.
    """
    return {"service": "upa-pool-league-api", "status": "ok", "version": "1.0.0"}


# Optional: log startup nicely
@app.on_event("startup")
async def on_startup():
    logger.info("upa-api starting up")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("upa-api shutting down")


# Mount versioned API routes

# app/main.py  (only new import/include shown)

app.include_router(health.router, prefix="/api/v1")
app.include_router(matches.router, prefix="/api/v1")
app.include_router(match_games.router, prefix="/api/v1")
app.include_router(score_events.router, prefix="/api/v1")  # NEW
app.include_router(auth.router, prefix="/api/v1")  # NEW
app.include_router(teams.router, prefix="/api/v1")  # 