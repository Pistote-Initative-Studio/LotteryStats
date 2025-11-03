"""Database configuration and session management for the FastAPI application."""
from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession, async_sessionmaker,
                                    create_async_engine)

RAW_DATABASE_URL = os.getenv("DATABASE_URL")

if not RAW_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")


def _as_asyncpg_dsn(dsn: str) -> str:
    """Ensure the DSN uses the asyncpg driver."""

    if "+asyncpg" in dsn:
        return dsn

    if dsn.startswith("postgres://"):
        return dsn.replace("postgres://", "postgresql+asyncpg://", 1)

    if dsn.startswith("postgresql://"):
        return dsn.replace("postgresql://", "postgresql+asyncpg://", 1)

    return dsn


DATABASE_URL = _as_asyncpg_dsn(RAW_DATABASE_URL)

# Create the async SQLAlchemy engine and session factory.
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def connect_to_db() -> None:
    """Validate the database connection at application startup."""
    async with engine.begin() as connection:
        await connection.execute(text("SELECT 1"))


async def disconnect_from_db() -> None:
    """Dispose of the engine when the application shuts down."""
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for FastAPI dependencies."""
    async with AsyncSessionLocal() as session:
        yield session
