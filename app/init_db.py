import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.crud import create_book, create_category, get_category_by_title
from app.db.db import Base, SessionLocal, engine
from app.db.models import Book, Category


def recreate_tables():
    with engine.begin() as connection:
        connection.exec_driver_sql("DROP TABLE IF EXISTS books CASCADE")
        connection.exec_driver_sql("DROP TABLE IF EXISTS categories CASCADE")

    Base.metadata.create_all(bind=engine)


def seed_data():
    with SessionLocal() as session:
        programming = get_category_by_title(session, "Программирование")
        if programming is None:
            programming = create_category(session, "Программирование")

        databases = get_category_by_title(session, "Базы данных")
        if databases is None:
            databases = create_category(session, "Базы данных")

        create_book(
            session,
            title="Python для начинающих",
            description="Практическое введение в Python.",
            price=1200,
            category_id=programming.id,
        )
        create_book(
            session,
            title="Чистый Python",
            description="Книга о стиле и структуре Python-кода.",
            price=1500,
            category_id=programming.id,
        )
        create_book(
            session,
            title="SQL на практике",
            description="Основы SQL-запросов и проектирования таблиц.",
            price=1000,
            category_id=databases.id,
        )
        create_book(
            session,
            title="PostgreSQL для разработчика",
            description="Работа с PostgreSQL из приложений.",
            price=1800,
            category_id=databases.id,
        )


def main():
    recreate_tables()
    seed_data()
    print("База данных и тестовые данные созданы.")


if __name__ == "__main__":
    main()
