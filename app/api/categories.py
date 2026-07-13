from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.db.db import get_db


router = APIRouter(prefix="/categories", tags=["Categories"])


def require_category(db: Session, category_id: int):
    category = crud.find_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("", response_model=list[schemas.CategoryRead], summary="List categories")
def get_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.get(
    "/{category_id}", response_model=schemas.CategoryRead, summary="Get a category"
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return require_category(db, category_id)


@router.post(
    "",
    response_model=schemas.CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a category",
)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    if crud.find_category_by_title(db, payload.title):
        raise HTTPException(status_code=409, detail="Category title already exists")
    return crud.add_category(db, payload)


@router.put(
    "/{category_id}", response_model=schemas.CategoryRead, summary="Update a category"
)
def update_category(
    category_id: int,
    payload: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = require_category(db, category_id)
    duplicate = crud.find_category_by_title(db, payload.title)
    if duplicate and duplicate.id != category_id:
        raise HTTPException(status_code=409, detail="Category title already exists")
    return crud.edit_category(db, category, payload)


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a category"
)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> Response:
    category = require_category(db, category_id)
    if crud.category_has_books(db, category_id):
        raise HTTPException(
            status_code=409, detail="Delete books from this category first"
        )
    crud.remove_category(db, category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
