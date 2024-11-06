import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from .schemas import UserCreate
from .utils import create_url_safe_token

AUTH_ENDPOINT_PREFIX = "/api/v1/auth"

MOCK_USER_EMAIL = "johndoe@gmail.com"
MOCK_USER_PASSWORD = "johndoe123"
MOCK_USERNAME = "johndoe123"
MOCK_FIRST_NAME = "John"
MOCK_LAST_NAME = "Doe"


@pytest.mark.asyncio
async def test_create_user(
    test_async_client: AsyncClient, mocker: MockerFixture
) -> None:
    mock_send_email = mocker.patch("src.celery.send_email.apply_async", autospec=True)
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/signup",
        json=UserCreate(
            email=MOCK_USER_EMAIL,
            password=MOCK_USER_PASSWORD,
            username=MOCK_USERNAME,
            first_name=MOCK_FIRST_NAME,
            last_name=MOCK_LAST_NAME,
        ).model_dump(),
    )

    assert response.status_code == 201
    mock_send_email.assert_called_once()


@pytest.mark.asyncio
async def test_verify_user_account(test_async_client: AsyncClient) -> None:
    response = await test_async_client.get(
        f"{AUTH_ENDPOINT_PREFIX}/verify/{create_url_safe_token({"email": MOCK_USER_EMAIL})}"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Account verified successfully."}


@pytest.mark.asyncio
async def test_login_failed_with_nonexisting_email(
    test_async_client: AsyncClient,
) -> None:
    nonexisting_email = "nonexisting@gmail.com"
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/login",
        json={"email": nonexisting_email, "password": MOCK_USER_PASSWORD},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"User with email {nonexisting_email} does not exists."
    }


@pytest.mark.asyncio
async def test_login_failed_with_wrong_password(
    test_async_client: AsyncClient,
) -> None:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/login",
        json={"email": MOCK_USER_EMAIL, "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


@pytest.mark.asyncio
async def test_get_current_user(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> None:
    response = await test_async_client.get(
        f"{AUTH_ENDPOINT_PREFIX}/me",
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "password" not in data
    assert data["username"] == MOCK_USERNAME
    assert data["email"] == MOCK_USER_EMAIL
    assert data["first_name"] == MOCK_FIRST_NAME
    assert data["last_name"] == MOCK_LAST_NAME


@pytest.mark.asyncio
async def test_refresh_access_token(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> None:
    response = await test_async_client.get(
        f"{AUTH_ENDPOINT_PREFIX}/refresh",
        headers={"Authorization": f"Bearer {mock_logged_in_user["refresh_token"]}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_refresh_access_token_providing_access_token(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> None:
    response = await test_async_client.get(
        f"{AUTH_ENDPOINT_PREFIX}/refresh",
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access token provided."}


@pytest.mark.asyncio
async def test_reset_password_request(test_async_client: AsyncClient) -> None:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/reset-password-request",
        json={"email": MOCK_USER_EMAIL},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password(test_async_client: AsyncClient) -> None:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/password-reset/{create_url_safe_token({"email": MOCK_USER_EMAIL})}",
        json={
            "new_password": "NewPassword123",
            "new_password_confirm": "NewPassword123",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset successfully."}


@pytest.mark.asyncio
async def test_reset_password_with_passwords_unmatch(
    test_async_client: AsyncClient,
) -> None:
    response = await test_async_client.post(
        f"{AUTH_ENDPOINT_PREFIX}/password-reset/{create_url_safe_token({"email": MOCK_USER_EMAIL})}",
        json={
            "new_password": "NewPassword123",
            "new_password_confirm": "NewPassword",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords do not match."}
