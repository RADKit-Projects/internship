import json
import time
from pathlib import Path

from app.models import Item

path = Path(__file__).parent / "items_db.json"
with path.open("r") as f:
    raw_data = json.load(f)

items_db: list[Item] = sorted([Item(**item) for item in raw_data], key=lambda item: item.price)

name_set: set[str] = {item.name for item in items_db}

next_id: int = max(item.id for item in items_db) + 1 if items_db else 1