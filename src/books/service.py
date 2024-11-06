import uuid
from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Book
from .schemas import BookCreate, BookUpdate


class BookService:
    async def get_books(self, session: AsyncSession) -> Sequence[Book]:
        result = await session.exec(select(Book).order_by(desc(Book.created_at)))
        return result.all()

    async def get_book(self, pk: uuid.UUID, session: AsyncSession) -> Book:
        result = await session.exec(select(Book).where(Book.id == pk))
        if (result := result.first()) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    async def get_user_books(
        self, user_id: uuid.UUID, session: AsyncSession
    ) -> Sequence[Book]:
        result = await session.exec(
            select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        )
        return result.all()

    async def create_book(
        self, book: BookCreate, session: AsyncSession, user_id: uuid.UUID
    ) -> Book:
        book_create = Book(**book.model_dump(), user_id=user_id)
        session.add(book_create)
        await session.commit()
        await session.refresh(book_create, ["reviews"])
        return book_create

    async def update_book(
        self, book_id: uuid.UUID, book: BookUpdate, session: AsyncSession
    ) -> Book:
        book_update = await self.get_book(book_id, session)
        for k, v in book.model_dump().items():
            setattr(book_update, k, v)
        await session.commit()
        return book_update

    async def delete_book(self, book_id: uuid.UUID, session: AsyncSession) -> None:
        book_delete = await self.get_book(book_id, session)
        await session.delete(book_delete)
        await session.commit()


BookServiceDep = Annotated[BookService, Depends(BookService)]
