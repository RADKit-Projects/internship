from typing import List

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate

existing_names = set(item["name"] for item in items_db)

def get_items(min_price: float = 0.0, page_number: int = 0, size: int = 100) -> List[Item]:
    filtered_items = [item for item in items_db if item["price"] >= min_price]
    start = page_number * size
    end = start + size
    paginated_items = filtered_items[start:end] # works because python slicing is out of bounds safe
    return [Item(**item) for item in paginated_items]

def create_item(item: ItemCreate) -> Item | None:
    if item.name in existing_names:
        return None
    
    new_id = max(item["id"] for item in items_db) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items_db.append(new_item)
    existing_names.add(item.name)
    return Item(**new_item)

def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    if update.name in existing_names:
        return None

    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                existing_names.remove(item["name"])
                item["name"] = update.name
                existing_names.add(update.name)
            if update.price:
                item["price"] = update.price
            return Item(**item)
    return None
