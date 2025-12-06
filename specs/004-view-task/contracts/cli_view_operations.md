# Contract: CLI View Operations

**Feature**: 004-view-task
**Component**: todo_cli.py (CLI)
**Purpose**: Define contracts for view-related CLI menu options and user interactions

---

## CLI Menu Options

The CLI must add 4 new menu options for viewing tasks:

1. **View All Tasks**: Display all tasks in the list
2. **View Task Details**: Display complete details for a specific task
3. **View Pending Tasks**: Display only pending (incomplete) tasks
4. **View Completed Tasks**: Display only completed tasks

---

## Operation: View All Tasks

### Contract

**Trigger**: User selects "View All Tasks" from main menu

**Flow**:
1. CLI calls `TaskList.get_all_tasks()`
2. CLI calls `format_task_list(tasks, context="all")`
3. CLI prints formatted output to console
4. CLI returns to main menu

**Expected Output**:
- If tasks exist: Header + list of all tasks
- If no tasks: "No tasks found. Add a task to get started!"

**Error Handling**: None required (method never fails)

### Test Cases

```python
def test_view_all_tasks_with_tasks(capsys):
    """Given TaskList with 3 tasks, when user selects View All, then all tasks displayed."""
    # Setup: Create tasklist with 3 tasks
    # Action: Simulate "View All Tasks" menu selection
    # Assert: Output contains all 3 task IDs and titles

def test_view_all_tasks_empty_list(capsys):
    """Given empty TaskList, when user selects View All, then empty message displayed."""
    # Setup: Create empty tasklist
    # Action: Simulate "View All Tasks" menu selection
    # Assert: Output contains "No tasks found. Add a task to get started!"
```

---

## Operation: View Task Details

### Contract

**Trigger**: User selects "View Task Details" from main menu

**Flow**:
1. CLI prompts user: "Enter task ID: "
2. CLI reads user input
3. CLI calls `validate_task_id(user_input)`
4. If validation fails:
   - CLI prints error message from validator
   - CLI returns to main menu
5. If validation succeeds:
   - CLI calls `TaskList.get_task_by_id(task_id)`
   - If task is None:
     - CLI prints "Error: Task with ID [X] not found."
     - CLI returns to main menu
   - If task exists:
     - CLI calls `format_task_detail(task)`
     - CLI prints formatted output
     - CLI returns to main menu

**Expected Output**:
- Valid task: Full task details (ID, title, description, status, timestamps)
- Invalid ID format: "Error: Invalid task ID format. Please enter a number."
- Invalid ID range: "Error: Task ID must be a positive number."
- Non-existent ID: "Error: Task with ID [X] not found."

**Error Handling**:
- Invalid input format (non-numeric): Show validation error
- Invalid input range (zero, negative): Show validation error
- Task not found: Show not found error
- All errors return to main menu (no crash)

### Test Cases

```python
def test_view_task_details_valid_id(capsys, monkeypatch):
    """Given valid task ID, when user views details, then full task details displayed."""
    # Setup: Create task with ID 5
    # Mock input: "5"
    # Assert: Output contains all task fields

def test_view_task_details_non_existent_id(capsys, monkeypatch):
    """Given non-existent task ID, when user views details, then error shown."""
    # Setup: Create tasks with IDs 1,2,3
    # Mock input: "99"
    # Assert: Output contains "Error: Task with ID 99 not found."

def test_view_task_details_invalid_format(capsys, monkeypatch):
    """Given non-numeric input, when user views details, then format error shown."""
    # Mock input: "abc"
    # Assert: Output contains "Error: Invalid task ID format"

def test_view_task_details_negative_id(capsys, monkeypatch):
    """Given negative ID, when user views details, then range error shown."""
    # Mock input: "-5"
    # Assert: Output contains "Error: Task ID must be a positive number."

def test_view_task_details_zero_id(capsys, monkeypatch):
    """Given zero ID, when user views details, then range error shown."""
    # Mock input: "0"
    # Assert: Output contains "Error: Task ID must be a positive number."
```

---

## Operation: View Pending Tasks

### Contract

**Trigger**: User selects "View Pending Tasks" from main menu

**Flow**:
1. CLI calls `TaskList.filter_tasks_by_status(completed=False)`
2. CLI calls `format_task_list(tasks, context="pending")`
3. CLI prints formatted output to console
4. CLI returns to main menu

**Expected Output**:
- If pending tasks exist: Header + list of pending tasks only
- If no pending tasks: "No pending tasks found."

**Error Handling**: None required (method never fails)

### Test Cases

```python
def test_view_pending_tasks_with_pending(capsys):
    """Given 3 pending and 2 completed tasks, when user views pending, then only 3 pending tasks shown."""
    # Setup: Create 3 pending + 2 completed tasks
    # Action: Simulate "View Pending Tasks" menu selection
    # Assert: Output shows only the 3 pending tasks

def test_view_pending_tasks_all_completed(capsys):
    """Given all tasks completed, when user views pending, then 'No pending tasks' message shown."""
    # Setup: Create tasks, mark all as completed
    # Action: Simulate "View Pending Tasks" menu selection
    # Assert: Output contains "No pending tasks found."

def test_view_pending_tasks_empty_list(capsys):
    """Given empty TaskList, when user views pending, then 'No pending tasks' message shown."""
    # Setup: Empty tasklist
    # Action: Simulate "View Pending Tasks" menu selection
    # Assert: Output contains "No pending tasks found."
```

---

## Operation: View Completed Tasks

### Contract

**Trigger**: User selects "View Completed Tasks" from main menu

**Flow**:
1. CLI calls `TaskList.filter_tasks_by_status(completed=True)`
2. CLI calls `format_task_list(tasks, context="completed")`
3. CLI prints formatted output to console
4. CLI returns to main menu

**Expected Output**:
- If completed tasks exist: Header + list of completed tasks only
- If no completed tasks: "No completed tasks found."

**Error Handling**: None required (method never fails)

### Test Cases

```python
def test_view_completed_tasks_with_completed(capsys):
    """Given 3 pending and 2 completed tasks, when user views completed, then only 2 completed tasks shown."""
    # Setup: Create 3 pending + 2 completed tasks
    # Action: Simulate "View Completed Tasks" menu selection
    # Assert: Output shows only the 2 completed tasks

def test_view_completed_tasks_all_pending(capsys):
    """Given all tasks pending, when user views completed, then 'No completed tasks' message shown."""
    # Setup: Create tasks, all pending
    # Action: Simulate "View Completed Tasks" menu selection
    # Assert: Output contains "No completed tasks found."

def test_view_completed_tasks_empty_list(capsys):
    """Given empty TaskList, when user views completed, then 'No completed tasks' message shown."""
    # Setup: Empty tasklist
    # Action: Simulate "View Completed Tasks" menu selection
    # Assert: Output contains "No completed tasks found."
```

---

## User Input Validation

**Reused Component**: `validate_task_id()` from 002-delete-task

**Used in**: View Task Details operation only

**Validation Rules**:
- Empty input: Error
- Non-numeric input: "Error: Invalid task ID format. Please enter a number."
- Zero or negative: "Error: Task ID must be a positive number."
- Valid positive integer: Parse and continue

---

## Menu Integration

**Existing Menu** (from 001/002/003):
1. Add Task
2. Delete Task
3. Update Task
... (other options)

**New Options** (added for this feature):
- View All Tasks
- View Task Details
- View Pending Tasks
- View Completed Tasks

**Placement**: Group view operations together, logically separate from modify operations

---

## Error Recovery

All view operations must:

1. ✅ **Never crash**: Invalid input shows error and returns to menu
2. ✅ **Clear errors**: Error messages explain what went wrong
3. ✅ **Return to menu**: After view operation (success or error), user returns to main menu
4. ✅ **No data loss**: View operations are read-only, never modify data
5. ✅ **Recoverable**: User can retry operation after error

---

## Acceptance Criteria

All CLI view operations must:

1. ✅ **Display correct data**: Show all expected tasks with correct fields
2. ✅ **Handle empty state**: Show appropriate message when no tasks match
3. ✅ **Validate input**: Catch and report invalid task IDs (detail view only)
4. ✅ **Consistent formatting**: Use display formatter functions for all output
5. ✅ **Return to menu**: Always return to main menu after operation
6. ✅ **No crashes**: Handle all error cases gracefully
7. ✅ **Clear feedback**: User understands what they're viewing and any errors

---

## Integration Points

- **Calls**: TaskList query methods, display formatter functions, validate_task_id
- **Called by**: Main menu loop
- **Tested in**: `tests/integration/test_view_integration.py`
- **Contract tests**: `tests/contract/test_view_contracts.py`
