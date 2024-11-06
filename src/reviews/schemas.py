from pydantic import BaseModel

from src.schemas import Identifier


class ReviewBase(BaseModel):
    content: str
    rating: int


class ReviewCreate(ReviewBase): ...


class ReviewUpdate(ReviewBase): ...


class ReviewPublic(ReviewBase, Identifier): ...


class ReviewPublicWithUserAndBook(ReviewPublic):
    user: "UserPublic"
    book: "BookPublic"


from src.auth.schemas import UserPublic  # noqa: E402
from src.books.schemas import BookPublic  # noqa: E402

ReviewPublic.model_rebuild()
