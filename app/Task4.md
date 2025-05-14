# Task 4: Reducing Time Complexity

## Adding Pagination

Paginating search results to avoid returning the full dataset on every request. This can improve performance as the item list grows larger.

### Steps to Implement:

1. **Request Query Parameters:**
   - `skip`: the number of items to skip.
   - `limit`: the maximum number of items to return per request (controls page size).

2. **Modify the `/items` Endpoint:**
   - Accept `skip` and `limit` as query parameters.
   - Return a subset of the data based on these values.

---

### Example:

```python

# Listing items with pagination
@app.get("/items", response_model=List[Item])
def list_items(skip: int = 0, limit: int = 50) -> List[Item]:
    # Return paginated items from the mock database
    return items_db[skip: skip + limit]
```

### Time Complexity:
  - **Before Pagination**: Fetching all items from a large list would be O(n), where `n` is the number of items.
  - **With Pagination**: Fetching a page of items would typically be O(m), where `m` is the `limit`.

---

## Using a Dictionary for Faster Lookups

Replacing the list-based `items_db` with a dictionary allows constant-time (O(1)) retrieval of items by ID, improving performance as the dataset scales.

### Steps to Implement:

1. **Redefine the In-Memory Storage:**
   - Change `items_db` from a `List[Dict]` to a `Dict[int, Dict]` (keyed by item ID).

2. **Refactor Endpoints:**
   - Use `.get(id)` for quick access.
   - Ensure all CRUD operations update the dictionary accordingly.

---

### Example:

```python
# Use a dictionary instead of a list for item storage
items_db: dict[int, dict] = {}

# Create item
def create_item(item: ItemCreate) -> Item:
    new_id = max(items_db.keys(), default=0) + 1
    items_db[new_id] = item.model_dump()
    return Item(id=new_id, **items_db[new_id])

# Get item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in items_db:
        raise HTTPException(status_code=404)
    return Item(id=item_id, **items_db[item_id])
```
### Time Complexity:
  - **List Lookup**: O(1)
  - **Dictionary Lookup**: O(n)


---

## Using a Dictionary for Corresponding Names to a Single Index

Adding a secondary index dictionary to track item names would imporve the efficiency of checking for duplicate names.

### Steps to Implement:
1. **Create a Name Index:**
Maintain a separate dictionary name_index: Dict[str, int] mapping item names to IDs.

2. **Update on Create/Update/Delete:**
Add/remove entries from name_index when modifying items_db.

3. **Use the Index for Fast Duplicate Checks:**
Check if name in name_index before creating/updating an item.


### Time Complexity:
  - **With Name to Index Dictionary**: O(1)
  - **Without Secondary Dictionary*: O(n)

  