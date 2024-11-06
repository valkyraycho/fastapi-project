import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status

from src.auth.dependencies.token import AccessTokenDep
from src.auth.dependencies.user import admin_user_role_checker
from src.database import SessionDep

from .models import Review
from .schemas import (
    ReviewCreate,
    ReviewPublicWithUserAndBook,
    ReviewUpdate,
)
from .service import ReviewServiceDep

router = APIRouter()


@router.get(
    "",
    response_model=Sequence[ReviewPublicWithUserAndBook],
    dependencies=[admin_user_role_checker],
)
async def get_reviews(
    session: SessionDep,
    access_token: AccessTokenDep,
    service: ReviewServiceDep,
) -> Sequence[Review]:
    return await service.get_reviews(session)


@router.get(
    "/{review_id}",
    response_model=ReviewPublicWithUserAndBook,
    dependencies=[admin_user_role_checker],
)
async def get_review(
    review_id: uuid.UUID,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: ReviewServiceDep,
) -> Review:
    return await service.get_review(review_id, session)


@router.post(
    "/books/{book_id}",
    response_model=ReviewPublicWithUserAndBook,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_user_role_checker],
)
async def create_review(
    book_id: uuid.UUID,
    review: ReviewCreate,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: ReviewServiceDep,
) -> Review:
    return await service.create_review(
        uuid.UUID(access_token.user["user_id"]), book_id, review, session
    )


@router.patch(
    "/{review_id}",
    response_model=ReviewPublicWithUserAndBook,
    dependencies=[admin_user_role_checker],
)
async def update_review(
    review_id: uuid.UUID,
    review: ReviewUpdate,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: ReviewServiceDep,
) -> Review:
    return await service.update_review(review_id, review, session)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_user_role_checker],
)
async def delete_review(
    review_id: uuid.UUID,
    session: SessionDep,
    access_token: AccessTokenDep,
    service: ReviewServiceDep,
) -> None:
    return await service.delete_review(review_id, session)
