# Validation Contract

**Feature**: 001-add-task
**Date**: 2025-12-06
**Type**: Validation Contract

---

## Overview

This contract defines input validation rules and interfaces for the Add Task feature. All components that accept user input MUST use these validators.

---

## Validator Interface

### Function Contract

All validator functions MUST:
- Accept input to validate as first parameter
- Return `tuple[bool, str]` where:
  - First element: `True` if valid, `False` if invalid
  - Second element: Empty string if valid, error message if invalid
- Be pure functions (no side effects)
- Be stateless (no class instance required)
- Handle `None` values appropriately

---

## Title Validation

### Contract

```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title input.

    Args:
        title: User-provided title string

    Returns:
        (True, "") if valid
        (False, error_message) if invalid

    Validation Rules:
        1. Type check: Must be string
        2. Non-empty: Must not be empty after strip()
        3. Length: Must be 1-200 characters after strip()

    Error Messages:
        - "Title must be a string" (type error)
        - "Title cannot be empty" (empty/whitespace)
        - "Title cannot exceed 200 characters" (too long)
    """
```

### Test Cases

```python
# Valid inputs
assert validate_title("Buy groceries") == (True, "")
assert validate_title("  Task with spaces  ") == (True, "")
assert validate_title("A" * 200) == (True, "")
assert validate_title("Task 📝") == (True, "")

# Invalid inputs
assert validate_title("") == (False, "Title cannot be empty")
assert validate_title("   ") == (False, "Title cannot be empty")
assert validate_title("A" * 201) == (False, "Title cannot exceed 200 characters")
assert validate_title(123) == (False, "Title must be a string")
```

---

## Description Validation

### Contract

```python
def validate_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate task description input.

    Args:
        description: User-provided description string or None

    Returns:
        (True, "") if valid
        (False, error_message) if invalid

    Validation Rules:
        1. Optional: None is valid
        2. Type check: Must be string or None
        3. Length: Must be 0-1000 characters (no stripping)

    Error Messages:
        - "Description must be a string" (type error)
        - "Description cannot exceed 1000 characters" (too long)
    """
```

### Test Cases

```python
# Valid inputs
assert validate_description(None) == (True, "")
assert validate_description("") == (True, "")
assert validate_description("Some description") == (True, "")
assert validate_description("A" * 1000) == (True, "")
assert validate_description("  Leading spaces") == (True, "")

# Invalid inputs
assert validate_description("A" * 1001) == (False, "Description cannot exceed 1000 characters")
assert validate_description(123) == (False, "Description must be a string")
```

---

## Validation Workflow

### CLI Input Validation Flow

```
User Input → validate_title() → Valid? → validate_description() → Valid? → add_task()
                ↓                              ↓
              Invalid                        Invalid
                ↓                              ↓
           Show Error                     Show Error
                ↓                              ↓
           Re-prompt                      Re-prompt
```

### Error Handling Contract

When validation fails:
1. MUST display error message to user
2. MUST re-prompt for input
3. MUST NOT create task
4. MUST NOT raise exceptions
5. MUST allow user to retry

---

## Standard Error Messages

```python
VALIDATION_ERRORS = {
    # Title errors
    "title_empty": "Title cannot be empty",
    "title_too_long": "Title cannot exceed 200 characters",
    "title_invalid_type": "Title must be a string",

    # Description errors
    "description_too_long": "Description cannot exceed 1000 characters",
    "description_invalid_type": "Description must be a string",
}
```

---

## Testing Requirements

### Unit Tests

- ✅ Title: type check (string, int, None)
- ✅ Title: empty string
- ✅ Title: whitespace only (" ", "\t", "\n")
- ✅ Title: boundary (1 char, 200 chars, 201 chars)
- ✅ Title: Unicode (emoji, Chinese, Arabic)
- ✅ Description: None
- ✅ Description: type check (string, int)
- ✅ Description: empty string
- ✅ Description: boundary (0 chars, 1000 chars, 1001 chars)
- ✅ Description: Unicode
- ✅ Error messages match VALIDATION_ERRORS

### Integration Tests

- ✅ Rejected title triggers re-prompt
- ✅ Rejected description triggers re-prompt
- ✅ Valid inputs proceed to task creation

---

**Status**: Contract Defined
**Version**: 1.0.0
**Last Updated**: 2025-12-06
