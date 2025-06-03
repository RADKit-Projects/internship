from typing import List, Optional
from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate
from fastapi import HTTPException

# Checks if a given name already exists in the items_db.
# Ignores the item with item_id (useful for updates).
# Returns True if a duplicate is found, False otherwise.
def is_duplicate_name(name:str, item_id: Optional[int] = None) -> bool:
    if name is None:
        return False  

    for item in items_db:
        if item["name"] == name:
            if item_id is None or item["id"] != item_id:
                return True
    return False



def get_items(min_price: float = 0.0) -> List[Item]:
    #fix: fixed comparison logic now returns items above the mim_price has excepted
    return [Item(**item) for item in items_db if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item:
    # feat: prevent updating in case of a duplicate item name
    if is_duplicate_name(item.name):
        raise HTTPException(status_code=400, detail="Duplicate item name")


    new_id = max(item["id"] for item in items_db) + 1
    #fix:used model_dump() has dic() is deprecated 
    new_item = {"id": new_id, **item.model_dump()}
    items_db.append(new_item)
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    # feat: prevent updating in case of a duplicate item name
    if update.name:
        if is_duplicate_name(update.name,item):
            raise HTTPException(status_code=400, detail="Duplicate item name")

    
    for item in items_db:
        
        if item["id"] == item_id:
            if update.name:
                item["name"] = update.name
            if update.price:
                item["price"] = update.price
            return Item(**item)
    return None
