from typing import List, Tuple
from fastapi import  FastAPI, HTTPException
from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate


def get_items(min_price: float = 0.0) -> List[Item]:
    return [Item(**item) for item in items_db if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item:
    new_id = len(items_db)
    new_item = {"id": new_id, **item.model_dump()}
    items_db.append(new_item)
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Tuple[Item | None, str]:
    for item in items_db:
        if item["id"] != item_id and update.name == item["name"]:
                raise HTTPException(status_code=400)

    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                item["name"] = update.name
            if update.price is not None:
                item["price"] = update.price
            return Item(**item)
        
    return None