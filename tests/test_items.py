from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json())


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422

def test_create_duplicate_item() -> None:
    client.post("/items", json={"name": "Mango", "price": 4.0})
    response = client.post("/items", json={"name": "Mango", "price": 6.0})
    assert response.status_code == 409 or response.status_code == 422

def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 404 or resp.status_code == 422

def test_item_name_consistency() -> None:
    new_name = "TestItem123"
    response = client.post("/items", json={"name": new_name, "price": 15})
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == new_name

    item_id = created_item["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == new_name

def test_get_nonexistent_item() -> None:
    new_item = {"name": "TemporaryTestItem", "price": 9.99}
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    created = response.json()
    created_id = created["id"]

    nonexistent_id = created_id + 1

    response = client.get(f"/items/{nonexistent_id}")
    assert response.status_code == 404

def test_get_items_pagination() -> None:
    page_size = 3
    for i in range(page_size):
        response = client.post("/items", json={"name": f"PaginateTestItem{i}", "price": 10})
        assert response.status_code == 200

    response = client.get(f"/items?page_number=0&size={page_size}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == page_size