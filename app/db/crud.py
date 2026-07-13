from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import schemas
from app.db.models import Book, Category


def list_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.id)))


def find_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def find_category_by_title(db: Session, title: str) -> Category | None:
    statement = select(Category).where(func.lower(Category.title) == title.lower())
    return db.scalar(statement)


def add_category(db: Session, payload: schemas.CategoryCreate) -> Category:
    category = Category(title=payload.title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def edit_category(
    db: Session, category: Category, payload: schemas.CategoryUpdate
) -> Category:
    category.title = payload.title
    db.commit()
    db.refresh(category)
    return category


def category_has_books(db: Session, category_id: int) -> bool:
    statement = select(Book.id).where(Book.category_id == category_id).limit(1)
    return db.scalar(statement) is not None


def remove_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()


def list_books(db: Session, category_id: int | None = None) -> list[Book]:
    statement = select(Book).order_by(Book.id)
    if category_id is not None:
        statement = statement.where(Book.category_id == category_id)
    return list(db.scalars(statement))


def find_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def add_book(db: Session, payload: schemas.BookCreate) -> Book:
    values = payload.model_dump(mode="json")
    book = Book(**values)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def edit_book(db: Session, book: Book, payload: schemas.BookUpdate) -> Book:
    for name, value in payload.model_dump(mode="json").items():
        setattr(book, name, value)
    db.commit()
    db.refresh(book)
    return book


def remove_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
