from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.db.db import get_db


router = APIRouter(prefix="/books", tags=["Books"])


def require_book(db: Session, book_id: int):
    book = crud.find_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def ensure_category_exists(db: Session, category_id: int) -> None:
    if crud.find_category(db, category_id) is None:
        raise HTTPException(status_code=422, detail="Category does not exist")


@router.get("", response_model=list[schemas.BookRead], summary="List and filter books")
def get_books(
    category_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    return crud.list_books(db, category_id)


@router.get("/{book_id}", response_model=schemas.BookRead, summary="Get a book")
def get_book(book_id: int, db: Session = Depends(get_db)):
    return require_book(db, book_id)


@router.post(
    "",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book",
)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    ensure_category_exists(db, payload.category_id)
    return crud.add_book(db, payload)


@router.put("/{book_id}", response_model=schemas.BookRead, summary="Update a book")
def update_book(
    book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)
):
    book = require_book(db, book_id)
    ensure_category_exists(db, payload.category_id)
    return crud.edit_book(db, book, payload)


@router.delete(
    "/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book"
)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Response:
    book = require_book(db, book_id)
    crud.remove_book(db, book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
