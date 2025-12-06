# Data Model: View Tasks Feature

**Branch**: `004-view-task` | **Date**: 2025-12-06

## Overview

This feature extends the existing `TaskList` entity from `001-add-task` with query methods for viewing tasks. The `Task` entity remains unchanged - no new fields or modifications required.

---

## Task Entity

**Source**: Defined in `001-add-task` feature.

**No changes required for this feature.**

The existing Task dataclass already contains all necessary fields for viewing:

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

All view operations use these existing fields.

---

## TaskList Entity Extensions

**Source**: Defined in `001-add-task`, extended by `002-delete-task` and `003-update-task`.

**New methods for this feature** (read-only query operations):

### Method: `get_all_tasks()`

**Purpose**: Retrieve all tasks for display.

**Signature**:
```python
def get_all_tasks(self) -> list[Task]:
    """
    Return all tasks sorted by ID ascending.

    Returns:
        list[Task]: All tasks in ID order (empty list if no tasks exist)
    """
```

**Behavior**:
- Returns all tasks in the internal `_tasks` list
- Tasks are sorted by ID in ascending order (1, 2, 3, ...)
- Empty list is valid return value (when no tasks exist)
- Does not modify internal state

**Example**:
```python
tasklist = TaskList()
# ... add tasks with IDs 3, 1, 2
all_tasks = tasklist.get_all_tasks()  # Returns [Task(id=1), Task(id=2), Task(id=3)]
```

---

### Method: `get_task_by_id()`

**Purpose**: Retrieve a specific task by its ID.

**Signature**:
```python
def get_task_by_id(self, task_id: int) -> Task | None:
    """
    Return the task with the specified ID.

    Args:
        task_id: The unique ID of the task to retrieve

    Returns:
        Task | None: The task if found, None otherwise
    """
```

**Behavior**:
- Searches internal `_tasks` list for task with matching ID
- Returns the Task object if found
- Returns None if task_id doesn't exist
- Does not modify internal state
- Does not validate task_id format (caller's responsibility)

**Example**:
```python
tasklist = TaskList()
# ... add task with ID 5
task = tasklist.get_task_by_id(5)  # Returns Task(id=5, ...)
missing = tasklist.get_task_by_id(99)  # Returns None
```

---

### Method: `filter_tasks_by_status()`

**Purpose**: Retrieve tasks filtered by completion status.

**Signature**:
```python
def filter_tasks_by_status(self, completed: bool) -> list[Task]:
    """
    Return tasks matching the specified completion status.

    Args:
        completed: True for completed tasks, False for pending tasks

    Returns:
        list[Task]: Matching tasks in ID order (empty list if no matches)
    """
```

**Behavior**:
- Filters internal `_tasks` list by `completed` attribute
- Returns only tasks where `task.completed == completed`
- Results are sorted by ID in ascending order
- Empty list is valid return value (when no tasks match filter)
- Does not modify internal state

**Example**:
```python
tasklist = TaskList()
# ... add 3 pending tasks (IDs 1, 2, 3) and 2 completed tasks (IDs 4, 5)
pending = tasklist.filter_tasks_by_status(completed=False)  # Returns [Task(id=1), Task(id=2), Task(id=3)]
completed = tasklist.filter_tasks_by_status(completed=True)  # Returns [Task(id=4), Task(id=5)]
```

---

## Display Formatting (New Module)

**Source**: New module `src/lib/display.py` created for this feature.

This module contains pure formatting functions with no state. These are not part of the data model but are documented here for completeness.

### Function: `format_task_list()`

**Purpose**: Format a list of tasks for console display.

**Signature**:
```python
def format_task_list(tasks: list[Task], context: str = "all") -> str:
    """
    Format list of tasks for display.

    Args:
        tasks: List of tasks to format
        context: Display context ("all", "pending", or "completed")

    Returns:
        str: Formatted output ready for console display
    """
```

**Behavior**:
- If tasks is empty, returns context-specific message
- Otherwise, returns formatted list with header and task rows
- Each task shows: `[ID] [Status Icon] Title (truncated)`
- Header shows task count

---

### Function: `format_task_detail()`

**Purpose**: Format a single task with full details.

**Signature**:
```python
def format_task_detail(task: Task) -> str:
    """
    Format a single task with complete details.

    Args:
        task: The task to format

    Returns:
        str: Formatted detail view ready for console display
    """
```

**Behavior**:
- Returns multi-line string with all task fields
- Shows: ID, Title (full), Description (full), Status, Created, Last Updated
- Timestamps formatted as "YYYY-MM-DD HH:MM:SS"

---

### Function: `truncate_title()`

**Purpose**: Truncate long titles for list view.

**Signature**:
```python
def truncate_title(title: str, max_len: int = 50) -> str:
    """
    Truncate title to max length with ellipsis.

    Args:
        title: The title to truncate
        max_len: Maximum length (default: 50)

    Returns:
        str: Truncated title (or original if <= max_len)
    """
```

**Behavior**:
- If `len(title) <= max_len`: returns title unchanged
- If `len(title) > max_len`: returns `title[:max_len-3] + "..."`

---

### Function: `format_status()`

**Purpose**: Format task completion status.

**Signature**:
```python
def format_status(completed: bool) -> str:
    """
    Format task status with icon and text.

    Args:
        completed: Task completion status

    Returns:
        str: "[✓] Completed" or "[ ] Pending"
    """
```

---

### Function: `format_timestamp()`

**Purpose**: Format datetime for display.

**Signature**:
```python
def format_timestamp(dt: datetime) -> str:
    """
    Format datetime as human-readable string.

    Args:
        dt: The datetime to format

    Returns:
        str: Formatted timestamp "YYYY-MM-DD HH:MM:SS"
    """
```

---

## Validation (Existing - Reused)

**Source**: Defined in `002-delete-task` feature.

**No new validators needed.** This feature reuses the existing task ID validator:

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | None, str]:
    """
    Validate task ID format and range.

    Args:
        task_id_str: User input for task ID

    Returns:
        tuple[bool, int | None, str]: (is_valid, parsed_id, error_message)
    """
```

Used when prompting user to enter task ID for detail view.

---

## Data Flow

### View All Tasks Flow
```
User selects "View All Tasks"
    ↓
CLI calls TaskList.get_all_tasks()
    ↓
TaskList returns sorted list[Task]
    ↓
CLI calls format_task_list(tasks, context="all")
    ↓
Display formatter returns formatted string
    ↓
CLI prints to console
```

### View Task Details Flow
```
User selects "View Task Details"
    ↓
CLI prompts for task ID
    ↓
CLI calls validate_task_id(user_input)
    ↓
If invalid: show error and return
If valid: continue
    ↓
CLI calls TaskList.get_task_by_id(task_id)
    ↓
If None: show "Task not found" error
If Task: continue
    ↓
CLI calls format_task_detail(task)
    ↓
Display formatter returns formatted detail string
    ↓
CLI prints to console
```

### Filter Tasks Flow
```
User selects "View Pending Tasks" or "View Completed Tasks"
    ↓
CLI determines filter: completed=True or completed=False
    ↓
CLI calls TaskList.filter_tasks_by_status(completed)
    ↓
TaskList returns filtered, sorted list[Task]
    ↓
CLI calls format_task_list(tasks, context="pending"|"completed")
    ↓
Display formatter returns formatted string (or empty message)
    ↓
CLI prints to console
```

---

## Immutability Considerations

**Important**: View operations return references to the original Task objects, not copies.

**Rationale**:
- Task is a dataclass (not frozen, but modification requires explicit assignment)
- View operations are read-only by design
- Performance: avoid unnecessary copying
- Python convention: no implicit immutability

**Risk**: Calling code could theoretically modify returned tasks.

**Mitigation**: View operations are only called from display/CLI code that has no reason to modify tasks. Update operations use dedicated methods from `003-update-task`.

---

## Summary

**Extensions to existing entities**:
- TaskList: +3 query methods (`get_all_tasks`, `get_task_by_id`, `filter_tasks_by_status`)

**New modules**:
- `src/lib/display.py`: 5 pure formatting functions

**No changes**:
- Task entity: No modifications
- Validators: Reuse existing `validate_task_id()` from 002-delete-task

**Design principles applied**:
- **Separation of concerns**: Data access (TaskList) vs. presentation (display.py)
- **Read-only operations**: Query methods don't modify state
- **Code reuse**: Leverage existing validator
- **Clear API**: Simple, testable method signatures
