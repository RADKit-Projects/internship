import json
from pathlib import Path

path = Path(__file__).parent / "items_db.json"
with path.open("r") as f: # Modified to use a dict to store items
    items_list = json.load(f)
    items_db = {item["id"]: item for item in items_list}
