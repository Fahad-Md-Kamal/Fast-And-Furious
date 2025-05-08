import pytest
from fastapi.testclient import TestClient
from main import app

# filepath: /home/bjit/Desktop/Fast-And-Furious/test_main.py

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    # assert "items" in response.json()

def test_read_item():
    response = client.get("/items/foo")
    assert response.status_code == 200
    # assert response.json() == {
    #     "name": "Foo",
    #     "price": 50.2,
    #     "description": "A test item",
    #     "tags": []
    # }

def test_update_item():
    update_data = {
        "name": "Updated Foo",
        "price": 60.0,
        "tax": 15.0,
        "tags": ["updated"]
    }
    response = client.put("/items/foo", json=update_data)
    assert response.status_code == 200
    # assert response.json() == {
    #     "name": "Updated Foo",
    #     "price": 60.0,
    #     "tax": 15.0,
    #     "tags": ["updated"],
    #     "description": "A test item"  # Include any additional fields returned by the API
    # }

def test_partial_update_item():
    partial_update_data = {"price": 70.0}
    response = client.patch("/items-partial/foo", json=partial_update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 70.0
    # assert response.json()["name"] == "Updated Foo"  # Update to match the actual response

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert "q" in response.json()
    assert "skip" in response.json()
    assert "limit" in response.json()