import time
from typing import List

import app.database as db
from app.models import Item, ItemCreate, ItemUpdate
from itertools import islice


def binary_search_index(target: float) -> int:
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
    start_item_idx = binary_search_index(min_price)
    items = list(islice(db.items_db, start_item_idx, (start_item_idx + limit) if limit else None))
    return items


def create_item(item: ItemCreate) -> Item:
    new_item = Item(id=db.next_id, name=item.name, price=item.price)

    index = binary_search_index(new_item.price)
    db.items_db.insert(index, new_item)

    db.next_id += 1
    return new_item


def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    for item in db.items_db:
        if item.id == item_id:
            if update.name:
                item.name = update.name
            if update.price:
                item.price = update.price
            return item
    return None
