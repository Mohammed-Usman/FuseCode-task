from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/",
        json={"title": "Dune", "author": "Frank Herbert", "published_year": 1965},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Dune"


def test_list_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_book():
    response = client.post(
        "/books/", json={"title": "Test", "author": "Author", "published_year": 2000}
    )
    book_id = response.json()["id"]
    response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated", "author": "New Author", "published_year": 2001},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_book():
    response = client.post(
        "/books/",
        json={"title": "To Delete", "author": "Someone", "published_year": 1999},
    )
    book_id = response.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204
