# Validation Contract: Delete Task

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Type**: Validation Contract

---

## Overview

This contract defines validation rules for delete task operations. Extends validation.md from 001-add-task.

---

## Task ID Validation

### Contract

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | None, str]:
    """
    Validate task ID input for delete operations.

    Args:
        task_id_str: User-provided task ID string

    Returns:
        (True, task_id, "") if valid
        (False, None, error_message) if invalid
        (False, None, "CANCEL") if user cancels

    Validation Rules:
        1. Empty check: Must not be empty string
        2. Cancel check: "cancel" (case-insensitive) returns special code
        3. Type check: Must be parseable as integer
        4. Range check: Must be >= 1

    Error Messages:
        - "Error: Task ID cannot be empty" (empty input)
        - "Error: Invalid task ID. Please enter a numeric ID" (non-numeric)
        - "Error: Task ID must be a positive number" (negative/zero)
        - "CANCEL" (user typed cancel)
    """
```

### Test Cases

```python
# Valid inputs
assert validate_task_id("1") == (True, 1, "")
assert validate_task_id("42") == (True, 42, "")
assert validate_task_id("007") == (True, 7, "")
assert validate_task_id("  5  ") == (True, 5, "")

# Invalid inputs
assert validate_task_id("") == (False, None, "Error: Task ID cannot be empty")
assert validate_task_id("  ") == (False, None, "Error: Task ID cannot be empty")
assert validate_task_id("abc") == (False, None, "Error: Invalid task ID. Please enter a numeric ID")
assert validate_task_id("-1") == (False, None, "Error: Task ID must be a positive number")
assert validate_task_id("0") == (False, None, "Error: Task ID must be a positive number")

# Cancel inputs
assert validate_task_id("cancel") == (False, None, "CANCEL")
assert validate_task_id("CANCEL") == (False, None, "CANCEL")
assert validate_task_id("Cancel") == (False, None, "CANCEL")
```

---

## Confirmation Validation

### Contract

```python
def validate_confirmation(response: str) -> tuple[bool, bool | None, str]:
    """
    Validate confirmation response (y/n).

    Args:
        response: User response to confirmation prompt

    Returns:
        (True, confirmed, "") if valid
        (False, None, error_message) if invalid

    Validation Rules:
        - Accepted yes: "y", "yes" (case-insensitive)
        - Accepted no: "n", "no" (case-insensitive)
        - All other inputs are invalid

    Error Message:
        - "Please enter 'y' for yes or 'n' for no"
    """
```

### Test Cases

```python
# Valid yes
assert validate_confirmation("y") == (True, True, "")
assert validate_confirmation("Y") == (True, True, "")
assert validate_confirmation("yes") == (True, True, "")
assert validate_confirmation("YES") == (True, True, "")

# Valid no
assert validate_confirmation("n") == (True, False, "")
assert validate_confirmation("N") == (True, False, "")
assert validate_confirmation("no") == (True, False, "")
assert validate_confirmation("NO") == (True, False, "")

# Invalid
assert validate_confirmation("") == (False, None, "Please enter 'y' for yes or 'n' for no")
assert validate_confirmation("maybe") == (False, None, "Please enter 'y' for yes or 'n' for no")
```

---

## Standard Error Messages

```python
VALIDATION_ERRORS = {
    # Task ID errors
    "task_id_empty": "Error: Task ID cannot be empty",
    "task_id_invalid": "Error: Invalid task ID. Please enter a numeric ID",
    "task_id_negative": "Error: Task ID must be a positive number",
    "task_id_cancel": "CANCEL",

    # Confirmation errors
    "confirmation_invalid": "Please enter 'y' for yes or 'n' for no",

    # Task existence errors (service layer)
    "task_not_found": "Error: Task #{{id}} not found. Please enter a valid task ID.",
}
```

---

## Testing Requirements

### Unit Tests

- ✅ Task ID: valid numbers (1, 42, 1000)
- ✅ Task ID: leading zeros ("007" → 7)
- ✅ Task ID: whitespace handling
- ✅ Task ID: empty string
- ✅ Task ID: non-numeric ("abc", "1.5", "#5")
- ✅ Task ID: negative/zero
- ✅ Task ID: cancel keyword (all cases)
- ✅ Confirmation: yes variants (y, Y, yes, YES)
- ✅ Confirmation: no variants (n, N, no, NO)
- ✅ Confirmation: invalid inputs

### Integration Tests

- ✅ Validation errors trigger re-prompt
- ✅ Cancel at ID prompt returns to menu
- ✅ Cancel at confirmation keeps task

---

**Status**: Contract Defined
**Version**: 1.0.0
**Last Updated**: 2025-12-06
