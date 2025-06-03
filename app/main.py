from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id, get_item_by_id
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items")
def list_items(
    min_price: float = Query(0.0),
    page_number: int = Query(0, ge=0),
    size: int = Query(100, gt=0)
) -> list[Item]:
    return get_items(min_price=min_price, page_number=page_number, size=size)


@app.post("/items")
def add_item(item: ItemCreate) -> Item:
    created = create_item(item)
    if not created:
        raise HTTPException(status_code=409, detail="Item not created because duplicate name")
    return created


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate) -> Item:
    updated = update_item_by_id(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found or duplicate name")
    return updated
