from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_add_item():
    response = client.post("/items/test_item/10")
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "test_item", "quantity": 10}}


def test_list_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item": {"id": 1, "name": "test_item", "quantity": 10}}