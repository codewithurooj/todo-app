# Data Model: Delete Task Feature

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Status**: Phase 1 - Design

---

## Overview

This document defines the data model extensions for the Delete Task feature. The Delete feature builds on the existing Task and TaskList entities from 001-add-task, adding delete operations while preserving all existing attributes and behaviors.

---

## 1. Task Entity

### Changes from 001-add-task

**No changes to Task entity**. The Task dataclass remains identical:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a single task in the todo application."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
```

### Deletion Behavior

**When a task is deleted**:
- Task is removed from TaskList collection
- Task ID is permanently retired (never reused)
- No cascade effects (Phase I has no relationships)
- Task object is garbage collected after removal

---

## 2. TaskList Collection

### Extended Operations

The TaskList class from 001-add-task is extended with delete operations:

```python
from typing import List, Optional

class TaskList:
    """In-memory collection of tasks with ID management."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    # EXISTING methods from 001-add-task (no changes):
    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and add a new task."""
        ...

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        ...

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID."""
        ...

    # NEW method for delete feature:
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was deleted, False if not found

        Side Effects:
            - Removes task from _tasks list
            - Does NOT decrement _next_id
            - Reduces list size by 1

        Guarantees:
            - Remaining tasks preserve their IDs
            - Remaining tasks maintain original order
            - Deleted ID is never reused
        """
        original_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        return len(self._tasks) < original_len
```

### New Invariants

In addition to invariants from 001-add-task:

1. **ID Monotonicity**: `_next_id` never decrements, even after deletion
2. **ID Uniqueness After Deletion**: Deleted IDs are permanently retired
3. **Order Preservation**: Remaining tasks maintain their original order
4. **Size Consistency**: After deleting N tasks, list size decreases by N

### State Transitions

```
Task exists in list → delete_task(id) called → Task removed from list
                                           → Deleted ID retired forever
```

**Critical**: The `_next_id` counter is never affected by deletion. If tasks 1-5 are created and task 3 is deleted, the next task created will still be ID 6, not ID 3.

---

## 3. Validation Model

### New Validator: Task ID Validation

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | None, str]:
    """
    Validate task ID input for delete operations.

    Args:
        task_id_str: User input string for task ID

    Returns:
        (True, task_id, "") if valid
        (False, None, error_message) if invalid

    Validation Rules:
        1. Must not be empty
        2. Must be numeric (parseable as int)
        3. Must be positive (>= 1)
        4. Leading zeros are acceptable ("007" → 7)
    """
    if not task_id_str:
        return False, None, "Error: Task ID cannot be empty"

    if task_id_str.lower() == 'cancel':
        return False, None, "CANCEL"  # Special case for cancellation

    try:
        task_id = int(task_id_str)
        if task_id < 1:
            return False, None, "Error: Task ID must be a positive number"
        return True, task_id, ""
    except ValueError:
        return False, None, "Error: Invalid task ID. Please enter a numeric ID"
```

### Error Messages

| Validation Failure | Error Message | User Action |
|-------------------|---------------|-------------|
| Empty input | "Error: Task ID cannot be empty" | Enter a task ID |
| Non-numeric | "Error: Invalid task ID. Please enter a numeric ID" | Enter numbers only |
| Negative/zero | "Error: Task ID must be a positive number" | Enter positive number |
| Task not found | "Error: Task #[ID] not found" | Verify task exists, check ID |

---

## 4. State Management

### Deletion State Flow

```
User selects "Delete Task"
    ↓
Empty list check → If empty: Show "No tasks available" → Return to menu
    ↓
Prompt for task ID
    ↓
Validate ID (numeric, positive)
    ↓
    ├─ Invalid → Show error → Re-prompt
    ├─ "cancel" → Cancel operation → Return to menu
    └─ Valid
        ↓
    Lookup task by ID
        ↓
        ├─ Not found → Show "Task not found" error → Return to menu
        └─ Found
            ↓
        Confirmation prompt (P3 optional)
            ↓
            ├─ No/cancel → Cancel deletion → Return to menu
            └─ Yes
                ↓
            Delete from TaskList
                ↓
            Show success message → Return to menu
```

### Edge Case Handling

**Scenario: Delete last remaining task**
```python
# Before: [Task(id=1)]
task_list.delete_task(1)
# After: []
# get_all_tasks() returns empty list
# Next task created will have ID=2
```

**Scenario: Delete from middle**
```python
# Before: [Task(id=1), Task(id=2), Task(id=3)]
task_list.delete_task(2)
# After: [Task(id=1), Task(id=3)]
# IDs preserved: 1 and 3, not renumbered to 1 and 2
```

**Scenario: Attempt to delete already-deleted task**
```python
task_list.delete_task(5)  # Returns True, task deleted
task_list.delete_task(5)  # Returns False, task not found
# Second deletion is safe, returns False without error
```

---

## 5. Performance Considerations

### Delete Operation Complexity

- **Time Complexity**: O(n) where n = number of tasks
  - List comprehension iterates through all tasks
  - Acceptable for Phase I target of ~1000 tasks
- **Space Complexity**: O(n) for creating new filtered list
  - Python list comprehension creates new list
  - Original list is garbage collected

### Performance Targets (from research.md)

- **Delete operation**: < 1 second
- **Validation overhead**: < 100ms
- **Support scale**: 1000+ tasks without degradation

**Actual Performance** (estimated for 1000 tasks):
- List comprehension: ~0.1ms for 1000 items
- ID validation: ~0.01ms
- Total operation: < 1ms (well under 1 second target)

---

## 6. Evolution Path

### Phase I → Phase II (File Persistence)

**Changes Required**:
- After `delete_task()`, write updated list to JSON file
- No changes to delete logic itself
- Persist `_next_id` to ensure deleted IDs stay retired

**Example JSON after deletion**:
```json
{
  "tasks": [
    {"id": 1, "title": "Task 1", ...},
    {"id": 3, "title": "Task 3", ...}
  ],
  "next_id": 4
}
```
Note: Task #2 was deleted, ID skipped.

### Phase II → Phase IV (Database)

**SQL DELETE Operation**:
```sql
DELETE FROM tasks WHERE id = ?
```

**ORM (SQLAlchemy)**:
```python
session.query(TaskModel).filter(TaskModel.id == task_id).delete()
session.commit()
```

**ID Management**: Database sequence or autoincrement continues from last value, deleted IDs not reused (standard SQL behavior).

---

## 7. Testing Considerations

### Unit Test Coverage

**TaskList.delete_task() method**:
- Delete existing task returns True
- Delete non-existent task returns False
- Delete from list of 1 leaves empty list
- Delete from middle preserves order
- Delete doesn't affect _next_id counter
- Multiple deletions work correctly

**Validator: validate_task_id()**:
- Empty string rejected
- Non-numeric string rejected
- Negative number rejected
- Zero rejected
- Positive number accepted
- Leading zeros handled ("007" → 7)
- "cancel" returns special code

### Integration Test Coverage

- End-to-end delete flow with confirmation
- Cancel at ID prompt
- Cancel at confirmation prompt
- Empty list handling
- Non-existent ID error display

---

## Summary

| Component | Changes from 001-add-task | Evolution Ready |
|-----------|---------------------------|-----------------|
| Task Entity | None | ✅ Same as 001 |
| TaskList | Added `delete_task()` method | ✅ Maps to DELETE in SQL |
| Validation | Added `validate_task_id()` | ✅ Reusable for update/mark |
| IDs | Deleted IDs never reused | ✅ Consistent with DB behavior |
| Performance | O(n) delete acceptable | ⚠️ Phase IV needs indexes |

---

**Status**: Phase 1 Design Complete
**Next**: Generate contracts and quickstart documentation
