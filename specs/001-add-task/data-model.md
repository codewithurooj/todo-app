# Data Model: Add Task Feature

**Feature**: 001-add-task
**Date**: 2025-12-06
**Status**: Phase 1 - Design

---

## Overview

This document defines the data model for the Add Task feature. The model uses Python dataclasses for type safety and clarity, with in-memory storage via Python lists. All design decisions prioritize Phase I simplicity while maintaining clear evolution paths for future phases.

---

## 1. Task Entity

### Definition

The `Task` is the core domain entity representing a single todo item.

**Python Implementation**:
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

### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-generated | Unique task identifier (sequential) |
| `title` | `str` | Yes | N/A | Task title/summary |
| `description` | `Optional[str]` | No | `None` | Detailed task description |
| `completed` | `bool` | Yes | `False` | Completion status |
| `created_at` | `datetime` | Yes | Auto-generated | Creation timestamp (UTC) |

### Validation Rules

**Title**:
- **Required**: Must not be empty or whitespace-only
- **Length**: 1-200 characters (after stripping whitespace)
- **Type**: String (UTF-8 encoded)
- **Validation**: `validate_title(title: str) -> tuple[bool, str]`

**Description**:
- **Optional**: Can be `None` or empty string
- **Length**: 0-1000 characters when provided
- **Type**: String (UTF-8 encoded) or None
- **Validation**: `validate_description(description: str | None) -> tuple[bool, str]`

**ID**:
- **Auto-generated**: Sequential integers starting from 1
- **Uniqueness**: Enforced by TaskList counter
- **Type**: Positive integer

**Completed**:
- **Type**: Boolean
- **Default**: `False` for new tasks
- **Immutable on creation**: Always `False` for Add Task feature

**Created At**:
- **Auto-generated**: Set to current UTC time on creation
- **Format**: Python `datetime` object (UTC timezone)
- **Display Format**: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- **Immutable**: Never changes after creation

### Invariants

1. **ID Uniqueness**: No two tasks can have the same ID
2. **Title Non-Empty**: Title must contain at least one non-whitespace character
3. **Created At Immutability**: Timestamp never changes after task creation
4. **Completed Default**: New tasks always start with `completed=False`

---

## 2. TaskList Collection

### Definition

The `TaskList` manages the in-memory collection of tasks and provides ID generation.

**Python Implementation**:
```python
from typing import List

class TaskList:
    """In-memory collection of tasks with ID management."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and add a new task to the collection."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow()
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in the collection."""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID, return None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_tasks` | `List[Task]` | Private list storing all tasks |
| `_next_id` | `int` | Counter for sequential ID generation |

### Operations

**Add Task**:
- **Input**: `title: str, description: Optional[str] = None`
- **Output**: `Task` (newly created task)
- **Side Effects**:
  - Increments `_next_id`
  - Appends task to `_tasks`
- **Validation**: Performed before calling this method

**Get All Tasks**:
- **Output**: `List[Task]` (defensive copy)
- **Complexity**: O(n) for copying
- **Use Case**: View all tasks feature

**Get Task By ID**:
- **Input**: `task_id: int`
- **Output**: `Optional[Task]` (None if not found)
- **Complexity**: O(n) linear search
- **Use Case**: View details, update, delete operations

### Invariants

1. **ID Monotonicity**: `_next_id` only increases, never decreases
2. **ID Uniqueness**: Each task has unique ID matching its position in sequence
3. **Insertion Order**: Tasks maintain creation order in list
4. **Non-Null List**: `_tasks` is never None, starts as empty list

---

## 3. Validation Model

### Validator Functions

**Title Validation**:
```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if not isinstance(title, str):
        return False, "Title must be a string"

    stripped = title.strip()

    if not stripped:
        return False, "Title cannot be empty"

    if len(stripped) > 200:
        return False, "Title cannot exceed 200 characters"

    return True, ""
```

**Description Validation**:
```python
def validate_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate task description.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if description is None:
        return True, ""

    if not isinstance(description, str):
        return False, "Description must be a string"

    if len(description) > 1000:
        return False, "Description cannot exceed 1000 characters"

    return True, ""
```

### Error Messages

| Validation Failure | Error Message | User Action |
|-------------------|---------------|-------------|
| Empty title | "Title cannot be empty" | Provide non-empty title |
| Title too long | "Title cannot exceed 200 characters" | Shorten title |
| Description too long | "Description cannot exceed 1000 characters" | Shorten description |
| Invalid type | "Title/Description must be a string" | Fix input type |

---

## 4. State Transitions

### Task Lifecycle (Phase I Scope)

```
[Non-existent] --add_task()--> [Active, completed=False]
```

**Phase I**: Tasks are created with `completed=False`. No state transitions in this feature.

**Future Phases**:
- Phase I (other features): Mark complete, update, delete
- Phase II: Persistence (save/load states)
- Phase IV: Archive, restore, soft delete

---

## 5. Relationships

### Current (Phase I)

**TaskList → Task**: One-to-Many
- One `TaskList` instance contains multiple `Task` instances
- Relationship managed via Python list
- No foreign keys (in-memory only)

### Future (Phase II+)

**Phase II** (File Persistence):
- Tasks serialized to JSON array
- Relationship implicit in file structure

**Phase IV** (Database):
- Foreign key: `task.user_id → user.id`
- Foreign key: `task.project_id → project.id`
- Indexes on `user_id`, `created_at`, `completed`

---

## 6. Constraints Summary

### Business Constraints

1. **Title Required**: Every task must have a non-empty title
2. **Sequential IDs**: IDs must be sequential starting from 1
3. **UTC Timestamps**: All timestamps stored in UTC
4. **New Tasks Incomplete**: All new tasks start with `completed=False`

### Technical Constraints

1. **In-Memory Only**: No persistence in Phase I
2. **Single Instance**: One TaskList per application session
3. **No Concurrency**: Single-threaded console application
4. **Linear Search**: O(n) lookups acceptable for n ≤ 1000

### Performance Constraints

1. **Task Creation**: < 1 second
2. **Memory Footprint**: < 100MB for 1000 tasks
3. **List Operations**: < 2 seconds for 1000 tasks

---

## 7. Evolution Path

### Phase I → Phase II (File Persistence)

**Changes Required**:
- Add `to_dict()` and `from_dict()` methods to Task
- Add `save_to_file()` and `load_from_file()` to TaskList
- Preserve all existing attributes (no schema changes)

**Example JSON Schema**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-06T10:30:00"
    }
  ],
  "next_id": 2
}
```

### Phase II → Phase IV (Database)

**ORM Mapping** (SQLAlchemy example):
```python
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Phase IV
```

---

## 8. Testing Considerations

### Unit Test Coverage

**Task Entity**:
- Valid task creation
- Dataclass immutability (frozen=False, but attributes should not be reassigned)
- String representation

**TaskList Operations**:
- Add task with title only
- Add task with title and description
- ID auto-increment
- Retrieve all tasks
- Retrieve by ID (found and not found)

**Validation**:
- Title: empty, valid, too long, whitespace-only
- Description: None, empty, valid, too long

### Edge Cases

1. **Empty TaskList**: Get all returns empty list
2. **Large Titles**: Exactly 200 characters (boundary test)
3. **Unicode Characters**: Emoji, international characters in title/description
4. **Rapid Creation**: Multiple tasks created in same second (timestamp granularity)

---

## Summary

| Component | Implementation | Evolution Ready |
|-----------|----------------|-----------------|
| Task Entity | `@dataclass` with type hints | ✅ JSON serializable |
| TaskList | In-memory list + counter | ✅ File/DB mappable |
| Validation | Pure functions, no state | ✅ Reusable in API layer |
| IDs | Sequential integers | ⚠️ Phase IV needs UUIDs |
| Timestamps | UTC datetime | ✅ ISO 8601 ready |

---

**Status**: Phase 1 Design Complete
**Next**: Generate contracts and quickstart documentation
