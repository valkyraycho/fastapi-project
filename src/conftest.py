from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
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
        yield session


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
async def test_db() -> AsyncGenerator[None]:
    async def init_db() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_db() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    await init_db()
    yield
    await drop_db()


@pytest.fixture
async def test_async_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def test_sync_client() -> TestClient:
    return TestClient(app)
