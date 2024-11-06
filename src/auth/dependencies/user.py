from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.database import SessionDep

from ..models import User
from ..service import AuthServiceDep
from .token import AccessTokenDep


async def get_current_user(
    token: AccessTokenDep, session: SessionDep, service: AuthServiceDep
) -> User:
    return await service.get_user(token.user.get("email", ""), session)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUserDep) -> None:
        if not user.is_verified:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, detail="Account not verified."
            )
        if UserRole(user.role) not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed."
            )


admin_user_role_checker = Depends(RoleChecker([UserRole.ADMIN, UserRole.USER]))
