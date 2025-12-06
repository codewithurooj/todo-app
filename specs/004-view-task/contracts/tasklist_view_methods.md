# Contract: TaskList View Query Methods

**Feature**: 004-view-task
**Component**: TaskList (model)
**Purpose**: Define contracts for read-only query methods added to TaskList

---

## Method: `get_all_tasks()`

### Contract

**Purpose**: Retrieve all tasks for display purposes.

**Input**: None

**Output**: `list[Task]`
- Always returns a list (never None)
- List may be empty if no tasks exist
- Tasks are sorted by ID in ascending order (1, 2, 3, ...)
- Returns references to original Task objects (not copies)

**Side Effects**: None (read-only operation)

**Exceptions**: None

**Performance**: O(n log n) due to sorting (acceptable for Phase I scale)

### Test Cases

```python
def test_get_all_tasks_empty_list():
    """Given empty TaskList, when get_all_tasks called, then returns empty list."""
    tasklist = TaskList()
    result = tasklist.get_all_tasks()
    assert result == []
    assert isinstance(result, list)

def test_get_all_tasks_single_task():
    """Given TaskList with 1 task, when get_all_tasks called, then returns list with 1 task."""
    tasklist = TaskList()
    task = tasklist.add_task("Test", "Description")
    result = tasklist.get_all_tasks()
    assert len(result) == 1
    assert result[0].id == task.id

def test_get_all_tasks_sorted_by_id():
    """Given TaskList with multiple tasks, when get_all_tasks called, then tasks sorted by ID ascending."""
    tasklist = TaskList()
    task1 = tasklist.add_task("First", "")
    task2 = tasklist.add_task("Second", "")
    task3 = tasklist.add_task("Third", "")
    result = tasklist.get_all_tasks()
    assert result[0].id == task1.id
    assert result[1].id == task2.id
    assert result[2].id == task3.id

def test_get_all_tasks_sorted_after_deletion():
    """Given tasks with IDs 1,2,3,4,5 and ID 3 deleted, when get_all_tasks called, then returns [1,2,4,5]."""
    tasklist = TaskList()
    for i in range(5):
        tasklist.add_task(f"Task {i+1}", "")
    tasklist.delete_task(3)
    result = tasklist.get_all_tasks()
    ids = [t.id for t in result]
    assert ids == [1, 2, 4, 5]

def test_get_all_tasks_mixed_status():
    """Given tasks with mixed completion status, when get_all_tasks called, then returns all tasks regardless of status."""
    tasklist = TaskList()
    task1 = tasklist.add_task("Pending", "")
    task2 = tasklist.add_task("Completed", "")
    task2.completed = True
    result = tasklist.get_all_tasks()
    assert len(result) == 2
```

---

## Method: `get_task_by_id()`

### Contract

**Purpose**: Retrieve a specific task by its unique ID.

**Input**: `task_id: int`
- Expected to be a positive integer
- No format validation (caller's responsibility)

**Output**: `Task | None`
- Returns Task object if task with matching ID exists
- Returns None if task_id not found
- Returns reference to original Task object (not a copy)

**Side Effects**: None (read-only operation)

**Exceptions**: None (returns None for not found, doesn't validate input)

**Performance**: O(n) linear search (acceptable for Phase I scale)

### Test Cases

```python
def test_get_task_by_id_found():
    """Given TaskList with task ID 5, when get_task_by_id(5) called, then returns the task."""
    tasklist = TaskList()
    task = tasklist.add_task("Test", "Description")
    result = tasklist.get_task_by_id(task.id)
    assert result is not None
    assert result.id == task.id
    assert result.title == "Test"

def test_get_task_by_id_not_found():
    """Given TaskList with tasks 1,2,3, when get_task_by_id(99) called, then returns None."""
    tasklist = TaskList()
    tasklist.add_task("Task 1", "")
    tasklist.add_task("Task 2", "")
    result = tasklist.get_task_by_id(99)
    assert result is None

def test_get_task_by_id_empty_list():
    """Given empty TaskList, when get_task_by_id(1) called, then returns None."""
    tasklist = TaskList()
    result = tasklist.get_task_by_id(1)
    assert result is None

def test_get_task_by_id_after_deletion():
    """Given task ID 5 deleted, when get_task_by_id(5) called, then returns None."""
    tasklist = TaskList()
    task = tasklist.add_task("Test", "")
    task_id = task.id
    tasklist.delete_task(task_id)
    result = tasklist.get_task_by_id(task_id)
    assert result is None

def test_get_task_by_id_invalid_input():
    """Given invalid task_id inputs, method returns None without crashing."""
    tasklist = TaskList()
    # Note: Input validation is caller's responsibility, but method should handle gracefully
    assert tasklist.get_task_by_id(0) is None
    assert tasklist.get_task_by_id(-1) is None
```

---

## Method: `filter_tasks_by_status()`

### Contract

**Purpose**: Retrieve tasks filtered by completion status.

**Input**: `completed: bool`
- True: return only completed tasks
- False: return only pending tasks

**Output**: `list[Task]`
- Always returns a list (never None)
- List may be empty if no tasks match the filter
- Tasks are sorted by ID in ascending order
- Returns references to original Task objects (not copies)

**Side Effects**: None (read-only operation)

**Exceptions**: None

**Performance**: O(n log n) due to filtering + sorting (acceptable for Phase I scale)

### Test Cases

```python
def test_filter_pending_tasks():
    """Given 3 pending and 2 completed tasks, when filter_tasks_by_status(False), then returns 3 pending tasks."""
    tasklist = TaskList()
    pending1 = tasklist.add_task("Pending 1", "")
    pending2 = tasklist.add_task("Pending 2", "")
    completed1 = tasklist.add_task("Completed 1", "")
    completed1.completed = True
    pending3 = tasklist.add_task("Pending 3", "")
    completed2 = tasklist.add_task("Completed 2", "")
    completed2.completed = True

    result = tasklist.filter_tasks_by_status(completed=False)
    assert len(result) == 3
    assert all(not t.completed for t in result)

def test_filter_completed_tasks():
    """Given 3 pending and 2 completed tasks, when filter_tasks_by_status(True), then returns 2 completed tasks."""
    tasklist = TaskList()
    tasklist.add_task("Pending 1", "")
    completed1 = tasklist.add_task("Completed 1", "")
    completed1.completed = True
    tasklist.add_task("Pending 2", "")
    completed2 = tasklist.add_task("Completed 2", "")
    completed2.completed = True

    result = tasklist.filter_tasks_by_status(completed=True)
    assert len(result) == 2
    assert all(t.completed for t in result)

def test_filter_no_matches():
    """Given all tasks are pending, when filter_tasks_by_status(True), then returns empty list."""
    tasklist = TaskList()
    tasklist.add_task("Pending 1", "")
    tasklist.add_task("Pending 2", "")

    result = tasklist.filter_tasks_by_status(completed=True)
    assert result == []

def test_filter_empty_list():
    """Given empty TaskList, when filter_tasks_by_status called, then returns empty list."""
    tasklist = TaskList()
    assert tasklist.filter_tasks_by_status(completed=True) == []
    assert tasklist.filter_tasks_by_status(completed=False) == []

def test_filter_sorted_by_id():
    """Given filtered tasks, when filter_tasks_by_status called, then results sorted by ID ascending."""
    tasklist = TaskList()
    task1 = tasklist.add_task("Task 1", "")
    task2 = tasklist.add_task("Task 2", "")
    task2.completed = True
    task3 = tasklist.add_task("Task 3", "")
    task4 = tasklist.add_task("Task 4", "")
    task4.completed = True
    task5 = tasklist.add_task("Task 5", "")

    pending = tasklist.filter_tasks_by_status(completed=False)
    assert [t.id for t in pending] == [1, 3, 5]

    completed = tasklist.filter_tasks_by_status(completed=True)
    assert [t.id for t in completed] == [2, 4]
```

---

## Acceptance Criteria

All three methods must:

1. ✅ **Return correct data**: Match expected output for all test cases
2. ✅ **Preserve encapsulation**: Do not expose internal `_tasks` list directly
3. ✅ **Maintain sort order**: All list returns must be sorted by ID ascending
4. ✅ **Handle empty state**: Return empty list (not None, not error) when appropriate
5. ✅ **No side effects**: Do not modify TaskList state or Task objects
6. ✅ **No exceptions**: Return None or empty list instead of raising exceptions
7. ✅ **Performance**: O(n log n) or better for Phase I scale (100+ tasks)

---

## Integration Points

- **Used by**: CLI view operations (`todo_cli.py`)
- **Depends on**: Task entity from `001-add-task`
- **Tested in**: `tests/unit/test_task_service_view.py`
- **Contract tests**: `tests/contract/test_view_contracts.py`
