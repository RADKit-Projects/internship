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
