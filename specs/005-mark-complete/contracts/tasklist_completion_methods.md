# Contract: TaskList Completion Methods

**Feature**: 005-mark-complete
**Component**: TaskList class - mark_complete() and unmark_complete() methods
**Created**: 2025-12-06

---

## Purpose

Define the interface contract for TaskList completion status operations. These methods extend the TaskList class (from 001-add-task) to support marking tasks as complete and reopening them.

---

## Method: `mark_complete()`

### Signature

```python
def mark_complete(self, task_id: int) -> Tuple[bool, str]:
    """
    Mark a pending task as complete.

    Args:
        task_id: Unique identifier of task to mark complete

    Returns:
        Tuple[bool, str]: (success, message)
            - (True, confirmation_msg) on success
            - (True, warning_msg) if already completed (idempotent)
            - (False, error_msg) if task not found

    Raises:
        None - all errors returned as (False, message)

    Side Effects:
        On success:
        - Sets task.completed = True
        - Updates task.updated_at = datetime.now(UTC)
        - Preserves all other task fields
    """
```

### Preconditions

- `task_id` is a positive integer
- TaskList instance is initialized

### Postconditions

**On Success** (task exists and was pending):
- Task completion status is `True`
- Task `updated_at` timestamp is updated to current UTC time
- All other task fields unchanged (id, title, description, created_at)
- Returns `(True, "✓ Task {task_id} marked as complete")`

**On Idempotent Success** (task exists and was already completed):
- Task state unchanged
- Returns `(True, "Task {task_id} is already completed")`

**On Failure** (task does not exist):
- No state changes
- Returns `(False, "Error: Task with ID {task_id} not found")`

### Examples

```python
# Success case
task_list = TaskList()
task_list.add("Buy groceries", "Milk, eggs, bread")
success, message = task_list.mark_complete(1)
assert success == True
assert message == "✓ Task 1 marked as complete"

# Idempotent case
success, message = task_list.mark_complete(1)
assert success == True
assert message == "Task 1 is already completed"

# Error case
success, message = task_list.mark_complete(999)
assert success == False
assert message == "Error: Task with ID 999 not found"
```

### Performance

- Time complexity: O(n) where n = number of tasks (linear search)
- Space complexity: O(1) (no additional allocation)
- Expected latency: <1ms for Phase I in-memory implementation

---

## Method: `unmark_complete()`

### Signature

```python
def unmark_complete(self, task_id: int) -> Tuple[bool, str]:
    """
    Reopen a completed task (change status to pending).

    Args:
        task_id: Unique identifier of task to reopen

    Returns:
        Tuple[bool, str]: (success, message)
            - (True, confirmation_msg) on success
            - (True, warning_msg) if already pending (idempotent)
            - (False, error_msg) if task not found

    Raises:
        None - all errors returned as (False, message)

    Side Effects:
        On success:
        - Sets task.completed = False
        - Updates task.updated_at = datetime.now(UTC)
        - Preserves all other task fields
    """
```

### Preconditions

- `task_id` is a positive integer
- TaskList instance is initialized

### Postconditions

**On Success** (task exists and was completed):
- Task completion status is `False`
- Task `updated_at` timestamp is updated to current UTC time
- All other task fields unchanged (id, title, description, created_at)
- Returns `(True, "✓ Task {task_id} reopened (marked as pending)")`

**On Idempotent Success** (task exists and was already pending):
- Task state unchanged
- Returns `(True, "Task {task_id} is already pending")`

**On Failure** (task does not exist):
- No state changes
- Returns `(False, "Error: Task with ID {task_id} not found")`

### Examples

```python
# Setup: Create and complete a task
task_list = TaskList()
task_list.add("Buy groceries", "Milk, eggs, bread")
task_list.mark_complete(1)

# Success case
success, message = task_list.unmark_complete(1)
assert success == True
assert message == "✓ Task 1 reopened (marked as pending)"

# Idempotent case
success, message = task_list.unmark_complete(1)
assert success == True
assert message == "Task 1 is already pending"

# Error case
success, message = task_list.unmark_complete(999)
assert success == False
assert message == "Error: Task with ID 999 not found"
```

### Performance

- Time complexity: O(n) where n = number of tasks (linear search)
- Space complexity: O(1) (no additional allocation)
- Expected latency: <1ms for Phase I in-memory implementation

---

## Error Handling

### Error Scenarios

| Scenario | Return Value | Message Format |
|----------|--------------|----------------|
| Task not found | `(False, msg)` | "Error: Task with ID {task_id} not found" |
| Already completed (mark) | `(True, msg)` | "Task {task_id} is already completed" |
| Already pending (unmark) | `(True, msg)` | "Task {task_id} is already pending" |

### Design Rationale

- **No Exceptions**: User input errors return error tuples instead of raising exceptions
- **Idempotent**: Duplicate operations succeed with informative warnings
- **Consistent Messages**: All errors follow "Error: ..." prefix pattern

---

## Integration Points

### Dependencies

**Required**:
- `Task` entity from 001-add-task (with `completed` and `updated_at` fields)
- `TaskList.find_by_id()` method from 001-add-task

**Used By**:
- CLI mark complete menu option (see `cli_mark_complete_handler.md`)
- Integration tests (see quickstart.md)

### State Transitions

```
mark_complete():   Pending → Completed
unmark_complete(): Completed → Pending
```

Both operations update `task.updated_at` timestamp.

---

## Testing Requirements

### Unit Tests (Required)

```python
def test_mark_complete_pending_task():
    """Verify marking pending task sets completed=True and updates timestamp."""

def test_mark_complete_already_completed():
    """Verify idempotent behavior when marking already-completed task."""

def test_mark_complete_nonexistent_task():
    """Verify error handling for task that doesn't exist."""

def test_unmark_complete_completed_task():
    """Verify reopening completed task sets completed=False and updates timestamp."""

def test_unmark_complete_already_pending():
    """Verify idempotent behavior when reopening already-pending task."""

def test_unmark_complete_nonexistent_task():
    """Verify error handling for task that doesn't exist."""

def test_mark_complete_preserves_other_fields():
    """Verify id, title, description, created_at unchanged after mark complete."""

def test_timestamp_accuracy():
    """Verify updated_at timestamp within ±1 second of operation time."""
```

### Property-Based Tests (Recommended)

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=1000))
def test_mark_unmark_roundtrip(task_id):
    """
    Verify mark -> unmark -> mark cycle preserves task state.

    Property: Completion status and timestamp should update,
    but all other fields remain identical.
    """
```

---

## Evolution Notes

### Phase II: File Persistence

**Changes**:
- Add file write after status update
- Implement transaction rollback on file write failure
- Return error if file write fails

### Phase III: REST API

**HTTP Endpoints**:
```
PATCH /tasks/{task_id}/complete   -> mark_complete()
PATCH /tasks/{task_id}/reopen     -> unmark_complete()

Response:
{
  "success": true,
  "message": "✓ Task 1 marked as complete",
  "task": { <updated task object> }
}
```

### Phase IV: Database Persistence

**Changes**:
- Wrap operations in database transactions
- Add optimistic locking check (version field)
- Return 409 Conflict on concurrent modification

---

## Contract Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-06 | Initial contract for Phase I in-memory implementation |

---

## Notes

- **Idempotency**: Both methods are safe to call multiple times with same arguments
- **Atomicity**: In Phase I, atomicity guaranteed by single-threaded Python execution
- **Performance**: O(n) search acceptable for Phase I; will optimize with indexing in Phase IV
