# app/main.py
from fastapi import FastAPI
from app.api.routers import health  # import the router module

app = FastAPI(
    title="UPA Pool League API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Mount versioned API routes
app.include_router(health.router, prefix="/api/v1")
