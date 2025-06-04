# ***Task 2:***

## **Issue:**

Endpoint for `GET /items` was not filtering correctly by the `min_price` query parameter. Instead of returning items
with a **greater than or equal** to the specified `min_price`, it returned items with price **lesser than or equal**.

**Failing Test:**

- `/tests/test_items.py` -> `test_min_price_filter`

## **Fix:**

Corrected the filtering loop to return items where the `item["price"] >= min_price` in `crud.py`, *(line 8)*.

## **Reasoning**:

1. After reviewing the code and checking that the `test_min_price_filter` test was failing due to incorrect filtering
   logic, I checked the `GET /items` endpoint and went to the `get_items()` function in `crud.py` file and 
   found that the filtering condition was reversed.

2. After that I changed to condition from **less than or equal** than the `min_price`, instead of **greater than or
   equal**.

**Commit:** `BugFix (Task 2) - Corrected min_price filtering logic in get_items function and added Task 2 Summary`