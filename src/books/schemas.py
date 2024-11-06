from datetime import date

from pydantic import BaseModel

from src.schemas import Identifier


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: date


class BookUpdate(BookBase): ...


class BookCreate(BookBase): ...


class BookPublic(BookBase, Identifier): ...


class BookPublicWithUserAndReviews(BookPublic):
    user: "UserPublic"
    reviews: list["ReviewPublic"] = []


from src.auth.schemas import UserPublic  # noqa: E402
from src.reviews.schemas import ReviewPublic  # noqa: E402

BookPublicWithUserAndReviews.model_rebuild()
