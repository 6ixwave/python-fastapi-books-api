from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.db import Base, get_db
from app.main import app


TEST_DB = Path(__file__).with_name("test.db")
engine = create_engine(f"sqlite:///{TEST_DB}", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(engine)


def override_db():
    with TestingSession() as session:
        yield session


app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_complete_crud_flow():
    category = client.post("/categories", json={"title": "Databases"})
    assert category.status_code == 201
    category_id = category.json()["id"]

    book_payload = {
        "title": "PostgreSQL in Practice",
        "description": "A practical database handbook",
        "price": "1490.00",
        "url": "https://example.com/postgresql",
        "category_id": category_id,
    }
    book = client.post("/books", json=book_payload)
    assert book.status_code == 201
    book_id = book.json()["id"]

    assert client.get(f"/books?category_id={category_id}").json()[0]["id"] == book_id
    book_payload["title"] = "PostgreSQL: Field Notes"
    assert client.put(f"/books/{book_id}", json=book_payload).status_code == 200
    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.delete(f"/categories/{category_id}").status_code == 204


def test_validation_and_missing_resources():
    assert client.get("/books/999").status_code == 404
    response = client.post(
        "/books",
        json={
            "title": "Unknown category",
            "description": "This category is absent",
            "price": "10.00",
            "url": "https://example.com/book",
            "category_id": 999,
        },
    )
    assert response.status_code == 422
