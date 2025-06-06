# ***Task 5:***

## **Issue:**

In the `PUT /items/{item_id}` endpoint, the `update_item_by_id` function was not correctly updating the item when the
name already existed in the database. It would allow it to update even if the name was already taken. Besides this, the
function also did not properly handle the HTTP code error when the item to be updated was not found in the database.

**Failing Test:**

- `/tests/test_items.py` -> `test_update_to_duplicate_name`

**Added Tests:**

- `/tests/test_items.py` -> `test_check_item_correct_place_after_update`: Ensures that the item is correctly put in the
  sorted order after an update, only in case of a `price` change.
- `/tests/test_items.py` -> `test_update_item_not_found`: Ensures that the correct behavior when trying to update an
  item that does not exist in the database.
- `/tests/test_items.py` -> `test_create_item`: Ensures that an item can be created successfully, and it fails if the
  item already exists.

## **Fix:**

Implemented duplicate name checking on the `update_item_by_id` and `create_item` functions in `crud.py`:

- First, there was a need to check if the item with the given `item_id` exists in the database. If it does not,
  the function should return a **404 Not Found error**.
- Then, before updating the item, the function should check if the new `name` already exists in the database.
  If it does, it should return a **400 Bad Request** error indicating that the `name` is already taken.
- When updating the name, there was the need to:

    - Remove the old name from the `name_set`.
    - Update the item with the new name.
    - Add the new name to the `name_set`.

- If the price was updated, the item would be removed from the sorted list and reinserted at the correct position
  using binary search to maintain the sorted order.
- Finally, there was also the need to ensure that the `name` field was unique when creating a new item, so the
  `create_item` function was also updated to check for duplicate names before adding a new item.

## **Reasoning**:

1. After reviewing the code and checking that the `test_update_to_duplicate_name` test was failing due to
   incorrect handling of duplicate names, I went to the `crud.py` file and checked the `update_item_by_id` function.
   With this I noticed that there was no validation for duplicate names before updating the item.

2. So, I first needed to ensure that the item with the given `item_id` exists in the database. If it does not, I
   returned a **404 Not Found error**. This had to be done in the `item_db` sorted list, leading to a linear search.
   There was a possibility to improve this by having a dictionary with the items indexed by their `id`s, but the
   complexity and maintainability the code would increase significantly and I chose to avoid it for now.

3. Then, I needed to check if the new `name` already exists in the database. If it does, I returned a
   **400 Bad Request** error indicating that the `name` is already taken. This was done by checking the new `name_set`
   in the `/app/database.py` file that keeps track of all the names. The **Set data structure** here was the best option
   to ensure uniqueness and fast lookups.

4. After that, I had to remove the old name from the `name_set`, update the item with the new name, and add the new
   name to the `name_set`.

5. Now, if the price was updated, I had to remove the item from the sorted list and reinsert it at the
   correct position using binary search to maintain the sorted order. This was necessary to ensure that the items
   remained sorted by price after an update.

6. Performance-wise, price updates are relatively expensive because of the removal(highly costly) and re-insertion being
   **O(n)**. However, this tradeoff was necessary to ensure data consistency in the sorted list. In practice, updates
   may be infrequent enough that the cost is acceptable, but this is something to keep in mind for **future
   optimizations** with more metrics available of what endpoints are being used more frequently.

7. Finally, I also updated the `create_item` function to check for duplicate names before adding a new item.
   This was necessary to ensure that the `name` field was unique when creating a new item.

**Commit:** `Bugfix (Tasks 5 & 6) - Handled duplicate name edge case on update and create and improved test 
"test_item_name_consistency" robustness`