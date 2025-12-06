# Data Model: Mark Task Complete Feature

**Feature**: 005-mark-complete
**Created**: 2025-12-06
**Purpose**: Define data structures, validation rules, and state transitions for mark complete operations

---

## Overview

This feature extends the existing Task entity (from 001-add-task) with completion status operations. No new entities are introduced - only new methods on TaskList to modify the `completed` field.

**Principle**: Minimal data model changes. Reuse existing structures per Evolutionary Architecture principle.

---

## Entities

### Task (Extended from 001-add-task)

**Source**: Defined in `001-add-task/data-model.md`, extended here with completion semantics

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """
    Represents a single todo task.

    Extended by 005-mark-complete to include completion status semantics.
    """
    id: int                    # Unique identifier (immutable)
    title: str                 # Task summary (immutable by this feature)
    description: str           # Detailed description (immutable by this feature)
    created_at: datetime       # Creation timestamp (immutable)
    updated_at: datetime       # Last modification timestamp (MODIFIED by mark complete)
    completed: bool = False    # Completion status (MODIFIED by mark complete)

    def __post_init__(self):
        """Validate task data on creation."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if self.id < 1:
            raise ValueError("Task ID must be positive integer")
```

**Field Semantics**:

| Field | Type | Mutability (this feature) | Validation |
|-------|------|--------------------------|------------|
| `id` | int | Immutable | Must be positive integer |
| `title` | str | Immutable | Non-empty after strip() |
| `description` | str | Immutable | Any string (can be empty) |
| `created_at` | datetime | Immutable | UTC timezone, ISO 8601 |
| `updated_at` | datetime | **Mutable** | UTC timezone, auto-updated on status change |
| `completed` | bool | **Mutable** | True (completed) or False (pending) |

**Constraints** (from spec FR-011):
- Mark complete operations MUST NOT modify: `id`, `title`, `description`, `created_at`
- Mark complete operations MUST modify: `completed`, `updated_at`

---

### TaskList (Extended from 001-add-task)

**Source**: Defined in `001-add-task/data-model.md`, extended here with mark complete methods

```python
from typing import Optional, Tuple
from datetime import datetime, UTC

class TaskList:
    """
    Collection of tasks with CRUD + completion operations.

    Extended by 005-mark-complete with mark_complete() and unmark_complete() methods.
    """

    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    # ... existing methods from 001-add-task (add, delete, update, find) ...

    def mark_complete(self, task_id: int) -> Tuple[bool, str]:
        """
        Mark a pending task as complete.

        Args:
            task_id: ID of task to mark complete

        Returns:
            Tuple of (success: bool, message: str)
            - (True, msg) on success or if already completed (idempotent)
            - (False, msg) on error (task not found)

        Validates:
            - Task with task_id exists (FR-004)
            - Current completion status (FR-005 - idempotent behavior)

        Side Effects:
            - Sets task.completed = True
            - Updates task.updated_at to current UTC time (FR-003)
            - Preserves all other fields (FR-011)

        Examples:
            >>> task_list.mark_complete(1)
            (True, "✓ Task 1 marked as complete")

            >>> task_list.mark_complete(1)  # Already complete
            (True, "Task 1 is already completed")

            >>> task_list.mark_complete(999)  # Not found
            (False, "Error: Task with ID 999 not found")
        """
        task = self.find_by_id(task_id)

        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        if task.completed:
            # Idempotent: Already completed, but not an error
            return (True, f"Task {task_id} is already completed")

        # Atomic update (FR-012)
        task.completed = True
        task.updated_at = datetime.now(UTC)

        return (True, f"✓ Task {task_id} marked as complete")

    def unmark_complete(self, task_id: int) -> Tuple[bool, str]:
        """
        Reopen a completed task (change status to pending).

        Args:
            task_id: ID of task to reopen

        Returns:
            Tuple of (success: bool, message: str)
            - (True, msg) on success or if already pending (idempotent)
            - (False, msg) on error (task not found)

        Validates:
            - Task with task_id exists (FR-004)
            - Current completion status (FR-005 - idempotent behavior)

        Side Effects:
            - Sets task.completed = False
            - Updates task.updated_at to current UTC time (FR-003)
            - Preserves all other fields (FR-011)

        Examples:
            >>> task_list.unmark_complete(1)
            (True, "✓ Task 1 reopened (marked as pending)")

            >>> task_list.unmark_complete(1)  # Already pending
            (True, "Task 1 is already pending")

            >>> task_list.unmark_complete(999)  # Not found
            (False, "Error: Task with ID 999 not found")
        """
        task = self.find_by_id(task_id)

        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        if not task.completed:
            # Idempotent: Already pending, but not an error
            return (True, f"Task {task_id} is already pending")

        # Atomic update (FR-012)
        task.completed = False
        task.updated_at = datetime.now(UTC)

        return (True, f"✓ Task {task_id} reopened (marked as pending)")

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
```

---

## State Transitions

### Completion Status State Machine

```
┌─────────┐                                 ┌───────────┐
│ Pending │  ──── mark_complete() ────────> │ Completed │
│         │                                  │           │
│         │ <──── unmark_complete() ─────── │           │
└─────────┘                                 └───────────┘

States:
- Pending: completed = False (default state on task creation)
- Completed: completed = True

Transitions:
- mark_complete(): Pending → Completed
- unmark_complete(): Completed → Pending

Idempotent Operations:
- mark_complete() on Completed → No state change, returns success with warning
- unmark_complete() on Pending → No state change, returns success with warning
```

**Invariants**:
1. Task always in exactly one state (Pending or Completed)
2. Transitions always update `updated_at` timestamp
3. Transitions never modify other fields

---

## Validation Rules

### Input Validation

**Task ID Validation** (FR-004):
```python
def validate_task_id(task_id: int, task_list: TaskList) -> Tuple[bool, str]:
    """
    Validate task ID before status operations.

    Rules:
    - task_id must be positive integer
    - task_id must exist in task list

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if not isinstance(task_id, int):
        return (False, "Task ID must be an integer")

    if task_id < 1:
        return (False, "Task ID must be a positive integer")

    if task_list.find_by_id(task_id) is None:
        return (False, f"Error: Task with ID {task_id} not found")

    return (True, "")
```

### State Validation

**Status Check** (FR-005):
```python
def validate_mark_complete_precondition(task: Task) -> Tuple[bool, str]:
    """
    Check if task can be marked complete.

    This is an idempotent check - returns True even if already completed,
    but provides informative message.

    Returns:
        (True, "") if can mark complete
        (True, warning_msg) if already completed (idempotent)
    """
    if task.completed:
        return (True, f"Task {task.id} is already completed")
    return (True, "")

def validate_unmark_complete_precondition(task: Task) -> Tuple[bool, str]:
    """
    Check if task can be reopened.

    This is an idempotent check - returns True even if already pending,
    but provides informative message.

    Returns:
        (True, "") if can reopen
        (True, warning_msg) if already pending (idempotent)
    """
    if not task.completed:
        return (True, f"Task {task.id} is already pending")
    return (True, "")
```

---

## Data Integrity Rules

### Atomic Updates (FR-012)

Operations MUST be atomic - either all changes succeed or none apply:

```python
def mark_complete(self, task_id: int) -> Tuple[bool, str]:
    """Atomic operation: both completed and updated_at change together."""
    task = self.find_by_id(task_id)

    if task is None:
        return (False, f"Error: Task with ID {task_id} not found")

    if task.completed:
        return (True, f"Task {task_id} is already completed")

    # Atomic: both fields update in single operation (in-memory)
    # Phase II+: Will require transaction management for file/DB persistence
    task.completed = True
    task.updated_at = datetime.now(UTC)

    return (True, f"✓ Task {task_id} marked as complete")
```

**Phase I Implementation**: Atomicity guaranteed by Python's in-memory execution (single-threaded)

**Phase IV+ Requirement**: Database transactions required for atomicity across persistence layers

### Field Immutability (FR-011)

The following fields MUST remain unchanged during mark complete operations:

```python
# Example validation (could be added to tests)
def verify_field_preservation(before: Task, after: Task) -> bool:
    """
    Verify that immutable fields were not changed.

    Returns True if all immutable fields preserved.
    """
    return (
        before.id == after.id and
        before.title == after.title and
        before.description == after.description and
        before.created_at == after.created_at
    )
```

---

## Evolution Notes

### Phase II: File Persistence

**Changes Required**:
- Add file I/O after status updates
- Implement rollback on file write failure
- Add file-level locking for atomicity

### Phase IV: Database Persistence

**Changes Required**:
- Wrap mark_complete/unmark_complete in database transactions
- Add optimistic locking (version field) for concurrent updates
- Create indices on `completed` field for filtering queries

### Phase V: Event-Driven Architecture

**Changes Required**:
- Emit `TaskCompletedEvent` and `TaskReopenedEvent`
- Support event replay for audit history
- Add event sourcing for completion status timeline

---

## Summary

**Entities Modified**: Task (extended), TaskList (extended)

**New Methods**:
- `TaskList.mark_complete(task_id: int) -> Tuple[bool, str]`
- `TaskList.unmark_complete(task_id: int) -> Tuple[bool, str]`

**Fields Modified**: `Task.completed`, `Task.updated_at`

**Validation Rules**: Task ID existence, status check (idempotent)

**State Transitions**: Pending ↔ Completed (reversible, idempotent)

**Constitutional Compliance**: ✅ Simplicity First, Evolutionary Architecture
