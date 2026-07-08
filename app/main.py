from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import books, categories
from app.db.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Books API", version="1.0.0", lifespan=lifespan)

app.include_router(categories.router)
app.include_router(books.router)


@app.get("/health")
def health():
    return {"status": "ok"}
