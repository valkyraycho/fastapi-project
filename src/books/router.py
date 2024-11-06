import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status

from src.auth.dependencies.token import AccessTokenDep
from src.auth.dependencies.user import admin_user_role_checker
from src.database import SessionDep

from .models import Book
from .schemas import BookCreate, BookPublicWithUserAndReviews, BookUpdate
from .service import BookServiceDep

router = APIRouter()


@router.get(
    "",
    response_model=Sequence[BookPublicWithUserAndReviews],
    dependencies=[admin_user_role_checker],
)
async def get_books(
    session: SessionDep, access_token: AccessTokenDep, service: BookServiceDep
) -> Sequence[Book]:
    return await service.get_books(session)


@router.get(
    "/{book_id}",
    response_model=BookPublicWithUserAndReviews,
    dependencies=[admin_user_role_checker],
)
async def get_book(
    book_id: uuid.UUID,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: BookServiceDep,
) -> Book:
    return await service.get_book(book_id, session)


@router.get(
    "/users/{user_id}",
    response_model=Sequence[BookPublicWithUserAndReviews],
    dependencies=[admin_user_role_checker],
)
async def get_user_books(
    user_id: uuid.UUID,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: BookServiceDep,
) -> Sequence[Book]:
    return await service.get_user_books(user_id, session)


@router.post(
    "",
    response_model=BookPublicWithUserAndReviews,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_user_role_checker],
)
async def create_book(
    book: BookCreate,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: BookServiceDep,
) -> Book:
    return await service.create_book(
        book, session, user_id=uuid.UUID(access_token.user["user_id"])
    )


@router.patch(
    "/{book_id}",
    response_model=BookPublicWithUserAndReviews,
    dependencies=[admin_user_role_checker],
)
async def update_book(
    book_id: uuid.UUID,
    book: BookUpdate,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: BookServiceDep,
) -> Book:
    return await service.update_book(book_id, book, session)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_user_role_checker],
)
async def delete_book(
    book_id: uuid.UUID,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: BookServiceDep,
) -> None:
    await service.delete_book(book_id, session)
