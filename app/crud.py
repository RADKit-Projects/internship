import time
from typing import List

import app.database as db
from app.models import Item, ItemCreate, ItemUpdate
from itertools import islice

# RETURN_CODES
RETURN_CODES = {
    "Success": "Success",
    "Duplicate_Name": "Duplicate_Name",
    "Not_Found": "Not_Found"
}


def _binary_search_index(target: float) -> int:
    low, high, idx = 0, len(db.items_db) - 1, len(db.items_db)
    while low <= high:
        mid = (low + high) // 2
        if db.items_db[mid].price >= target:
            idx = mid
            high = mid - 1
        else:
            low = mid + 1
    return idx


def get_items(min_price: float = 0.0, limit: int = 50) -> List[Item]:
    start_item_idx = _binary_search_index(min_price)
    items = list(islice(db.items_db, start_item_idx, (start_item_idx + limit) if limit else None))
    return items


def create_item(item: ItemCreate) -> tuple[str, Item | None]:
    if item.name in db.name_set:
        return RETURN_CODES["Duplicate_Name"], None

    new_item = Item(id=db.next_id, name=item.name, price=item.price)

    index = _binary_search_index(new_item.price)
    db.items_db.insert(index, new_item)

    db.next_id += 1
    db.name_set.add(new_item.name)
    return RETURN_CODES["Success"], new_item


def update_item_by_id(item_id: int, update: ItemUpdate) -> tuple[str, Item | None]:
    item = next((item for item in db.items_db if item.id == item_id), None)
    if not item:
        return RETURN_CODES["Not_Found"], None

    if update.name and update.name != item.name:
        if update.name in db.name_set:
            return RETURN_CODES["Duplicate_Name"], None

        db.name_set.remove(item.name)
        item.name = update.name
        db.name_set.add(item.name)

    if update.price is not None and update.price != item.price:
        db.items_db.remove(item)
        item.price = update.price
        index = _binary_search_index(item.price)
        db.items_db.insert(index, item)

    return RETURN_CODES["Success"], item
