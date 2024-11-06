from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

from ..redis import token_in_blocklist
from ..utils import decode_token


@dataclass
class Token:
    user: dict[str, str]
    exp: int
    jti: str
    refresh: bool


class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Token:
        credentials = await super().__call__(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credentials not provided",
            )

        token = Token(**decode_token(credentials.credentials))
        self.verify_token(token)
        if await token_in_blocklist(token.jti):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token is revoked."
            )
        return token

    def verify_token(self, token: Token) -> None:
        raise NotImplementedError()


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token: Token) -> None:
        if token.refresh:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token provided.",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token: Token) -> None:
        if not token.refresh:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token provided.",
            )


AccessTokenDep = Annotated[Token, Depends(AccessTokenBearer())]
RefreshTokenDep = Annotated[Token, Depends(RefreshTokenBearer())]
