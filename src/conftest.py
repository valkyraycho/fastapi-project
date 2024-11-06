from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import Config
from .database import get_session
from .main import app

async_engine = create_async_engine(url=Config.DATABASE_TEST_URL)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
def test_client() -> TestClient:
    app.dependency_overrides[get_session] = get_test_session
    return TestClient(app)
