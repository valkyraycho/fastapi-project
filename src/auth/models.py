import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy.dialects.postgresql as pg
from pydantic import EmailStr
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.books.models import Book
    from src.reviews.models import Review


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[reportAssignmentType]
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: list["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: list["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"User(username={self.username})"
