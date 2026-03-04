from pathlib import Path
import sys

from fastapi.testclient import TestClient

# Ensure top-level modules (like main.py) are importable during test collection.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import app, get_token


client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_get_item_success() -> None:
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Book"}


def test_get_item_not_found() -> None:
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_add_item() -> None:
    response = client.post("/items")
    assert response.status_code == 201
    assert response.json() == {"ok": True}


def test_ping() -> None:
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_secure_success() -> None:
    response = client.get("/secure")
    assert response.status_code == 200
    assert response.json() == {"secure_data": "This is secure"}


def test_secure_forbidden_with_override() -> None:
    app.dependency_overrides[get_token] = lambda: "wrong-token"
    try:
        response = client.get("/secure")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_list_items_router_endpoint() -> None:
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"items": ["item1", "item2", "item3"]}
