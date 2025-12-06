# Technical Research: Mark Task Complete Feature

**Feature**: 005-mark-complete
**Created**: 2025-12-06
**Purpose**: Document technical decisions and rationale for implementing mark complete/uncomplete operations

---

## Research Scope

This feature modifies existing Task entities by toggling completion status. Key research areas:
1. Status field implementation approach
2. Timestamp update mechanism
3. Integration with existing features (001-add-task, 003-update-task, 004-view-task)
4. Validation and error handling patterns
5. CLI menu integration

---

## Technical Decisions

### Decision 1: Status Field Representation

**Decision**: Use boolean `completed` field on Task entity

**Rationale**:
- Phase I constraint: Simple in-memory implementation
- Boolean is sufficient for two states (pending/completed)
- Aligns with existing Task model from 001-add-task
- Follows YAGNI principle - no premature optimization for workflow states

**Alternatives Considered**:
- **String-based status** ("pending", "completed", "in-progress")
  - Rejected: Over-engineering for Phase I; no requirement for intermediate states
- **Enum-based status** (TaskStatus.PENDING, TaskStatus.COMPLETED)
  - Rejected: More complex than needed for binary state in Phase I
  - Note: Will reconsider in Phase II+ when workflow complexity increases

**Evolution Path**:
- Phase II+: May migrate to enum-based system if additional states needed
- Phase IV+: May add workflow state machine for complex lifecycle

**Constitutional Alignment**: ✅ Simplicity First (YAGNI)

---

### Decision 2: Timestamp Update Strategy

**Decision**: Update `updated_at` field on status changes, preserve `created_at`

**Rationale**:
- Spec requirement FR-003: "System MUST update Last Updated timestamp on status changes"
- Maintains audit trail of most recent modification
- Consistent with 003-update-task behavior
- UTC ISO 8601 format already established by 001-add-task

**Alternatives Considered**:
- **Add completion_timestamp field**: Rejected for Phase I (YAGNI)
- **No timestamp update**: Rejected - violates spec FR-003

**Implementation**:
```python
from datetime import datetime, UTC

def mark_complete(task_id: int) -> None:
    task = find_task(task_id)
    task.completed = True
    task.updated_at = datetime.now(UTC)
```

**Evolution Path**:
- Phase II+: Add `completed_at` and `reopened_at` for history tracking
- Phase V+: Event sourcing for complete status change history

**Constitutional Alignment**: ✅ Spec-Driven Development (follows FR-003)

---

### Decision 3: Integration with Existing Features

**Decision**: Reuse Task and TaskList from 001-add-task; extend with mark_complete/unmark methods

**Rationale**:
- Spec dependency: "Relies on Task and TaskList entities from 001-add-task"
- Single source of truth for data model
- Follows DRY principle
- Integrates seamlessly with 004-view-task display logic

**Integration Points**:
1. **001-add-task**: Task and TaskList entities (base)
2. **003-update-task**: Validation and field update patterns (reference)
3. **004-view-task**: Completion status display with "[✓] Completed" indicator

**Implementation Approach**:
- Add methods to existing TaskList class: `mark_complete()`, `unmark_complete()`
- Preserve existing fields (FR-011: "Status changes MUST NOT modify other task fields")
- Use atomic operations (FR-012: "Status changes MUST be atomic")

**Constitutional Alignment**: ✅ Evolutionary Architecture (builds on existing foundation)

---

### Decision 4: Validation Strategy

**Decision**: Two-phase validation: (1) Task existence, (2) Current status check

**Rationale**:
- Spec requirements FR-004 and FR-005
- Provides clear error messages for different failure modes
- Prevents invalid state transitions
- Consistent with validation patterns from 003-update-task

**Validation Flow**:
```python
def mark_complete(task_id: int) -> Result:
    # Phase 1: Validate task existence (FR-004)
    task = task_list.find_by_id(task_id)
    if not task:
        return Error(f"Task with ID {task_id} not found")

    # Phase 2: Validate current status (FR-005)
    if task.completed:
        return Warning(f"Task {task_id} already completed")  # Idempotent UI

    # Execute state change
    task.completed = True
    task.updated_at = datetime.now(UTC)
    return Success(f"Task {task_id} marked as complete")
```

**Error Messages** (FR-007):
- Task not found: "Error: Task with ID {id} not found"
- Already completed: "Task {id} is already completed"
- Already pending: "Task {id} is already pending"

**Constitutional Alignment**: ✅ Clean Code & Python Standards

---

### Decision 5: CLI Menu Integration

**Decision**: Add two new menu options: "Mark Task Complete" and "Reopen Completed Task"

**Rationale**:
- Spec requirements FR-013 and FR-014
- Separates mark/unmark for clarity
- Consistent with existing CLI pattern from other features
- User-friendly labels (non-technical)

**Menu Structure**:
```
Todo App - Main Menu
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete     # New
6. Reopen Completed Task  # New
7. Exit
```

**User Flow**:
1. User selects option 5 or 6
2. System prompts for Task ID
3. System validates and executes operation
4. System displays confirmation or error (FR-006, FR-007)

**Constitutional Alignment**: ✅ Clean Code (clear user interface)

---

### Decision 6: Idempotent Operations

**Decision**: Allow marking already-completed tasks (idempotent), but show warning message

**Rationale**:
- Assumption 5 from spec: "Idempotent UI for already-complete/pending"
- Prevents user confusion if operation repeated
- Aligns with web API best practices (future-proofing for Phase III)
- No crashes from duplicate operations

**Behavior**:
- Marking completed task: Warning + no state change
- Unmarking pending task: Warning + no state change
- Rapid toggles: Each operation succeeds (Edge Case 2)

**Constitutional Alignment**: ✅ Evolutionary Architecture (prepares for REST API idempotency)

---

### Decision 7: Error Handling Approach

**Decision**: Use exceptions for programmer errors, return codes for user input errors

**Rationale**:
- User input errors (invalid ID): Return error result, display message
- Programmer errors (missing task in valid list): Raise exception
- Prevents crashes during normal operation (SC-007: "0 crashes during 1000 operations")
- Pythonic approach: EAFP (Easier to Ask Forgiveness than Permission)

**Implementation Pattern**:
```python
class TaskNotFoundError(ValueError):
    """Raised when task ID does not exist"""
    pass

def mark_complete(task_id: int) -> tuple[bool, str]:
    """Mark task as complete. Returns (success, message)."""
    try:
        task = task_list.get_task(task_id)
        if task.completed:
            return (True, f"Task {task_id} already completed")
        task.completed = True
        task.updated_at = datetime.now(UTC)
        return (True, f"✓ Task {task_id} marked as complete")
    except TaskNotFoundError:
        return (False, f"Error: Task with ID {task_id} not found")
```

**Constitutional Alignment**: ✅ Clean Code & Python Standards

---

### Decision 8: Testing Strategy

**Decision**: Unit tests for TaskList methods + integration tests for CLI workflow

**Rationale**:
- Constitution requirement: Test-Driven Development (TDD)
- Spec success criteria: SC-002 (100% valid operations), SC-004 (100% invalid inputs caught)
- Pyramid approach: More unit tests, fewer integration tests
- pytest framework already established

**Test Coverage**:
1. **Unit Tests** (test_task_list.py):
   - Mark pending task as complete
   - Unmark completed task to reopen
   - Mark non-existent task (error)
   - Mark already-completed task (idempotent)
   - Timestamp updates correctly
   - Other fields preserved (FR-011)

2. **Integration Tests** (test_cli_mark_complete.py):
   - Full CLI workflow for marking complete
   - Full CLI workflow for reopening
   - Error message display
   - Menu option availability

**Constitutional Alignment**: ✅ Test-Driven Development (NON-NEGOTIABLE)

---

## Dependencies

### Internal Dependencies
- **001-add-task**: Task and TaskList entities (REQUIRED)
- **003-update-task**: Validation patterns (REFERENCE)
- **004-view-task**: Completion status display integration (INTEGRATION)

### External Dependencies
- Python 3.13+ (datetime.UTC support)
- pytest (testing framework)

---

## Performance Considerations

**Performance Goals** (from spec SC-001):
- Status changes complete within 1 second

**Analysis**:
- In-memory operations: ~μs latency
- No database queries in Phase I
- No network calls
- Performance goal easily achieved

**Evolution Path**:
- Phase II (file): <100ms with file I/O
- Phase IV (database): <500ms with indexed queries
- Phase VI (distributed): <1s with network latency

**Constitutional Alignment**: ✅ Simplicity First (no premature optimization)

---

## Edge Cases & Solutions

| Edge Case | Solution |
|-----------|----------|
| Empty task list | Return error "No tasks available" |
| Rapid toggle operations | Each operation succeeds independently |
| Mark deleted task | Return "Task with ID X not found" |
| Very large task ID | Handled by standard validation |
| Task ID with leading zeros | Parse as integer (strips zeros) |
| Mark during view | Status updates immediately in memory |
| Special characters in title | Display correctly (unaffected by status) |
| All tasks completed | View shows all with "[✓] Completed" |
| No completed tasks | View shows all as pending |

---

## Out of Scope (Phase I)

- Completion history/audit trail
- Undo/redo functionality
- Bulk mark operations
- Scheduled/automatic completion
- Partial completion tracking
- Completion notifications
- Task dependency blocking
- Persistent storage

**Rationale**: Phase I constraint - in-memory console app only. These features deferred to future phases per Evolutionary Architecture principle.

---

## Summary

All technical unknowns resolved. Ready for Phase 1 (Design & Contracts).

**Key Takeaways**:
1. Boolean `completed` field sufficient for Phase I
2. Reuse existing Task/TaskList from 001-add-task
3. Two-phase validation (existence + status)
4. Idempotent operations with warnings
5. Separate CLI menu options for mark/unmark
6. Comprehensive test coverage (unit + integration)

**Constitutional Compliance**: ✅ All gates passed
