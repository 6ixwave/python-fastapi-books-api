from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import BookCreate, BookRead, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
def list_books(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, category_id=category_id)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    category = crud.get_category(db, book_data.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail="Category does not exist")

    return crud.create_book(db, **book_data.model_dump())


@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    category = crud.get_category(db, book_data.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail="Category does not exist")

    book = crud.update_book(db, book_id, **book_data.model_dump())
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
