# ***Task 1:***
## **Issue:** 
Endpoint for `/health` was incorrectly defined as `/heath`, causing a 404 Not found error.

**Failing Test:**  /tests/test_items.py -> `test_health`

## **Fix:** 
Corrected the typo in `main.py` *(line 9)* from `/heath` to `/health`.

## **Reasoning**:
1. After reviewing the code and checking that the `test_health` test was failing due to a 404 Not found error, 
I went to the `main.py` file and found that the endpoint was incorrectly spelled as `/heath` instead of `/health`.

**Commit:** `BugFix (Task 1) - Corrected typo in /health endpoint`