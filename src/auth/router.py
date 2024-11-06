from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.auth.utils import create_url_safe_token
from src.celery import send_email
from src.config import Config
from src.database import SessionDep

from .dependencies.token import AccessTokenDep, RefreshTokenDep
from .dependencies.user import CurrentUserDep
from .models import User
from .redis import add_jti_to_blocklist
from .schemas import (
    PasswordReset,
    PasswordResetRequest,
    UserCreate,
    UserLogin,
    UserPublicWithBooksAndReviews,
)
from .service import AuthServiceDep
from .utils import (
    create_token,
    decode_url_safe_token,
    generate_password_hash,
    verify_password,
)

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicWithBooksAndReviews,
)
async def create_user(
    user: UserCreate, session: SessionDep, service: AuthServiceDep
) -> User:
    if await service.user_exists(user.email, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists.",
        )
    user.password = user.password.replace("\x00", "")
    user_created = await service.create_user(user, session)
    html = f"""
    <h1>Verify your email</h1>
    <p>Please click this <a href="http://{Config.DOMAIN}/api/v1/auth/verify/{create_url_safe_token({"email": user_created.email})}">link</a> to verify your email</p>
    """
    send_email.delay([user_created.email], "Verify your email", html)

    return user_created


@router.get("/verify/{url_safe_token}", status_code=status.HTTP_200_OK)
async def verify_user_account(
    url_safe_token: str, session: SessionDep, service: AuthServiceDep
) -> JSONResponse:
    if not (email := decode_url_safe_token(url_safe_token).get("email")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await service.update_user(email, {"is_verified": True}, session)
    return JSONResponse(content={"message": "Account verified successfully."})


@router.post("/login")
async def login(
    user: UserLogin, session: SessionDep, service: AuthServiceDep
) -> JSONResponse:
    existing_user = await service.get_user(user.email, session)
    verify_password(user.password, existing_user.password)

    user_data = {
        "email": existing_user.email,
        "user_id": str(existing_user.id),
        "role": existing_user.role,
    }
    access_token = create_token(user_data=user_data)
    refresh_token = create_token(user_data=user_data, refresh=True)

    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_data,
        }
    )


@router.get("/me", response_model=UserPublicWithBooksAndReviews)
async def get_current_user(user: CurrentUserDep) -> User:
    return user


@router.get("/refresh")
async def refresh_access_token(
    refresh_token: RefreshTokenDep,
) -> JSONResponse:
    if datetime.fromtimestamp(refresh_token.exp, tz=UTC) > datetime.now(UTC):
        return JSONResponse(content={"access_token": create_token(refresh_token.user)})
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired refresh token."
    )


@router.get("/logout")
async def logout(access_token: AccessTokenDep) -> JSONResponse:
    await add_jti_to_blocklist(access_token.jti)
    return JSONResponse(
        content={"message": "Logout Successfully."}, status_code=status.HTTP_200_OK
    )


@router.post("/reset-password-request", status_code=status.HTTP_200_OK)
async def reset_password_request(request: PasswordResetRequest) -> None:
    html = f"""
    <h1>Verify your password</h1>
    <p>Please click this <a href="http://{Config.DOMAIN}/api/v1/auth/password-reset/{create_url_safe_token({"email": request.email})}">link</a> to reset your password</p>
    """
    send_email.delay([request.email], "Verify your password", html)


@router.post("/password-reset/{url_safe_token}")
async def reset_password(
    url_safe_token: str,
    passwords: PasswordReset,
    session: SessionDep,
    service: AuthServiceDep,
) -> JSONResponse:
    if not passwords.new_password == passwords.new_password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match."
        )
    if not (email := decode_url_safe_token(url_safe_token).get("email")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await service.update_user(
        email, {"password": generate_password_hash(passwords.new_password)}, session
    )
    return JSONResponse(content={"message": "Account verified successfully."})
