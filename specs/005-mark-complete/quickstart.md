# Developer Quickstart: Mark Task Complete Feature

**Feature**: 005-mark-complete
**Created**: 2025-12-06
**Purpose**: Get developers up to speed on implementing the Mark Complete feature

---

## Overview

This feature adds completion status operations to the todo app, allowing users to mark tasks as complete and reopen them. Implementation extends existing Task and TaskList classes from 001-add-task.

**Key Additions**:
- `TaskList.mark_complete(task_id)` method
- `TaskList.unmark_complete(task_id)` method
- CLI menu options for mark complete and reopen
- Completion status validation logic

---

## Prerequisites

Before implementing this feature, ensure:
1. **Feature 001-add-task** is complete (provides Task and TaskList)
2. **Feature 004-view-task** is complete (provides completion status display)
3. Python 3.13+ installed with `datetime.UTC` support
4. pytest testing framework set up

---

## Quick Implementation Checklist

```
Phase 0: Setup & Research
☐ Read spec.md for requirements
☐ Review research.md for technical decisions
☐ Study data-model.md for entity extensions
☐ Review contracts/ for API definitions

Phase 1: TDD - Write Tests (Red)
☐ Write unit tests for TaskList.mark_complete()
☐ Write unit tests for TaskList.unmark_complete()
☐ Write validation tests
☐ Write CLI handler tests
☐ Run tests - verify all FAIL (red phase)

Phase 2: Implementation (Green)
☐ Add mark_complete() method to TaskList
☐ Add unmark_complete() method to TaskList
☐ Create validation functions
☐ Add CLI menu options (5 and 6)
☐ Add CLI handlers
☐ Run tests - verify all PASS (green phase)

Phase 3: Refactor
☐ Extract common validation logic
☐ Improve error messages
☐ Add docstrings and type hints
☐ Run tests - verify still PASS

Phase 4: Integration
☐ Test with existing features (add, view, update, delete)
☐ Verify completion status displays in view tasks
☐ Test edge cases from spec
☐ Manual testing in console
```

---

## File Structure

```
src/
├── models/
│   ├── task.py           # Task entity (from 001-add-task, no changes)
│   └── tasklist.py       # TaskList class (EXTEND with mark_complete methods)
├── services/
│   └── validation.py     # Validation functions (NEW for this feature)
└── cli/
    ├── menu.py           # Main menu (UPDATE with options 5 & 6)
    └── handlers.py       # CLI handlers (ADD mark_complete and reopen handlers)

tests/
├── unit/
│   ├── test_tasklist_completion.py    # NEW - mark_complete/unmark tests
│   └── test_validation.py             # NEW - validation tests
└── integration/
    └── test_cli_mark_complete.py      # NEW - CLI workflow tests
```

---

## Step-by-Step Implementation Guide

### Step 1: Write Tests First (TDD Red Phase)

Create `tests/unit/test_tasklist_completion.py`:

```python
import pytest
from datetime import datetime, UTC, timedelta
from src.models.task import Task
from src.models.tasklist import TaskList

class TestMarkComplete:
    """Tests for TaskList.mark_complete() method."""

    def test_mark_pending_task_as_complete(self):
        """Verify marking pending task sets completed=True and updates timestamp."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")
        before_time = datetime.now(UTC)

        # Act
        success, message = task_list.mark_complete(1)

        # Assert
        assert success is True
        assert "marked as complete" in message
        task = task_list.find_by_id(1)
        assert task.completed is True
        assert task.updated_at >= before_time

    def test_mark_already_completed_task_idempotent(self):
        """Verify marking already-completed task returns success with warning."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")
        task_list.mark_complete(1)

        # Act
        success, message = task_list.mark_complete(1)

        # Assert
        assert success is True
        assert "already completed" in message

    def test_mark_nonexistent_task_returns_error(self):
        """Verify marking non-existent task returns error."""
        # Arrange
        task_list = TaskList()

        # Act
        success, message = task_list.mark_complete(999)

        # Assert
        assert success is False
        assert "not found" in message
        assert "999" in message

    def test_mark_complete_preserves_immutable_fields(self):
        """Verify id, title, description, created_at unchanged."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")
        task_before = task_list.find_by_id(1)
        id_before = task_before.id
        title_before = task_before.title
        desc_before = task_before.description
        created_before = task_before.created_at

        # Act
        task_list.mark_complete(1)

        # Assert
        task_after = task_list.find_by_id(1)
        assert task_after.id == id_before
        assert task_after.title == title_before
        assert task_after.description == desc_before
        assert task_after.created_at == created_before

    def test_timestamp_accuracy_within_one_second(self):
        """Verify updated_at within ±1 second of operation (SC-003)."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")
        operation_time = datetime.now(UTC)

        # Act
        task_list.mark_complete(1)

        # Assert
        task = task_list.find_by_id(1)
        diff = abs((task.updated_at - operation_time).total_seconds())
        assert diff <= 1.0, f"Timestamp diff {diff}s exceeds 1s tolerance"


class TestUnmarkComplete:
    """Tests for TaskList.unmark_complete() method."""

    def test_unmark_completed_task_to_reopen(self):
        """Verify reopening completed task sets completed=False."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")
        task_list.mark_complete(1)

        # Act
        success, message = task_list.unmark_complete(1)

        # Assert
        assert success is True
        assert "reopened" in message or "pending" in message
        task = task_list.find_by_id(1)
        assert task.completed is False

    def test_unmark_already_pending_task_idempotent(self):
        """Verify unmarking already-pending task returns success with warning."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")

        # Act
        success, message = task_list.unmark_complete(1)

        # Assert
        assert success is True
        assert "already pending" in message

    def test_unmark_nonexistent_task_returns_error(self):
        """Verify unmarking non-existent task returns error."""
        # Arrange
        task_list = TaskList()

        # Act
        success, message = task_list.unmark_complete(999)

        # Assert
        assert success is False
        assert "not found" in message


class TestRapidToggle:
    """Test rapid completion status toggles (Edge Case 2)."""

    def test_multiple_toggle_operations_succeed(self):
        """Verify rapid mark/unmark/mark operations all succeed."""
        # Arrange
        task_list = TaskList()
        task_list.add("Buy groceries", "Milk, eggs, bread")

        # Act & Assert - Each operation should succeed
        success, _ = task_list.mark_complete(1)
        assert success is True

        success, _ = task_list.unmark_complete(1)
        assert success is True

        success, _ = task_list.mark_complete(1)
        assert success is True

        # Final state should be completed
        task = task_list.find_by_id(1)
        assert task.completed is True
```

Run tests: `pytest tests/unit/test_tasklist_completion.py -v`

**Expected**: All tests FAIL (red phase) because methods don't exist yet.

---

### Step 2: Implement TaskList Methods (Green Phase)

Update `src/models/tasklist.py`:

```python
from typing import Optional, Tuple
from datetime import datetime, UTC

class TaskList:
    """Collection of tasks with CRUD + completion operations."""

    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    # ... existing methods (add, delete, update, view, find_by_id) ...

    def mark_complete(self, task_id: int) -> Tuple[bool, str]:
        """
        Mark a pending task as complete.

        Args:
            task_id: ID of task to mark complete

        Returns:
            Tuple of (success: bool, message: str)
        """
        task = self.find_by_id(task_id)

        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        if task.completed:
            return (True, f"Task {task_id} is already completed")

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
        """
        task = self.find_by_id(task_id)

        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        if not task.completed:
            return (True, f"Task {task_id} is already pending")

        task.completed = False
        task.updated_at = datetime.now(UTC)

        return (True, f"✓ Task {task_id} reopened (marked as pending)")
```

Run tests: `pytest tests/unit/test_tasklist_completion.py -v`

**Expected**: All tests PASS (green phase).

---

### Step 3: Add CLI Handlers

Create `src/cli/handlers.py` (or extend existing):

```python
from src.models.tasklist import TaskList

def handle_mark_complete(task_list: TaskList) -> None:
    """Handle marking task as complete."""
    print("\n--- Mark Task Complete ---")

    user_input = input("Enter task ID to mark as complete: ")

    try:
        task_id = int(user_input.strip())
        if task_id < 1:
            print("Task ID must be a positive integer")
            return
    except ValueError:
        print("Invalid input. Please enter a valid task ID (number)")
        return

    success, message = task_list.mark_complete(task_id)
    print(message)


def handle_reopen_task(task_list: TaskList) -> None:
    """Handle reopening completed task."""
    print("\n--- Reopen Completed Task ---")

    user_input = input("Enter task ID to reopen: ")

    try:
        task_id = int(user_input.strip())
        if task_id < 1:
            print("Task ID must be a positive integer")
            return
    except ValueError:
        print("Invalid input. Please enter a valid task ID (number)")
        return

    success, message = task_list.unmark_complete(task_id)
    print(message)
```

---

### Step 4: Update Main Menu

Update `src/cli/menu.py`:

```python
def display_main_menu() -> None:
    """Display main menu options."""
    print("\n=== Todo App - Main Menu ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")      # NEW
    print("6. Reopen Completed Task")   # NEW
    print("7. Exit")
    print("="*30)


def handle_menu_selection(choice: str, task_list: TaskList) -> bool:
    """Handle user menu selection. Returns True to continue, False to exit."""
    if choice == "1":
        handle_add_task(task_list)
    elif choice == "2":
        handle_view_tasks(task_list)
    elif choice == "3":
        handle_update_task(task_list)
    elif choice == "4":
        handle_delete_task(task_list)
    elif choice == "5":
        handle_mark_complete(task_list)     # NEW
    elif choice == "6":
        handle_reopen_task(task_list)       # NEW
    elif choice == "7":
        print("Goodbye!")
        return False
    else:
        print("Invalid choice. Please try again.")

    return True
```

---

### Step 5: Integration Testing

Create `tests/integration/test_cli_mark_complete.py`:

```python
import pytest
from src.models.tasklist import TaskList
from src.cli.handlers import handle_mark_complete, handle_reopen_task

def test_full_mark_complete_workflow(monkeypatch, capsys):
    """Integration test: Add task -> Mark complete -> Verify status."""
    # Arrange
    task_list = TaskList()
    task_list.add("Buy groceries", "Milk, eggs, bread")

    # Simulate user input: task ID = 1
    monkeypatch.setattr('builtins.input', lambda _: "1")

    # Act
    handle_mark_complete(task_list)

    # Assert
    captured = capsys.readouterr()
    assert "marked as complete" in captured.out
    task = task_list.find_by_id(1)
    assert task.completed is True


def test_full_reopen_workflow(monkeypatch, capsys):
    """Integration test: Add -> Complete -> Reopen -> Verify."""
    # Arrange
    task_list = TaskList()
    task_list.add("Buy groceries", "Milk, eggs, bread")
    task_list.mark_complete(1)

    # Simulate user input: task ID = 1
    monkeypatch.setattr('builtins.input', lambda _: "1")

    # Act
    handle_reopen_task(task_list)

    # Assert
    captured = capsys.readouterr()
    assert "reopened" in captured.out or "pending" in captured.out
    task = task_list.find_by_id(1)
    assert task.completed is False
```

---

## Running the Complete Test Suite

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_tasklist_completion.py -v

# Run tests matching pattern
pytest tests/ -k "mark_complete" -v
```

---

## Manual Testing Checklist

```
☐ Start app: python src/main.py
☐ Add task (option 1)
☐ View tasks (option 2) - verify task shows as pending
☐ Mark complete (option 5) - verify confirmation message
☐ View tasks (option 2) - verify task shows "[✓] Completed"
☐ Mark complete again (option 5) - verify idempotent message
☐ Reopen task (option 6) - verify confirmation message
☐ View tasks (option 2) - verify task shows as pending again
☐ Try invalid task ID - verify error message
☐ Try non-numeric input - verify error message
```

---

## Common Issues & Solutions

### Issue: Tests fail with "module not found"

**Solution**: Ensure PYTHONPATH includes project root:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Timestamp tests fail intermittently

**Solution**: Use tolerance in assertions:
```python
assert abs((actual - expected).total_seconds()) <= 1.0
```

### Issue: Task entity missing completed field

**Solution**: Ensure you're using Task from 001-add-task which includes:
```python
@dataclass
class Task:
    # ... other fields ...
    completed: bool = False
```

---

## Next Steps After Implementation

1. **Code Review**: Verify code follows constitution principles (PEP 8, type hints, docstrings)
2. **Manual Testing**: Complete manual testing checklist above
3. **Documentation**: Update main README.md with new menu options
4. **Git Workflow**: Create commit with conventional format: `feat(005-mark-complete): add mark complete operations`
5. **Pull Request**: Create PR referencing spec and linking to planning artifacts

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `spec.md` | Requirements and acceptance criteria |
| `research.md` | Technical decisions and rationale |
| `data-model.md` | Entity definitions and state machines |
| `contracts/tasklist_completion_methods.md` | TaskList method contracts |
| `contracts/cli_mark_complete_handler.md` | CLI handler contracts |
| `contracts/completion_validation.md` | Validation function contracts |

---

## Performance Targets (Phase I)

- ✅ Status changes complete within 1 second (SC-001)
- ✅ O(n) complexity acceptable for in-memory list
- ✅ No optimization needed for Phase I

**Future Optimization** (Phase IV):
- Add index on `completed` field for filtering
- Use hash map for O(1) task lookup by ID

---

## Success Criteria Checklist

From spec.md:

- ☐ SC-001: Status changes complete within 1 second
- ☐ SC-002: 100% of valid operations update status correctly
- ☐ SC-003: Timestamps accurate within ±1 second
- ☐ SC-004: 100% of invalid inputs caught with appropriate errors
- ☐ SC-005: 0 unintended field modifications during status changes
- ☐ SC-006: 100% of users understand messages
- ☐ SC-007: 0 crashes during 1000 operations
- ☐ SC-008: Users can manage task lifecycle without friction

---

## Questions?

- Review `spec.md` for requirements clarification
- Check `data-model.md` for entity structure
- See `contracts/` for detailed API specifications
- Refer to constitution.md for coding standards
