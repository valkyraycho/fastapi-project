from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash


class AuthService:
    async def get_user(self, email: EmailStr, session: AsyncSession) -> User:
        result = await session.exec(select(User).where(User.email == email))
        if (result := result.first()) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} does not exists.",
            )
        return result

    async def user_exists(self, email: EmailStr, session: AsyncSession) -> bool:
        result = await session.exec(select(User).where(User.email == email))
        return result.first() is not None

    async def create_user(self, user: UserCreate, session: AsyncSession) -> User:
        user_create = User(**user.model_dump())
        user_create.password = generate_password_hash(user_create.password)
        user_create.role = "user"
        user_create.books = []
        user_create.reviews = []
        session.add(user_create)
        await session.commit()
        return user_create

    async def update_user(
        self, email: str, user_data: dict[str, Any], session: AsyncSession
    ) -> User:
        user_update = await self.get_user(email, session)
        for k, v in user_data.items():
            setattr(user_update, k, v)
        await session.commit()
        return user_update


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
