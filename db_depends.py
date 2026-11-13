from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker
from contextlib import asynccontextmanager
from database import Base, async_engine
from models import Fighter

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(
                Base.metadata.create_all,
                tables=[Fighter.__table__],
            )
        yield
    finally:
        await async_engine.dispose()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию SQLAlchemy для работы с базой данных PostgreSQL.
    """
    async with async_session_maker() as session:
        yield session
