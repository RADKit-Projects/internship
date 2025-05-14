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


def test_update_to_duplicate_name() -> None:
    r = client.post("/items", json={"name": "Grape", "price": 6})
    print(r.status_code)

    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    response = client.get("/items")
    names = [item["name"] for item in response.json()]
    assert "Item500000" in names
