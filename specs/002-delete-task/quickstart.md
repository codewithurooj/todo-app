# Quick Start Guide: Delete Task Feature

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Audience**: Developers

---

## Overview

This guide provides instructions for testing and developing the Delete Task feature. The Delete feature extends the existing Add Task foundation (001-add-task).

---

## Prerequisites

Same as 001-add-task. See `specs/001-add-task/quickstart.md` for full setup instructions.

**Quick Check**:
```bash
# Verify environment
python --version  # Should be 3.13+
pytest --version  # Should be installed
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```

---

## Testing Delete Feature

### Run Delete-Specific Tests

```bash
# Run all delete feature tests
pytest tests/ -k delete -v

# Run delete unit tests only
pytest tests/unit/test_task_service.py::test_delete -v

# Run delete integration tests
pytest tests/integration/test_delete_task_flow.py -v

# Run delete contract tests
pytest tests/contract/test_delete_contract.py -v
```

### Test Delete Manually

```bash
# Run the application
python main.py

# Steps to test delete:
1. Select "1" to add a few tasks
2. Select "4" to view tasks (note the IDs)
3. Select "2" to delete a task
4. Enter a task ID
5. Confirm deletion (if prompted)
6. Verify task is removed
```

---

## Development Workflow for Delete

### TDD Cycle for Delete Operations

1. **RED - Write Failing Test**
   ```bash
   # Example: test delete non-existent task
   vim tests/unit/test_task_service.py

   # Add test:
   def test_delete_nonexistent_task():
       task_list = TaskList()
       success, msg = task_list.delete_task(999)
       assert success == False
       assert "not found" in msg

   # Run test (should fail)
   pytest tests/unit/test_task_service.py::test_delete_nonexistent_task -v
   ```

2. **GREEN - Implement Minimum Code**
   ```bash
   # Implement delete_task() method
   vim src/services/task_service.py

   # Run test (should pass)
   pytest tests/unit/test_task_service.py::test_delete_nonexistent_task -v
   ```

3. **REFACTOR - Improve Code**
   ```bash
   # Run all tests to ensure no regression
   pytest tests/ -v

   # Run linter and formatter
   ruff check src/
   black src/
   ```

---

## Common Delete Test Scenarios

### Test 1: Delete Existing Task

```python
def test_delete_existing_task():
    task_list = TaskList()
    task_list.add_task("Test task", None)
    
    success, msg = task_list.delete_task(1)
    
    assert success == True
    assert "deleted successfully" in msg
    assert len(task_list.get_all_tasks()) == 0
```

### Test 2: ID Preservation After Delete

```python
def test_id_preservation_after_delete():
    task_list = TaskList()
    task_list.add_task("Task 1", None)  # ID 1
    task_list.add_task("Task 2", None)  # ID 2
    task_list.add_task("Task 3", None)  # ID 3
    
    task_list.delete_task(2)  # Delete middle task
    
    remaining = task_list.get_all_tasks()
    assert [t.id for t in remaining] == [1, 3]  # IDs not renumbered
```

### Test 3: Deleted IDs Not Reused

```python
def test_deleted_ids_not_reused():
    task_list = TaskList()
    task_list.add_task("Task 1", None)  # ID 1
    task_list.delete_task(1)
    
    new_task = task_list.add_task("Task 2", None)
    assert new_task.id == 2  # Not 1
```

### Test 4: Validation Tests

```python
def test_validate_task_id_valid():
    valid, task_id, error = validate_task_id("42")
    assert valid == True
    assert task_id == 42
    assert error == ""

def test_validate_task_id_invalid():
    valid, task_id, error = validate_task_id("abc")
    assert valid == False
    assert task_id is None
    assert "numeric" in error.lower()
```

---

## Debugging Delete Issues

### Issue: Task Not Deleting

**Check**:
```bash
# Add debug print in delete_task()
vim src/services/task_service.py

def delete_task(self, task_id):
    print(f"DEBUG: Attempting to delete task {task_id}")
    print(f"DEBUG: Current tasks: {[t.id for t in self._tasks]}")
    ...
```

### Issue: IDs Being Renumbered

**Check**:
```bash
# Verify delete implementation uses filter, not mutation
# BAD: for loop with remove()
# GOOD: list comprehension
self._tasks = [t for t in self._tasks if t.id != task_id]
```

### Issue: Confirmation Not Working

**Check**:
```bash
# Test confirmation validation
pytest tests/unit/test_validators.py::test_validate_confirmation -v
```

---

## Code Coverage for Delete

```bash
# Run with coverage
pytest --cov=src/services/task_service.py tests/unit/test_task_service.py -v

# Generate HTML report
pytest --cov=src --cov-report=html tests/

# Open report
open htmlcov/index.html  # Linux/macOS
start htmlcov/index.html  # Windows
```

**Target Coverage for Delete Feature**:
- `delete_task()` method: 100%
- `validate_task_id()`: 100%
- `validate_confirmation()`: 100%
- Delete CLI flow: 90%+

---

## Integration with Existing Features

### Dependencies

Delete feature depends on:
- ✅ `Task` entity (from 001-add-task)
- ✅ `TaskList.get_task_by_id()` (from 001-add-task)
- ✅ `TaskList.get_all_tasks()` (from 001-add-task)

### No Impact On

Delete feature does NOT affect:
- Add task functionality
- Task entity structure
- ID generation for new tasks

---

## Next Steps

After Delete Task implementation:

1. **Run Full Test Suite**: `pytest tests/ --cov=src`
2. **Verify Coverage**: Ensure 90%+ coverage for delete code
3. **Manual Testing**: Test all edge cases in console
4. **Integration Test**: Combine add + delete + view operations
5. **Documentation**: Update README with delete instructions

---

## Quick Reference

```bash
# Test Commands
pytest tests/ -k delete -v              # All delete tests
pytest tests/unit/ -v                   # Unit tests
pytest tests/integration/ -v            # Integration tests

# Coverage
pytest --cov=src tests/ -v              # With coverage
pytest --cov-report=html tests/         # HTML report

# Code Quality
ruff check src/                         # Lint
black src/                              # Format
mypy src/                               # Type check

# Manual Testing
python main.py                          # Run app
```

---

**Status**: Development Guide Complete
**Last Updated**: 2025-12-06
