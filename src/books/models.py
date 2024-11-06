import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.auth.models import User
    from src.reviews.models import Review


class Book(SQLModel, table=True):
    __tablename__ = "books"  # type: ignore[reportAssignmentType]

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: date
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    user: "User" = Relationship(back_populates="books")  # type: ignore  # noqa: F821
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    reviews: list["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"Book(title={self.title})"
