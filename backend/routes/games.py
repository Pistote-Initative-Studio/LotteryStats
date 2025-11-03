"""API routes related to lottery games."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models import Game

router = APIRouter()


class GameSchema(BaseModel):
    """Pydantic schema used to serialize game records."""

    code: str
    display_name: str
    config: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


@router.get("/games", response_model=List[GameSchema])
async def list_games(session: AsyncSession = Depends(get_session)) -> List[GameSchema]:
    """Return all games ordered by their code."""

    result = await session.execute(select(Game).order_by(Game.code))
    games = result.scalars().all()
    return games
