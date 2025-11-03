"""SQLAlchemy ORM models for the FastAPI application."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarative class for ORM models."""


class Game(Base):
    """Database representation of a lottery game."""

    __tablename__ = "games"

    code: Mapped[str] = mapped_column(String, primary_key=True)
    display_name: Mapped[str] = mapped_column(String)
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
