import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.auth.models import User
    from src.books.models import Book


class Review(SQLModel, table=True):
    __tablename__ = "reviews"  # type: ignore[reportAssignmentType]
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    book_id: uuid.UUID | None = Field(default=None, foreign_key="books.id")
    content: str
    rating: int = Field(le=5)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: "User" = Relationship(back_populates="reviews")
    book: "Book" = Relationship(back_populates="reviews")
