"""Entry point for the FastAPI application."""
from __future__ import annotations

from fastapi import FastAPI

from backend.db import connect_to_db, disconnect_from_db
from backend.routes.games import router as games_router

app = FastAPI(title="Lottery Stats API")


@app.on_event("startup")
async def on_startup() -> None:
    """Event handler executed when the application starts."""
    await connect_to_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Event handler executed when the application stops."""
    await disconnect_from_db()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple status response to verify service availability."""
    return {"status": "ok"}


app.include_router(games_router)
