# ***Task 1:***

## **Issue:**

Endpoint for `GET /health` was incorrectly defined as `GET /heath`, causing a 404 Not found error.

**Failing Test:**

- `/tests/test_items.py` -> `test_health`

## **Fix:**

Corrected the typo in `main.py` *(line 9)* from `GET /heath` to `GET /health`.

## **Reasoning**:

1. After reviewing the code and checking that the `test_health` test was failing due to a 404 Not found error,
   I went to the `main.py` file and found that the endpoint was incorrectly spelled as `GET /heath` instead of
   `GET /health`.

**Commit:** `BugFix (Task 1) - Corrected typo in /health endpoint`