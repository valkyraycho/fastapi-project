import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .auth.tests import AUTH_ENDPOINT_PREFIX, MOCK_USER_EMAIL, MOCK_USER_PASSWORD
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


@pytest_asyncio.fixture(autouse=True, scope="session")
async def test_db() -> AsyncGenerator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=False)
async def test_async_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def test_sync_client() -> TestClient:
    return TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def mock_logged_in_user(
    test_async_client: AsyncClient,
) -> dict[str, str | dict[str, str]]:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/login",
        json={"email": MOCK_USER_EMAIL, "password": MOCK_USER_PASSWORD},
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user_data" in data
    assert "email" in data["user_data"]
    assert "user_id" in data["user_data"]
    assert "role" in data["user_data"]
    return data
