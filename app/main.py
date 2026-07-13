from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import schemas
from app.api import books, categories
from app.db import models  # noqa: F401 - registers ORM metadata
from app.db.db import create_tables, get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Personal Bookshelf API",
    description="CRUD service for a categorized personal book collection.",
    version="2.0.0",
    lifespan=lifespan,
)
app.include_router(categories.router)
app.include_router(books.router)


@app.get(
    "/health",
    response_model=schemas.HealthRead,
    tags=["Service"],
    summary="Check API and database",
)
def health(db: Session = Depends(get_db)) -> schemas.HealthRead:
    db.execute(text("SELECT 1"))
    return schemas.HealthRead()
