from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from .auth.router import router as auth_router
from .books.router import router as book_router
from .database import init_db
from .middlewares import register_middlewares
from .reviews.router import router as review_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    print("server starting...")
    await init_db()
    yield
    print("server stopped")


version = "v1"
app = FastAPI(
    version=version, description="RESTful API for a book review web service."
)  # lifespan=lifespan
register_middlewares(app)
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}
