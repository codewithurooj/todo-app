# Phase 0 Research: View Tasks Feature

**Branch**: `004-view-task` | **Date**: 2025-12-06

## Research Scope

Determine the optimal technical approach for implementing read-only task viewing operations in the Phase I todo application. Focus on query methods, display formatting, filtering logic, and error handling for empty/non-existent tasks.

---

## Technical Decisions

### Decision 1: Query Method Design

**Question**: How should TaskList expose tasks for viewing?

**Options Considered**:
1. Direct list access: `tasklist._tasks` (breaks encapsulation)
2. Generator pattern: `yield` tasks one at a time (complex for simple use case)
3. Query methods: `get_all_tasks()`, `get_task_by_id()`, `filter_tasks_by_status()` (clear API)

**Decision**: **Option 3 - Query methods**

**Rationale**:
- Preserves encapsulation of internal `_tasks` list
- Clear, testable API surface
- Returns copies/views to prevent external modification
- Aligns with existing service pattern from 001/002/003

**Implementation**:
```python
def get_all_tasks(self) -> list[Task]:
    """Return all tasks sorted by ID ascending."""
    return sorted(self._tasks, key=lambda t: t.id)

def get_task_by_id(self, task_id: int) -> Task | None:
    """Return task with given ID, or None if not found."""
    for task in self._tasks:
        if task.id == task_id:
            return task
    return None

def filter_tasks_by_status(self, completed: bool) -> list[Task]:
    """Return tasks matching completion status, sorted by ID."""
    filtered = [t for t in self._tasks if t.completed == completed]
    return sorted(filtered, key=lambda t: t.id)
```

---

### Decision 2: Display Formatting Strategy

**Question**: Where should display formatting logic live?

**Options Considered**:
1. Inside TaskList methods (violates SRP, mixes data and presentation)
2. Inside CLI code (duplicates formatting logic across menu options)
3. Dedicated display module (`lib/display.py`) with formatting functions

**Decision**: **Option 3 - Dedicated display module**

**Rationale**:
- Separates data access from presentation (SRP)
- Reusable formatting functions across all view operations
- Easy to test formatting independently
- Keeps TaskList focused on data management

**Implementation**:
```python
# src/lib/display.py
def format_task_list(tasks: list[Task]) -> str:
    """Format list of tasks for console display."""
    # Header with count + formatted tasks

def format_task_detail(task: Task) -> str:
    """Format single task with full details."""
    # ID, title, description, status, timestamps

def truncate_title(title: str, max_len: int = 50) -> str:
    """Truncate title to max_len with ellipsis."""
    # Handle truncation
```

---

### Decision 3: Title Truncation Approach

**Question**: How should we truncate long titles in list view?

**Options Considered**:
1. Hard cutoff at 50 chars (looks broken: "This is a very long task title that exceeds fi")
2. Word boundary cutoff (complex, inconsistent length)
3. 47 chars + "..." (clear truncation indicator, consistent format)

**Decision**: **Option 3 - 47 chars + "..."**

**Rationale**:
- Clear visual indicator that title is truncated
- Consistent total length (50 chars)
- Simple implementation: `title[:47] + "..."` if `len(title) > 50`
- Spec requirement: FR-024

**Implementation**:
```python
def truncate_title(title: str, max_len: int = 50) -> str:
    if len(title) <= max_len:
        return title
    return title[:max_len - 3] + "..."
```

---

### Decision 4: Empty List Handling

**Question**: How should we handle viewing empty task lists?

**Options Considered**:
1. Return empty string (confusing, looks like error)
2. Raise exception (forces try/catch everywhere)
3. Return specific message string from formatting function

**Decision**: **Option 3 - Specific message from formatter**

**Rationale**:
- No exceptions for expected scenarios
- Clear, helpful user feedback
- Spec requirement: FR-005, FR-014
- Messages vary by context:
  - All tasks: "No tasks found. Add a task to get started!"
  - Pending filter: "No pending tasks found."
  - Completed filter: "No completed tasks found."

**Implementation**:
```python
def format_task_list(tasks: list[Task], context: str = "all") -> str:
    if not tasks:
        if context == "pending":
            return "No pending tasks found."
        elif context == "completed":
            return "No completed tasks found."
        else:
            return "No tasks found. Add a task to get started!"
    # ... format tasks
```

---

### Decision 5: Task ID Validation - Reuse or Duplicate?

**Question**: Should we reuse the task ID validator from 002-delete-task?

**Options Considered**:
1. Duplicate validation in view code (violates DRY)
2. Copy validator to new module (still duplicates)
3. Reuse existing `validate_task_id()` from 002-delete-task

**Decision**: **Option 3 - Reuse existing validator**

**Rationale**:
- DRY principle - single source of truth
- Consistent validation across features (delete, update, view)
- Already tested and working
- Same requirements: positive integer, numeric format

**Implementation**:
- Import `validate_task_id()` from existing validator module
- Use in CLI when prompting for task ID in detail view
- No new validation code needed

---

### Decision 6: Sort Order for Task Lists

**Question**: How should tasks be ordered in list views?

**Options Considered**:
1. Insertion order (unpredictable, depends on add/delete history)
2. ID descending (newest first - not intuitive for task lists)
3. ID ascending (oldest first - matches creation order)

**Decision**: **Option 3 - ID ascending**

**Rationale**:
- Predictable, consistent ordering
- Matches intuitive "chronological" expectation (lower ID = created earlier)
- Easy to implement: `sorted(tasks, key=lambda t: t.id)`
- Spec requirement: FR-004, FR-015

**Implementation**:
```python
# All query methods return sorted results
return sorted(self._tasks, key=lambda t: t.id)
return sorted(filtered, key=lambda t: t.id)
```

---

### Decision 7: Status Display Format

**Question**: How should task status be displayed in list view?

**Options Considered**:
1. Text only: "Completed", "Pending" (plain, no visual distinction)
2. Colored text: green/red (console color codes - complex, not portable)
3. Symbols + text: "[✓] Completed", "[ ] Pending" (clear, portable)

**Decision**: **Option 3 - Symbols + text**

**Rationale**:
- Clear visual distinction without requiring color support
- Portable across all consoles
- Intuitive checkbox metaphor
- Spec requirement: FR-004

**Implementation**:
```python
def format_status(completed: bool) -> str:
    return "[✓] Completed" if completed else "[ ] Pending"
```

---

### Decision 8: Detail View Timestamp Format

**Question**: How should timestamps be formatted in detail view?

**Options Considered**:
1. ISO 8601: "2025-12-06T10:00:00+00:00" (precise, not human-friendly)
2. Relative: "2 hours ago" (imprecise, requires calculation)
3. Human-readable: "2025-12-06 10:00:00" (clear, precise, readable)

**Decision**: **Option 3 - Human-readable format**

**Rationale**:
- Balances precision and readability
- Spec requirement: FR-011 ("human-readable")
- Simple: `created_at.strftime("%Y-%m-%d %H:%M:%S")`
- Consistent with spec example

**Implementation**:
```python
def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
```

---

### Decision 9: Error Handling for Non-Existent Tasks

**Question**: How should we handle viewing non-existent task IDs?

**Options Considered**:
1. Raise exception (forces try/catch in CLI, verbose)
2. Return None, CLI checks and shows error (separation of concerns)
3. Return tuple `(success: bool, result: Task | str)` (complex return type)

**Decision**: **Option 2 - Return None, CLI handles error**

**Rationale**:
- `get_task_by_id()` returns `Task | None` (simple, Pythonic)
- CLI checks result and shows appropriate error message
- Consistent with "not found" pattern in Python
- Service layer doesn't need to know about error messages

**Implementation**:
```python
# Service layer
task = task_service.get_task_by_id(task_id)
if not task:
    print(f"Error: Task with ID {task_id} not found.")
    return
# ... display task details
```

---

### Decision 10: CLI Menu Structure for View Operations

**Question**: How should view operations be organized in the CLI menu?

**Options Considered**:
1. Single "View Tasks" option with sub-menu (extra navigation step)
2. Flat menu with all view options at top level (cluttered, 7+ options)
3. Logical grouping: "View All", "View Details", "Filter" submenu

**Decision**: **Option 2 - Flat menu with clear labels**

**Rationale**:
- Minimizes navigation steps
- All view operations are one selection away
- Clear labels differentiate options:
  - "1. View All Tasks"
  - "2. View Task Details"
  - "3. View Pending Tasks"
  - "4. View Completed Tasks"
- Consistent with existing menu structure from 001/002/003

**Implementation**:
- Add 4 new menu options to existing todo_cli.py main menu
- Each option calls corresponding service method + display formatter

---

### Decision 11: View Method Return Types

**Question**: What should view query methods return?

**Options Considered**:
1. Mutable references to original Task objects (allows accidental modification)
2. Deep copies of Task objects (expensive, unnecessary for immutable viewing)
3. Original Task references (acceptable since Task is a dataclass)

**Decision**: **Option 3 - Return original references**

**Rationale**:
- Task is a dataclass - modification requires explicit attribute assignment
- No expectation of immutability in Python (unlike Java/C#)
- Performance: avoid unnecessary copying
- Viewing code doesn't modify tasks (read-only operations)
- If future needs arise, can copy in display layer

**Implementation**:
```python
# Just return the task objects directly
return sorted(self._tasks, key=lambda t: t.id)
return task  # not copy.deepcopy(task)
```

---

## Summary of Research Outcomes

**11 technical decisions finalized**:

1. ✅ Query methods API: `get_all_tasks()`, `get_task_by_id()`, `filter_tasks_by_status()`
2. ✅ Display formatting: Dedicated `lib/display.py` module (SRP)
3. ✅ Title truncation: 47 chars + "..." for >50 char titles
4. ✅ Empty list handling: Context-specific messages from formatter
5. ✅ Task ID validation: Reuse existing `validate_task_id()` from 002
6. ✅ Sort order: ID ascending (oldest first)
7. ✅ Status display: "[✓] Completed" / "[ ] Pending"
8. ✅ Timestamp format: "YYYY-MM-DD HH:MM:SS"
9. ✅ Non-existent task: Return None, CLI shows error
10. ✅ Menu structure: Flat menu with 4 view options
11. ✅ Return types: Original Task references (no copying)

**Key Design Principles**:
- **Separation of concerns**: Data access (TaskList) vs. presentation (display.py)
- **Code reuse**: Leverage existing validators from 002-delete-task
- **Clear feedback**: Specific messages for empty lists and errors
- **Consistency**: Align with existing patterns from 001/002/003

**Ready for Phase 1**: Data model extensions and contract definitions.
