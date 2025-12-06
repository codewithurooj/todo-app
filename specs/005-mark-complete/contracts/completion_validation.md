# Contract: Completion Status Validation

**Feature**: 005-mark-complete
**Component**: Validation functions for mark complete operations
**Created**: 2025-12-06

---

## Purpose

Define validation contracts for completion status operations. These functions ensure data integrity before marking tasks as complete or reopening them.

---

## Function: `validate_task_exists()`

### Signature

```python
def validate_task_exists(
    task_id: int,
    task_list: TaskList
) -> Tuple[bool, Optional[Task], str]:
    """
    Validate that a task with given ID exists.

    Args:
        task_id: Task identifier to validate
        task_list: TaskList instance to search

    Returns:
        Tuple[bool, Optional[Task], str]: (valid, task, error_message)
            - (True, task, "") if task exists
            - (False, None, error_msg) if task not found

    Validates:
        - task_id is positive integer
        - Task with task_id exists in task_list

    Examples:
        >>> task_list = TaskList()
        >>> task_list.add("Buy milk", "")
        >>> valid, task, msg = validate_task_exists(1, task_list)
        >>> assert valid == True
        >>> assert task.id == 1

        >>> valid, task, msg = validate_task_exists(999, task_list)
        >>> assert valid == False
        >>> assert msg == "Error: Task with ID 999 not found"
    """
```

### Implementation

```python
def validate_task_exists(
    task_id: int,
    task_list: TaskList
) -> Tuple[bool, Optional[Task], str]:
    """Validate task existence."""
    # Validate task_id type and range
    if not isinstance(task_id, int):
        return (False, None, "Task ID must be an integer")

    if task_id < 1:
        return (False, None, "Task ID must be a positive integer")

    # Check task existence
    task = task_list.find_by_id(task_id)
    if task is None:
        return (False, None, f"Error: Task with ID {task_id} not found")

    return (True, task, "")
```

### Validation Rules

| Condition | Result | Error Message |
|-----------|--------|---------------|
| task_id not an integer | Invalid | "Task ID must be an integer" |
| task_id < 1 | Invalid | "Task ID must be a positive integer" |
| task_id not in list | Invalid | "Error: Task with ID {task_id} not found" |
| task_id exists | Valid | "" (empty string) |

---

## Function: `validate_can_mark_complete()`

### Signature

```python
def validate_can_mark_complete(task: Task) -> Tuple[bool, str]:
    """
    Validate that a task can be marked as complete.

    This validation is informational (idempotent) - it returns True even if
    the task is already completed, but provides a warning message.

    Args:
        task: Task instance to validate

    Returns:
        Tuple[bool, str]: (can_proceed, message)
            - (True, "") if task is pending (can mark complete)
            - (True, warning_msg) if task already completed (idempotent)

    Note:
        This function never returns False - operations are idempotent.
        The message indicates whether state will change.

    Examples:
        >>> task = Task(1, "Buy milk", "", datetime.now(UTC), datetime.now(UTC), False)
        >>> can_proceed, msg = validate_can_mark_complete(task)
        >>> assert can_proceed == True
        >>> assert msg == ""

        >>> task.completed = True
        >>> can_proceed, msg = validate_can_mark_complete(task)
        >>> assert can_proceed == True
        >>> assert msg == "Task 1 is already completed"
    """
```

### Implementation

```python
def validate_can_mark_complete(task: Task) -> Tuple[bool, str]:
    """Validate task can be marked complete."""
    if task.completed:
        return (True, f"Task {task.id} is already completed")
    return (True, "")
```

### Behavior

- **Pending task**: Returns `(True, "")` - proceed with status change
- **Completed task**: Returns `(True, warning_msg)` - no status change needed (idempotent)

---

## Function: `validate_can_reopen()`

### Signature

```python
def validate_can_reopen(task: Task) -> Tuple[bool, str]:
    """
    Validate that a task can be reopened (unmarked as complete).

    This validation is informational (idempotent) - it returns True even if
    the task is already pending, but provides a warning message.

    Args:
        task: Task instance to validate

    Returns:
        Tuple[bool, str]: (can_proceed, message)
            - (True, "") if task is completed (can reopen)
            - (True, warning_msg) if task already pending (idempotent)

    Note:
        This function never returns False - operations are idempotent.
        The message indicates whether state will change.

    Examples:
        >>> task = Task(1, "Buy milk", "", datetime.now(UTC), datetime.now(UTC), True)
        >>> can_proceed, msg = validate_can_reopen(task)
        >>> assert can_proceed == True
        >>> assert msg == ""

        >>> task.completed = False
        >>> can_proceed, msg = validate_can_reopen(task)
        >>> assert can_proceed == True
        >>> assert msg == "Task 1 is already pending"
    """
```

### Implementation

```python
def validate_can_reopen(task: Task) -> Tuple[bool, str]:
    """Validate task can be reopened."""
    if not task.completed:
        return (True, f"Task {task.id} is already pending")
    return (True, "")
```

### Behavior

- **Completed task**: Returns `(True, "")` - proceed with status change
- **Pending task**: Returns `(True, warning_msg)` - no status change needed (idempotent)

---

## Function: `validate_field_immutability()`

### Signature

```python
def validate_field_immutability(
    before: Task,
    after: Task
) -> Tuple[bool, str]:
    """
    Validate that immutable fields were not changed during status update.

    This is a post-condition check used in tests to verify data integrity.

    Args:
        before: Task state before status update
        after: Task state after status update

    Returns:
        Tuple[bool, str]: (valid, error_message)
            - (True, "") if all immutable fields preserved
            - (False, error_msg) if any immutable field changed

    Immutable Fields:
        - id
        - title
        - description
        - created_at

    Examples:
        >>> task_before = Task(1, "Buy milk", "Whole milk", created, updated, False)
        >>> # Simulate mark complete operation
        >>> task_after = Task(1, "Buy milk", "Whole milk", created, new_updated, True)
        >>> valid, msg = validate_field_immutability(task_before, task_after)
        >>> assert valid == True

        >>> # Simulate invalid operation that changed title
        >>> task_after_bad = Task(1, "Buy eggs", "Whole milk", created, new_updated, True)
        >>> valid, msg = validate_field_immutability(task_before, task_after_bad)
        >>> assert valid == False
        >>> assert "title" in msg
    """
```

### Implementation

```python
def validate_field_immutability(
    before: Task,
    after: Task
) -> Tuple[bool, str]:
    """Validate immutable fields preserved."""
    errors = []

    if before.id != after.id:
        errors.append(f"id changed from {before.id} to {after.id}")

    if before.title != after.title:
        errors.append(f"title changed from '{before.title}' to '{after.title}'")

    if before.description != after.description:
        errors.append(f"description changed from '{before.description}' to '{after.description}'")

    if before.created_at != after.created_at:
        errors.append(f"created_at changed from {before.created_at} to {after.created_at}")

    if errors:
        return (False, f"Immutable fields modified: {'; '.join(errors)}")

    return (True, "")
```

### Validation Rules

All immutable fields MUST remain unchanged:
- `task.id` - Unique identifier
- `task.title` - Task summary
- `task.description` - Task details
- `task.created_at` - Creation timestamp

**Mutable fields** (allowed to change):
- `task.completed` - Completion status (expected to change)
- `task.updated_at` - Last modified timestamp (expected to change)

---

## Function: `validate_timestamp_accuracy()`

### Signature

```python
def validate_timestamp_accuracy(
    operation_time: datetime,
    updated_at: datetime,
    tolerance_seconds: int = 1
) -> Tuple[bool, str]:
    """
    Validate that updated_at timestamp is accurate within tolerance.

    Args:
        operation_time: Time when operation was initiated
        updated_at: Task's updated_at timestamp after operation
        tolerance_seconds: Acceptable difference in seconds (default: 1)

    Returns:
        Tuple[bool, str]: (valid, error_message)
            - (True, "") if timestamp within tolerance
            - (False, error_msg) if timestamp outside tolerance

    Success Criterion:
        SC-003: Timestamps accurate within ±1 second

    Examples:
        >>> op_time = datetime.now(UTC)
        >>> updated = datetime.now(UTC)
        >>> valid, msg = validate_timestamp_accuracy(op_time, updated)
        >>> assert valid == True

        >>> old_time = datetime.now(UTC) - timedelta(seconds=5)
        >>> valid, msg = validate_timestamp_accuracy(op_time, old_time)
        >>> assert valid == False
    """
```

### Implementation

```python
from datetime import timedelta

def validate_timestamp_accuracy(
    operation_time: datetime,
    updated_at: datetime,
    tolerance_seconds: int = 1
) -> Tuple[bool, str]:
    """Validate timestamp accuracy."""
    diff = abs((updated_at - operation_time).total_seconds())

    if diff > tolerance_seconds:
        return (
            False,
            f"Timestamp difference {diff:.2f}s exceeds tolerance {tolerance_seconds}s"
        )

    return (True, "")
```

---

## Integration with TaskList Methods

### Usage in `mark_complete()`

```python
def mark_complete(self, task_id: int) -> Tuple[bool, str]:
    """Mark task complete with validation."""
    # Step 1: Validate task exists
    valid, task, error_msg = validate_task_exists(task_id, self)
    if not valid:
        return (False, error_msg)

    # Step 2: Check if already completed (idempotent)
    can_proceed, warning_msg = validate_can_mark_complete(task)
    if warning_msg:
        return (True, warning_msg)  # Idempotent success

    # Step 3: Update status (atomically)
    task.completed = True
    task.updated_at = datetime.now(UTC)

    return (True, f"✓ Task {task_id} marked as complete")
```

### Usage in `unmark_complete()`

```python
def unmark_complete(self, task_id: int) -> Tuple[bool, str]:
    """Reopen task with validation."""
    # Step 1: Validate task exists
    valid, task, error_msg = validate_task_exists(task_id, self)
    if not valid:
        return (False, error_msg)

    # Step 2: Check if already pending (idempotent)
    can_proceed, warning_msg = validate_can_reopen(task)
    if warning_msg:
        return (True, warning_msg)  # Idempotent success

    # Step 3: Update status (atomically)
    task.completed = False
    task.updated_at = datetime.now(UTC)

    return (True, f"✓ Task {task_id} reopened (marked as pending)")
```

---

## Testing Requirements

### Unit Tests (Required)

```python
def test_validate_task_exists_valid():
    """Verify validation succeeds for existing task."""

def test_validate_task_exists_not_found():
    """Verify validation fails for non-existent task."""

def test_validate_task_exists_invalid_id():
    """Verify validation fails for negative/zero task ID."""

def test_validate_can_mark_complete_pending():
    """Verify pending task can be marked complete."""

def test_validate_can_mark_complete_already_completed():
    """Verify already-completed task returns idempotent message."""

def test_validate_can_reopen_completed():
    """Verify completed task can be reopened."""

def test_validate_can_reopen_already_pending():
    """Verify already-pending task returns idempotent message."""

def test_validate_field_immutability_preserved():
    """Verify validation passes when immutable fields unchanged."""

def test_validate_field_immutability_violated():
    """Verify validation fails when immutable fields change."""

def test_validate_timestamp_accuracy_within_tolerance():
    """Verify validation passes for timestamps within ±1s."""

def test_validate_timestamp_accuracy_outside_tolerance():
    """Verify validation fails for timestamps >1s difference."""
```

---

## Evolution Notes

### Phase II: File Persistence

Add validation for file system operations:
- `validate_file_writable()` - Check file write permissions before update
- `validate_file_lock()` - Ensure no concurrent modifications

### Phase IV: Database Persistence

Add validation for database constraints:
- `validate_version_match()` - Optimistic locking check
- `validate_transaction_open()` - Ensure transaction context
- `validate_foreign_keys()` - Check referential integrity

---

## Contract Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-06 | Initial validation contracts for Phase I |

---

## Notes

- All validation functions return tuples for consistent error handling
- Idempotent validations return `(True, warning_msg)` instead of `(False, error_msg)`
- Field immutability and timestamp accuracy validations used primarily in tests
- Task existence validation is the only hard failure condition
