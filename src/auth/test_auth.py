import pytest
from httpx import AsyncClient

AUTH_ENDPOINT_PREFIX = "/api/v1/auth"

MOCK_USER_EMAIL = "johndoe@gmail.com"
MOCK_USER_PASSWORD = "johndoe123"
MOCK_USERNAME = "johndoe123"
MOCK_FIRST_NAME = "John"
MOCK_LAST_NAME = "Doe"


@pytest.mark.anyio
async def test_create_user(test_async_client: AsyncClient) -> None:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/signup",
        json={
            "email": MOCK_USER_EMAIL,
            "password": MOCK_USER_PASSWORD,
            "username": MOCK_USERNAME,
            "first_name": MOCK_FIRST_NAME,
            "last_name": MOCK_LAST_NAME,
        },
    )
    assert response.status_code == 201
