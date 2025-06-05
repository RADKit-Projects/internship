# ***Task 4:***

## **Issue:**

The `GET /items` endpoint was too inefficient to handle the large number of items being filtered in linear time. This
caused performance issues as the item list grew. The endpoint for the `POST /items` was also taking too long to create
a new item due to the need to iterate through all items to check for the one with the highest ID.

**Added Tests:**

- `/tests/test_items.py` -> `test_sorted_insertion_with_binary_search`: Ensures that new items are inserted at the
  correct position so they appear as the first item with their price in the sorted list using binary search.
- `/tests/test_items.py` -> `test_create_item_max_id`: Ensures correct handling of item creation and that the new items
  receive incrementally highest `id`'s.

## **Fix:**

Implemented a binary search-based insertion and retrieval method by:

- Pre-sorting the item database (list of `Item`) by `price` on startup of the server without modifying the source
  database file (`/app/items_db.json`).
- Using a lower-bound binary search algorithm to find the first item matching the minimum price filter. This
  significantly reduced the time complexity of the search operation to logarithmic time.
- Adding support for a `limit` parameter on the `GET /items` endpoint to restrict the number of returned items and
  further improve response times, in case there is no need to fetch all of them until the last.
- Updated the `POST /items` endpoint to use a binary search for inserting new items, ensuring that the new item is
  correctly placed in the sorted list.
- Created the `next_id` variable in the `/app/database.py` file to keep track of the next ID to be assigned
  to a new item, which has to be incremented each time a new item is added by the `create_item` function.

## **Reasoning**:

1. After reviewing the code and checking that the `GET /items` endpoint was taking too long to filter items, I
   realized that the **linear search** was inefficient for large datasets and the need to create a
   **new List of `Item`'s** every single time the endpoint was called was also undermining a lot the time it took to
   process.

2. Just by pre-creating the list of `Item` on server startup there was a significant improvement in the time it took to
   fetch them. From around **3 seconds** to roughly **0.5 seconds**.

3. But this time could still be improved, by pre-sorting the list of `Item`'s by `price` and using a
   **binary search** to find the first item matching the minimum price filter. With this change, I was able to reduce
   the time it took to search for the items with a `min_price = 50`, for example, to around **0.04 seconds**.

4. Additionally, I added the `limit` parameter to the `GET /items` endpoint, which can further improve performance in
   cases where not all items are needed.

5. Now, that items are sorted by `price`, I also updated the `POST /items` endpoint to use binary search for inserting
   new items, ensuring that the new ones are placed in the correct first position in the sorted list. This made the
   insertion worse in terms of time complexity, but it was necessary to keep the list sorted.

6. To try and counter the time it took to create a new item (previously around **0.44 seconds** per creation), I created
   a `next_id` variable in the `/app/database.py` file to keep track of the next ID to be assigned to a new item, which
   has to be incremented each time a new item is added by the `create_item` function. This way, I was able to avoid
   iterating through all items to find the highest ID. This change reduced significantly the time it took to create a
   new item to about **0.001 seconds**.

7. I had also to keep in mind that the server startup time was being affected by the time it took to pre-sort the
   items, which went from about **0.74 seconds** to **4.0 seconds**. But being this is a one-time cost, it is worth it
   for the performance improvements in later requests.

8. Test coverage was also maintained, and the new insertion mechanism was tested to ensure correct item ordering.

**Commit:**
`Performance (Task 4) - Optimized item retrieval and insertion performance with binary search with proper 
Testing and added Task 4 Summary`