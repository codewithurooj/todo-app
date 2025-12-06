# Contract: Display Formatter Functions

**Feature**: 004-view-task
**Component**: display.py (lib)
**Purpose**: Define contracts for display formatting functions

---

## Function: `format_task_list()`

### Contract

**Purpose**: Format a list of tasks for console display with appropriate empty state messages.

**Input**:
- `tasks: list[Task]` - List of tasks to format (may be empty)
- `context: str = "all"` - Display context ("all", "pending", or "completed")

**Output**: `str`
- If tasks is empty:
  - context="all": "No tasks found. Add a task to get started!"
  - context="pending": "No pending tasks found."
  - context="completed": "No completed tasks found."
- If tasks is not empty:
  - Header: "You have X task(s)"
  - One line per task: "[ID] [Status] Title"
  - Title truncated to 50 chars if needed

**Side Effects**: None (pure function)

**Exceptions**: None

### Test Cases

```python
def test_format_task_list_empty_all():
    """Given empty list with context='all', returns 'No tasks found' message."""
    result = format_task_list([], context="all")
    assert result == "No tasks found. Add a task to get started!"

def test_format_task_list_empty_pending():
    """Given empty list with context='pending', returns 'No pending tasks' message."""
    result = format_task_list([], context="pending")
    assert result == "No pending tasks found."

def test_format_task_list_empty_completed():
    """Given empty list with context='completed', returns 'No completed tasks' message."""
    result = format_task_list([], context="completed")
    assert result == "No completed tasks found."

def test_format_task_list_single_task():
    """Given list with 1 task, formats with header and task row."""
    task = Task(id=1, title="Test", description="", completed=False, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_list([task])
    assert "You have 1 task(s)" in result
    assert "[1]" in result
    assert "[ ]" in result  # Pending status
    assert "Test" in result

def test_format_task_list_multiple_tasks():
    """Given list with 3 tasks, formats all tasks with correct count."""
    tasks = [
        Task(id=1, title="First", description="", completed=False, created_at=datetime.now(), updated_at=datetime.now()),
        Task(id=2, title="Second", description="", completed=True, created_at=datetime.now(), updated_at=datetime.now()),
        Task(id=3, title="Third", description="", completed=False, created_at=datetime.now(), updated_at=datetime.now()),
    ]
    result = format_task_list(tasks)
    assert "You have 3 task(s)" in result
    assert "[1]" in result
    assert "[2]" in result
    assert "[3]" in result

def test_format_task_list_truncates_long_titles():
    """Given task with >50 char title, title is truncated with ellipsis."""
    long_title = "This is a very long task title that exceeds the fifty character limit significantly"
    task = Task(id=1, title=long_title, description="", completed=False, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_list([task])
    assert "This is a very long task title that exceeds ..." in result
    assert len("This is a very long task title that exceeds ...") == 50
```

---

## Function: `format_task_detail()`

### Contract

**Purpose**: Format a single task with all details for console display.

**Input**: `task: Task` - The task to format (must not be None)

**Output**: `str`
- Multi-line formatted string with:
  - ID: [value]
  - Title: [full title, no truncation]
  - Description: [full description, no truncation]
  - Status: [Completed or Pending]
  - Created: [formatted timestamp]
  - Last Updated: [formatted timestamp]

**Side Effects**: None (pure function)

**Exceptions**: None (assumes valid Task input)

### Test Cases

```python
def test_format_task_detail_all_fields():
    """Given complete task, formats all fields correctly."""
    task = Task(
        id=5,
        title="Buy groceries",
        description="Get milk, bread, eggs from the store",
        completed=False,
        created_at=datetime(2025, 12, 6, 10, 0, 0),
        updated_at=datetime(2025, 12, 6, 10, 0, 0)
    )
    result = format_task_detail(task)
    assert "ID: 5" in result
    assert "Title: Buy groceries" in result
    assert "Description: Get milk, bread, eggs from the store" in result
    assert "Status: Pending" in result
    assert "Created: 2025-12-06 10:00:00" in result
    assert "Last Updated: 2025-12-06 10:00:00" in result

def test_format_task_detail_completed_status():
    """Given completed task, status shows 'Completed'."""
    task = Task(id=1, title="Test", description="", completed=True, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_detail(task)
    assert "Status: Completed" in result

def test_format_task_detail_pending_status():
    """Given pending task, status shows 'Pending'."""
    task = Task(id=1, title="Test", description="", completed=False, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_detail(task)
    assert "Status: Pending" in result

def test_format_task_detail_long_title_no_truncation():
    """Given task with 200-char title, detail view shows full title."""
    long_title = "A" * 200
    task = Task(id=1, title=long_title, description="", completed=False, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_detail(task)
    assert long_title in result  # Full title, not truncated

def test_format_task_detail_long_description_no_truncation():
    """Given task with 1000-char description, detail view shows full description."""
    long_desc = "B" * 1000
    task = Task(id=1, title="Test", description=long_desc, completed=False, created_at=datetime.now(), updated_at=datetime.now())
    result = format_task_detail(task)
    assert long_desc in result  # Full description, not truncated
```

---

## Function: `truncate_title()`

### Contract

**Purpose**: Truncate long titles with ellipsis for list display.

**Input**:
- `title: str` - The title to truncate
- `max_len: int = 50` - Maximum length (default 50)

**Output**: `str`
- If `len(title) <= max_len`: returns title unchanged
- If `len(title) > max_len`: returns `title[:max_len-3] + "..."`

**Side Effects**: None (pure function)

**Exceptions**: None

### Test Cases

```python
def test_truncate_title_short():
    """Given title <= 50 chars, returns unchanged."""
    assert truncate_title("Short title") == "Short title"
    assert truncate_title("A" * 50) == "A" * 50

def test_truncate_title_long():
    """Given title > 50 chars, truncates with ellipsis."""
    long_title = "This is a very long task title that exceeds the fifty character limit"
    result = truncate_title(long_title)
    assert result == "This is a very long task title that exceeds ..."
    assert len(result) == 50

def test_truncate_title_custom_max_len():
    """Given custom max_len, truncates at that length."""
    result = truncate_title("This is a test", max_len=10)
    assert result == "This is..."
    assert len(result) == 10

def test_truncate_title_exactly_max_len():
    """Given title exactly max_len, returns unchanged."""
    title = "A" * 50
    assert truncate_title(title, max_len=50) == title
```

---

## Function: `format_status()`

### Contract

**Purpose**: Format task completion status with icon and text.

**Input**: `completed: bool` - Task completion status

**Output**: `str`
- True: "[✓] Completed"
- False: "[ ] Pending"

**Side Effects**: None (pure function)

**Exceptions**: None

### Test Cases

```python
def test_format_status_completed():
    """Given completed=True, returns completed status with checkmark."""
    assert format_status(True) == "[✓] Completed"

def test_format_status_pending():
    """Given completed=False, returns pending status with empty checkbox."""
    assert format_status(False) == "[ ] Pending"
```

---

## Function: `format_timestamp()`

### Contract

**Purpose**: Format datetime as human-readable string.

**Input**: `dt: datetime` - The datetime to format

**Output**: `str`
- Format: "YYYY-MM-DD HH:MM:SS"
- Example: "2025-12-06 14:30:00"

**Side Effects**: None (pure function)

**Exceptions**: None (assumes valid datetime input)

### Test Cases

```python
def test_format_timestamp_standard():
    """Given datetime, formats as YYYY-MM-DD HH:MM:SS."""
    dt = datetime(2025, 12, 6, 14, 30, 0)
    assert format_timestamp(dt) == "2025-12-06 14:30:00"

def test_format_timestamp_midnight():
    """Given midnight time, formats correctly."""
    dt = datetime(2025, 1, 1, 0, 0, 0)
    assert format_timestamp(dt) == "2025-01-01 00:00:00"

def test_format_timestamp_single_digits():
    """Given single-digit month/day/time, formats with leading zeros."""
    dt = datetime(2025, 1, 5, 9, 5, 3)
    assert format_timestamp(dt) == "2025-01-05 09:05:03"
```

---

## Acceptance Criteria

All formatting functions must:

1. ✅ **Pure functions**: No side effects, same input always produces same output
2. ✅ **No exceptions**: Handle all expected inputs gracefully
3. ✅ **Clear output**: Console-friendly formatting with proper alignment
4. ✅ **Consistent**: All list views use same format
5. ✅ **Truncation**: List views truncate titles at 50 chars, detail views show full text
6. ✅ **Empty state**: Appropriate messages for empty lists based on context
7. ✅ **Portable**: No console color codes or special characters that might not render

---

## Integration Points

- **Used by**: CLI view operations (`todo_cli.py`)
- **Depends on**: Task entity from `001-add-task`
- **Tested in**: `tests/unit/test_display.py`
- **Contract tests**: `tests/contract/test_view_contracts.py`
