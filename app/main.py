from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id, RETURN_CODES
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()


@app.get("/health" , response_model=dict[str, str])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items" , response_model=list[Item])
def list_items(min_price: float = Query(0.0),
               limit: Optional[int] = Query(None, ge=1)) -> list[Item]:
    return get_items(min_price=min_price, limit=limit)


@app.post("/items", response_model=Item)
def add_item(item: ItemCreate) -> Item:
    code, created = create_item(item)
    if code == RETURN_CODES["Duplicate_Name"]:
        raise HTTPException(status_code=400, detail="Item name already exists")
    return created


@app.put("/items/{item_id}" , response_model=Item)
def update_item(item_id: int, item: ItemUpdate) -> Item:
    code, updated = update_item_by_id(item_id, item)
    if code == RETURN_CODES["Not_Found"]:
        raise HTTPException(status_code=404, detail="Item not found")
    if code == RETURN_CODES["Duplicate_Name"]:
        raise HTTPException(status_code=400, detail="Item name already exists")
    return updated
