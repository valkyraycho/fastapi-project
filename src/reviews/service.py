import uuid
from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Review
from .schemas import ReviewCreate, ReviewUpdate


class ReviewService:
    async def get_reviews(self, session: AsyncSession) -> Sequence[Review]:
        result = await session.exec(select(Review).order_by(desc(Review.created_at)))
        return result.all()

    async def get_review(self, review_id: uuid.UUID, session: AsyncSession) -> Review:
        result = await session.exec(select(Review).where(Review.id == review_id))
        if (result := result.first()) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    async def create_review(
        self,
        user_id: uuid.UUID,
        book_id: uuid.UUID,
        review: ReviewCreate,
        session: AsyncSession,
    ) -> Review:
        review_create = Review(**review.model_dump(), user_id=user_id, book_id=book_id)
        session.add(review_create)
        await session.commit()
        return review_create

    async def update_review(
        self, review_id: uuid.UUID, review: ReviewUpdate, session: AsyncSession
    ) -> Review:
        review_update = await self.get_review(review_id, session)
        for k, v in review.model_dump().items():
            setattr(review_update, k, v)
        await session.commit()
        return review_update

    async def delete_review(self, review_id: uuid.UUID, session: AsyncSession) -> None:
        review_delete = await self.get_review(review_id, session)
        await session.delete(review_delete)
        await session.commit()


ReviewServiceDep = Annotated[ReviewService, Depends(ReviewService)]
