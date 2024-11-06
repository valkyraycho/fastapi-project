import uuid

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

BOOK_ENDPOINT_PREFIX = "/api/v1/books"

BOOK_ID = uuid.uuid4()
USER_ID = uuid.uuid4()
BOOK_TITLE = "Test Book"
BOOK_AUTHOR = "John Doe"
BOOK_PUBLISHER = "John Doe"
BOOK_PAGE_COUNT = 1000
BOOK_LANGUAGE = "English"
BOOK_PUBLISHED_DATE = "2021-01-01"


@pytest_asyncio.fixture
async def book_id(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> str:
    response = await test_async_client.get(
        BOOK_ENDPOINT_PREFIX,
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    return response.json()[0]["id"]


@pytest.mark.asyncio
async def test_create_book(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> None:
    book_data = {
        "title": BOOK_TITLE,
        "author": BOOK_AUTHOR,
        "publisher": BOOK_PUBLISHER,
        "published_date": BOOK_PUBLISHED_DATE,
        "page_count": BOOK_PAGE_COUNT,
        "language": BOOK_LANGUAGE,
    }
    response = await test_async_client.post(
        BOOK_ENDPOINT_PREFIX,
        json=book_data,
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    book = response.json()
    assert book["title"] == book_data["title"]
    assert book["author"] == book_data["author"]
    assert book["publisher"] == book_data["publisher"]
    assert book["published_date"] == book_data["published_date"]
    assert book["language"] == book_data["language"]
    assert book["page_count"] == book_data["page_count"]


@pytest.mark.asyncio
async def test_get_books(
    test_async_client: AsyncClient, mock_logged_in_user: dict[str, str | dict[str, str]]
) -> None:
    response = await test_async_client.get(
        BOOK_ENDPOINT_PREFIX,
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_200_OK
    books = response.json()
    assert isinstance(books, list)


@pytest.mark.asyncio
async def test_get_book(
    test_async_client: AsyncClient,
    mock_logged_in_user: dict[str, str | dict[str, str]],
    book_id: str,
) -> None:
    response = await test_async_client.get(
        f"{BOOK_ENDPOINT_PREFIX}/{book_id}",
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_200_OK
    book = response.json()
    assert book["id"] == book_id


@pytest.mark.asyncio
async def test_get_user_books(
    test_async_client: AsyncClient,
    mock_logged_in_user: dict[str, str | dict[str, str]],
) -> None:
    response = await test_async_client.get(
        f"{BOOK_ENDPOINT_PREFIX}/users/{mock_logged_in_user["user_data"]["user_id"]}",  # type: ignore[ReportArgumentType]
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_200_OK
    books = response.json()
    assert isinstance(books, list)


@pytest.mark.asyncio
async def test_update_book(
    test_async_client: AsyncClient,
    mock_logged_in_user: dict[str, str | dict[str, str]],
    book_id: str,
) -> None:
    update_data = {
        "title": "Updated Book Title",
        "author": "Updated Author",
        "publisher": BOOK_PUBLISHER,
        "published_date": BOOK_PUBLISHED_DATE,
        "page_count": BOOK_PAGE_COUNT,
        "language": BOOK_LANGUAGE,
    }
    response = await test_async_client.patch(
        f"{BOOK_ENDPOINT_PREFIX}/{book_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_200_OK
    updated_book = response.json()
    assert updated_book["title"] == update_data["title"]
    assert updated_book["author"] == update_data["author"]


@pytest.mark.asyncio
async def test_delete_book(
    test_async_client: AsyncClient,
    mock_logged_in_user: dict[str, str | dict[str, str]],
    book_id: str,
) -> None:
    response = await test_async_client.delete(
        f"{BOOK_ENDPOINT_PREFIX}/{book_id}",
        headers={"Authorization": f"Bearer {mock_logged_in_user["access_token"]}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
