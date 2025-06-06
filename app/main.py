from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()


@app.get("/health") # Fixed spelling of "health"
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items") # Added pagination and filtering
def list_items(min_price: float = Query(0.0), limit: int = Query(100, ge=1, le=100000000), offset: int = Query(0, ge=0)) -> list[Item]:
    return get_items(min_price=min_price, limit=limit, offset=offset)


@app.post("/items")
def add_item(item: ItemCreate) -> Item:
    if len(item.name) < 3: # Ensure item name is at least 3 characters long
        raise HTTPException(status_code=422, detail="Item name must be at least 3 characters long")
    return create_item(item)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate) -> Item:
    updated = update_item_by_id(item_id, item)
    if not updated:
        raise HTTPException(status_code=400, detail="Item not found or duplicate name")
    return updated
