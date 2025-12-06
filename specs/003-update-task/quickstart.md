# Quick Start Guide: Update Task Feature

**Feature**: 003-update-task
**Audience**: Developers

## Prerequisites

Same as 001-add-task. See `specs/001-add-task/quickstart.md`.

## Testing Update Feature

```bash
# All update tests
pytest tests/ -k update -v

# Update unit tests
pytest tests/unit/test_task_service.py::test_update -v

# Update integration tests
pytest tests/integration/test_update_task_flow.py -v
```

## Manual Testing

```bash
python main.py

# Test update:
1. Add tasks (option 1)
2. View tasks (option 4)  
3. Update task (option 3)
4. Enter task ID
5. Choose field to update
6. Enter new value
7. Verify change
```

## Common Test Scenarios

```python
def test_update_title():
    task_list = TaskList()
    task_list.add_task("Old title", None)
    
    success, msg = task_list.update_task_title(1, "New title")
    
    assert success == True
    task = task_list.get_task_by_id(1)
    assert task.title == "New title"

def test_preserve_other_fields():
    task_list = TaskList()
    task = task_list.add_task("Title", "Desc")
    original_id = task.id
    original_time = task.created_at
    
    task_list.update_task_title(1, "New Title")
    
    task = task_list.get_task_by_id(1)
    assert task.id == original_id
    assert task.created_at == original_time
    assert task.description == "Desc"  # Unchanged

def test_toggle_status():
    task_list = TaskList()
    task_list.add_task("Task", None)
    
    # Toggle to complete
    success, msg = task_list.update_task_status(1)
    task = task_list.get_task_by_id(1)
    assert task.completed == True
    
    # Toggle back to incomplete
    task_list.update_task_status(1)
    task = task_list.get_task_by_id(1)
    assert task.completed == False
```

## Debugging Issues

**Issue**: Fields not updating
```bash
# Check object reference
print(f"Task ID: {task.id}, Title: {task.title}")
```

**Issue**: Validation failing
```bash
# Test validators directly
from utils.validators import validate_title
valid, error = validate_title("test")
print(f"Valid: {valid}, Error: {error}")
```

## Integration with Existing Features

**Dependencies**: Reuses validate_title(), validate_description() from 001-add-task

**No Impact On**: Add, delete, view features

## Quick Reference

```bash
pytest tests/ -k update -v          # All update tests
pytest --cov=src tests/ -v          # With coverage
ruff check src/                     # Lint
python main.py                      # Run app
```

**Status**: Development Guide Complete
