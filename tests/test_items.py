from multiprocessing.spawn import prepare

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200, "Health check failed"
    assert response.json() == {"status": "ok"}, "Unexpected health check response"


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
    response = client.post("/items", json={"name": "abc", "price": 5})
    assert response.status_code == 200, "Failed to create item for update test"
    item_id = response.json()["id"]

    name, price = "UpdatedItem", 10.0
    update_response = client.put(f"/items/{item_id}", json={"name": name, "price": price})
    assert update_response.status_code == 200, "Failed to update item for update test"
    updated_item = update_response.json()
    assert updated_item["name"] == name, "Item name was not updated correctly"
    assert updated_item["price"] == price, "Item price was not updated correctly"


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    response = client.get("/items")
    names = [item["name"] for item in response.json()]
    assert "Item500000" in names


def test_create_item_max_id() -> None:
    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items after creation"
    before_max_id = max(item["id"] for item in response.json())

    name, price = "abc", 10.0
    response = client.post("/items", json={"name": name, "price": price})
    assert response.status_code == 200, "Failed to create item"
    created_item = response.json()

    response = client.get("/items")
    assert response.status_code == 200, "Failed to fetch items after creation"
    after_max_id = max(item["id"] for item in response.json())

    assert created_item["id"] == after_max_id, "Created item ID does not match the expected ID"
    assert after_max_id == before_max_id + 1, "Item ID was not incremented correctly after creation"


def test_sorted_insertion_with_binary_search() -> None:
    name, price, low_price = "abc", 45.0, 40.0

    post_response = client.post("/items", json={"name": name, "price": price})
    posted_item = post_response.json()
    assert post_response.status_code == 200, "Failed to create item"

    response = client.get(f"/items?min_price={low_price}")
    assert response.status_code == 200, "Failed to fetch items with min_price filter"
    result_items = response.json()

    first_index_45 = next((i for i, item in enumerate(result_items) if item["price"] == price), None)

    assert first_index_45 is not None, "No item found with the specified price"
    assert result_items[first_index_45]["id"] == posted_item["id"], "The item ID does not match the expected ID"
