import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200, "Health check failed"
    assert response.json() == {"status": "ok"}, "Unexpected health check response"

def test_create_item() -> None:
    response = client.post("/items", json={"name": "Apple", "price": 3.5})
    assert response.status_code == 200, "Failed to create item"
    created_item = response.json()
    assert created_item["name"] == "Apple", "Item name does not match"
    assert created_item["price"] == 3.5, "Item price does not match"

    dup_response = client.post("/items", json={"name": "Apple", "price": 3.5})
    assert dup_response.status_code == 400, "Duplicate item name should not be accepted"


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json()), "Items returned do not respect the min_price filter"


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422, "Short item name should not be accepted"


def test_negative_price() -> None:
    response = client.post("/items", json={"name": "abc", "price": -1})
    assert response.status_code == 422, "Negative item price should not be accepted"


def test_update_item() -> None:
    response = client.post("/items", json={"name": "abcd", "price": 5})
    assert response.status_code == 200, "Failed to create item for update test"
    item_id = response.json()["id"]

    updated_name, updated_price = "UpdatedItem", 10.0
    update_response = client.put(f"/items/{item_id}", json={"name": updated_name, "price": updated_price})
    assert update_response.status_code == 200, "Failed to update item for update test"

    fetch_response = client.get(f"/items?min_price={updated_price}")
    result_items = fetch_response.json()

    updated_item = next((item for item in result_items if item["id"] == item_id), None)
    assert updated_item is not None, "Updated item not found"
    assert updated_item["name"] == updated_name, "Item name was not updated correctly"
    assert updated_item["price"] == updated_price, "Item price was not updated correctly"


def test_check_item_correct_place_after_update() -> None:
    name, before_price, after_price = "abcde", 10.0, 15.0
    response = client.post("/items", json={"name": name, "price": before_price})
    assert response.status_code == 200, "Failed to create item"
    item_id = response.json()["id"]

    update_response = client.put(f"/items/{item_id}", json={"price": after_price})
    assert update_response.status_code == 200, "Failed to update item"

    response = client.get(f"/items?min_price={before_price}")
    assert response.status_code == 200, "Failed to fetch items after update"
    result_items = response.json()

    first_index_15 = next((i for i, item in enumerate(result_items) if item["price"] == after_price), None)

    assert first_index_15 is not None, "No item found with the specified price"
    assert result_items[first_index_15]["id"] == item_id, "The item ID does not match the expected ID"


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422

def test_update_item_not_found() -> None:
    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items for update test"
    items = response.json()

    response = client.put(f"/items/{len(items) + 1}", json={"name": "NonExistentItem", "price": 10})
    assert response.status_code == 404, "Updating a non-existent item should return 404"


def test_item_name_consistency() -> None:
    name, price = "abcf", 15.0
    create_response = client.post("/items", json={"name": name, "price": price})
    assert create_response.status_code == 200, "Failed to create item for name consistency test"
    created_item = create_response.json()

    assert created_item["name"] == name, "Created item name does not match the expected name"
    assert created_item["price"] == price, "Created item price does not match the expected price"

    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items for name consistency test"
    items_names = [item["name"] for item in response.json()]
    assert created_item["name"] in items_names, "Created item name is not consistent in the list of items"


def test_create_item_max_id() -> None:
    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items after creation"
    before_max_id = max(item["id"] for item in response.json())

    name, price = "abcg", 10.0
    response = client.post("/items", json={"name": name, "price": price})
    assert response.status_code == 200, "Failed to create item"
    created_item = response.json()

    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items after creation"
    after_max_id = max(item["id"] for item in response.json())

    assert created_item["id"] == after_max_id, "Created item ID does not match the expected ID"
    assert after_max_id == before_max_id + 1, "Item ID was not incremented correctly after creation"


def test_sorted_insertion_with_binary_search() -> None:
    name, high_price, low_price = "abcz", 45.0, 40.0

    post_response = client.post("/items", json={"name": name, "price": high_price})
    posted_item = post_response.json()
    assert post_response.status_code == 200, "Failed to create item"

    response = client.get(f"/items?min_price={low_price}")
    assert response.status_code == 200, "Failed to fetch items with min_price filter"
    result_items = response.json()

    first_index_45 = next((i for i, item in enumerate(result_items) if item["price"] == high_price), None)

    assert first_index_45 is not None, "No item found with the specified price"
    assert result_items[first_index_45]["id"] == posted_item["id"], "The item ID does not match the expected ID"
