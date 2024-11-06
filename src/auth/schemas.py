from pydantic import BaseModel, EmailStr, Field

from src.schemas import Identifier


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    username: str
    first_name: str
    last_name: str


class UserLogin(UserBase): ...


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_data: dict[str, str]


class UserPublic(UserCreate, Identifier):
    role: str
    is_verified: bool = False


class UserPublicWithBooksAndReviews(UserPublic):
    password: str = Field(exclude=True)
    books: list["BookPublic"] = []
    reviews: list["ReviewPublic"] = []


from src.books.schemas import BookPublic  # noqa: E402
from src.reviews.schemas import ReviewPublic  # noqa: E402

UserPublicWithBooksAndReviews.model_rebuild()


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    new_password: str
    new_password_confirm: str
