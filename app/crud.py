from typing import List

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate


def get_items(min_price: float = 0.0, limit: int = 100, offset: int = 0) -> List[Item]:
    filtered = [Item(**item) for item in items_db.values() if item["price"] >= min_price]
    return filtered[offset:offset + limit]


def create_item(item: ItemCreate) -> Item:
    new_id = max(items_db.keys(), default=0) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items_db[new_id] = new_item
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    if update.name and any(
        item["name"] == update.name for item in items_db.values() if item["id"] != item_id
    ):
        return None

    item = items_db.get(item_id)
    if not item:
        return None
    if update.name:
        item["name"] = update.name
    if update.price:
        item["price"] = update.price
    return Item(**item)
