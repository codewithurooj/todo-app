# Technical Research: Delete Task Feature

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Status**: Completed

## Overview

This document captures technical research and decisions made during the planning phase for the Delete Task feature. All decisions build on the existing foundation from 001-add-task while adding delete-specific functionality.

---

## 1. Delete Operation Design

### Decision

**Choice**: Remove by ID search using list comprehension (filter out deleted)

**Rationale**:
- Clean, Pythonic approach using list comprehension
- Safe: creates new list without mutating during iteration
- Clear intent: `self._tasks = [t for t in self._tasks if t.id != task_id]`
- Preserves order of remaining tasks
- No index management complexity

**Alternatives Considered**:
- **Remove by index**: Requires finding index first, two-step process, error-prone
- **list.remove()**: Requires finding task object first, not ideal for ID-based lookup
- **Direct mutation during iteration**: Unsafe, can cause iteration issues

**Implementation**:
```python
def delete_task(self, task_id: int) -> bool:
    original_len = len(self._tasks)
    self._tasks = [t for t in self._tasks if t.id != task_id]
    return len(self._tasks) < original_len  # True if deleted
```

**Evolution Path**: Phase II (file persistence) can serialize the filtered list to JSON. Phase IV (database) translates to SQL DELETE operation.

---

## 2. ID Preservation Strategy

### Decision

**Choice**: Never decrement ID counter + validation at creation time

**Rationale**:
- ID counter (`_next_id`) only increments, never decrements
- Deleted IDs become "retired" - permanently unavailable
- Simple implementation: no tracking of deleted IDs needed
- Consistent with Add Task behavior (sequential, monotonic IDs)
- Prevents ID collision issues

**Alternatives Considered**:
- **Track deleted IDs for reuse**: Complex, violates YAGNI, adds memory overhead
- **Compact IDs after deletion**: Breaks user expectations, confusing UX
- **UUID instead of sequential**: Overkill for Phase I, harder to reference in console

**Implementation**: No changes to `_next_id` logic from 001-add-task. Deletion removes task from list but doesn't affect counter.

**Evolution Path**: Phase IV (distributed system) will require UUIDs or distributed ID generation, but Phase I-III can use sequential IDs safely.

---

## 3. Confirmation Flow Design

### Decision

**Choice**: CLI layer handles confirmation (separate from service layer)

**Rationale**:
- Separation of concerns: business logic (service) vs user interaction (CLI)
- Service layer remains testable without user input mocking
- Confirmation is a UI/UX concern, not business logic
- Reusable: service can be called from API in Phase III without confirmation
- Flexibility: Easy to make confirmation optional or configurable

**Alternatives Considered**:
- **Service layer confirmation**: Mixes business logic with UI, harder to test
- **Separate confirmation utility**: Over-engineering for Phase I, YAGNI violation

**Implementation**:
```python
# In cli/task_cli.py
def delete_task_cli(task_service, task_id):
    task = task_service.get_task_by_id(task_id)
    if task:
        confirm = input(f"Delete task #{task.id}: '{task.title}'? (y/n): ")
        if confirm.lower() in ['y', 'yes']:
            task_service.delete_task(task_id)
            print(f"Task #{task_id} '{task.title}' deleted successfully")
        else:
            print("Deletion cancelled")
```

**Evolution Path**: REST API (Phase III) won't include confirmation - client handles that.

---

## 4. Error Handling Patterns

### Decision

**Choice**: Return tuple pattern `(success: bool, message: str)` from service layer

**Rationale**:
- Pythonic: similar to validation pattern from 001-add-task
- No exceptions for expected failures (non-existent ID is expected user error)
- Clear success/failure indication
- Provides user-friendly error message
- Easy to test both paths

**Alternatives Considered**:
- **Return None on failure**: Ambiguous, doesn't provide error reason
- **Raise exception**: Exceptions for control flow is anti-pattern, expensive
- **Return Task | None**: Doesn't indicate why failure occurred

**Implementation**:
```python
def delete_task(self, task_id: int) -> tuple[bool, str]:
    task = self.get_task_by_id(task_id)
    if not task:
        return False, f"Error: Task #{task_id} not found"

    self._tasks = [t for t in self._tasks if t.id != task_id]
    return True, f"Task #{task_id} '{task.title}' deleted successfully"
```

**Evolution Path**: REST API will map to HTTP status codes (404 for not found, 200 for success).

---

## 5. Validation Integration

### Decision

**Choice**: Extend validators.py with `validate_task_id()` function

**Rationale**:
- Reuses existing validation pattern from 001-add-task
- Centralized validation logic
- Testable in isolation
- Can be reused by Update and Mark Complete features
- Follows DRY principle

**Alternatives Considered**:
- **Inline validation in service**: Violates SRP, not reusable
- **Service-level validation only**: Misses pre-validation opportunity

**Implementation**:
```python
# In utils/validators.py
def validate_task_id(task_id_str: str) -> tuple[bool, int | None, str]:
    """
    Validate task ID input.

    Returns:
        (True, task_id, "") if valid
        (False, None, error_message) if invalid
    """
    if not task_id_str:
        return False, None, "Error: Task ID cannot be empty"

    try:
        task_id = int(task_id_str)
        if task_id < 1:
            return False, None, "Error: Task ID must be a positive number"
        return True, task_id, ""
    except ValueError:
        return False, None, "Error: Invalid task ID. Please enter a numeric ID"
```

**Evolution Path**: Phase III (REST API) will use Pydantic for request validation.

---

## 6. Empty List Handling

### Decision

**Choice**: Check list emptiness before prompting for ID input

**Rationale**:
- Better UX: Don't ask for ID if there's nothing to delete
- Fails fast: Immediate feedback to user
- Prevents unnecessary validation errors
- Clear error message: "No tasks available to delete"

**Implementation**:
```python
def delete_task_cli(task_list):
    if not task_list.get_all_tasks():
        print("No tasks available to delete")
        return

    # Proceed with ID prompt...
```

**Evolution Path**: Consistent with View Tasks feature (004).

---

## 7. Cancel Operation Handling

### Decision

**Choice**: Accept "cancel" keyword (case-insensitive) at ID prompt

**Rationale**:
- User-friendly: Provides escape hatch before destructive operation
- Low complexity: Simple string check
- Follows CLI best practices
- No additional confirmation needed if user cancels early

**Implementation**:
```python
task_id_input = input("Enter task ID to delete (or 'cancel' to abort): ")
if task_id_input.lower() == 'cancel':
    print("Delete operation cancelled")
    return
```

**Evolution Path**: REST API won't need this - HTTP DELETE can simply not be called.

---

## 8. Leading Zeros Handling

### Decision

**Choice**: Python's `int()` automatically handles leading zeros

**Rationale**:
- Built-in behavior: `int("007")` returns `7`
- No custom logic needed
- Consistent with user expectations
- Works for all valid numeric formats

**Implementation**: No special handling needed beyond `int(task_id_str)` in validator.

---

## Summary of Decisions

| Decision Area | Choice |
|---------------|--------|
| Delete Operation | Filter out using list comprehension |
| ID Preservation | Never decrement counter, retired IDs |
| Confirmation Flow | CLI layer (not service layer) |
| Error Handling | Return tuple (success, message) |
| Validation | Extend validators.py with validate_task_id() |
| Empty List | Check before prompting for input |
| Cancel Operation | Accept "cancel" keyword at prompt |
| Leading Zeros | Use built-in int() behavior |

---

**Status**: All research complete. Ready for Phase 1 (Design & Contracts).
