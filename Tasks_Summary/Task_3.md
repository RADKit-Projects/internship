# ***Task 3:***

## **Issue:**

Endpoint for `POST /items` was allowing to create items that were too short (less than three characters) in the `name`
field. Additionally, there was no validation for negative prices, and the update functionality did not
have proper testing.

**Failing Test:**

- `/tests/test_items.py` -> `test_short_name`

**Added Tests:**

- `/tests/test_items.py` -> `test_negative_price`: Ensures items cannot be created with negative prices.
- `/tests/test_items.py` -> `test_update_item`: Ensures that a complete Item update is working as intended.

## **Fix:**

Added validation in the `Item`, `ItemCreate`, and `ItemUpdate` models within `models.py` to:

- Ensure the `name` field has a minimum length of three characters.
- Ensure the `price` field is non-negative (≥ 0).

## **Reasoning**:

1. After reviewing the code and checking that the `test_short_name` test was passing incorrectly,
   I went to the `models.py` file and added validation for the `name` field to ensure it is at least three characters
   long in the `ItemCreate`, `ItemUpdate` and `Item` models (`min_length=3`).

2. After reviewing the code, I also noticed that there was no validation for negative prices, so I also altered the
   models to ensure that the `price` field is non-negative (`ge=0`).

3. Additionally, I added tests for negative prices (`test_negative_price`) and item updates (`test_update_item`)
   to ensure that these functionalities work as expected.

**Commit:** `BugFix (Task 3) - Added name length and price validation to Item with proper Testing 
and added Task 3 Summary`