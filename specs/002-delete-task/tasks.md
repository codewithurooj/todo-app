# Implementation Tasks: Delete Task Feature

**Feature**: 002-delete-task
**Branch**: `002-delete-task`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)
**Date**: 2025-12-06

---

## Overview

This document provides an ordered, testable breakdown of tasks for implementing the Delete Task feature. Tasks are organized by user story to enable independent implementation and testing of each increment.

**Implementation Strategy**: MVP-first (User Story 1), then incremental delivery (US2, US3).

**Total Tasks**: 20 tasks across 4 phases

---

## User Story Mapping

| User Story | Priority | Tasks | Independent Test Criteria |
|------------|----------|-------|---------------------------|
| **US1**: Delete Task by ID | P1 | T001-T007 | Can delete task by ID, see confirmation, verify task removed from list |
| **US2**: Handle Delete Errors Gracefully | P2 | T008-T013 | Invalid inputs rejected with clear errors, empty list handled, app remains stable |
| **US3**: Delete Confirmation for Safety | P3 | T014-T017 | Confirmation prompt appears, can confirm/cancel, task deleted only on confirm |

---

## Dependencies

```
Phase 1 (US1 - P1) ← MVP - Can ship after this
    ↓
Phase 2 (US2 - P2) ← Enhanced error handling
    ↓
Phase 3 (US3 - P3) ← Safety confirmation
    ↓
Phase 4 (Integration & Polish)
```

**Blocking Dependencies**:
- All user stories require 001-add-task feature complete (Task and TaskList models exist)
- US2 and US3 require US1 complete (basic delete functionality)

**Independent Stories**:
- US2 can be implemented independently of US3 (both depend only on US1)

---

## Parallel Execution Opportunities

### Phase 1 - User Story 1
- `T001 [P]` and `T002 [P]` - Test and implementation in different files
- `T004 [P]` and `T005 [P]` - CLI tests vs service tests

### Phase 2 - User Story 2
- `T008 [P]`, `T009 [P]`, `T010 [P]` - Multiple validation tests for different error scenarios
- `T011 [P]` and `T012 [P]` - Different validation scenarios

### Phase 3 - User Story 3
- `T014 [P]` and `T015 [P]` - Test and implementation can run in parallel

### Phase 4 - Polish
- `T018 [P]` and `T019 [P]` - Documentation and integration tests independent

**Example Parallel Execution (Phase 1)**:
```bash
# Terminal 1
pytest tests/unit/test_task_service.py::test_delete_task  # T001

# Terminal 2
# Implement TaskList.delete_task() method  # T002

# Terminal 3
pytest tests/unit/test_delete_cli.py  # T004
```

---

## Phase 1: User Story 1 - Delete Task by ID (P1 - MVP)

**Goal**: Implement core task deletion by ID

**Story**: A user wants to remove a completed or unwanted task from their list by specifying its unique identifier.

**Independent Test Criteria**:
✅ User can launch app, select "Delete Task", enter valid ID, see confirmation
✅ Task is removed from list and no longer appears
✅ Remaining tasks retain their original IDs (no renumbering)
✅ Can delete first task, last task, middle task, only task

### Tests (TDD - Write First)

- [X] T001 [P] [US1] Write unit tests for TaskList.delete_task() in tests/unit/test_task_service.py (delete existing task, verify removal, ID preservation)
- [X] T002 [P] [US1] Write unit tests for delete validation in tests/unit/test_task_service.py (task exists check, empty list handling)
- [X] T003 [US1] Write unit tests for task ID preservation in tests/unit/test_task_service.py (verify remaining IDs unchanged after deletion)
- [X] T004 [P] [US1] Write unit tests for CLI delete handler in tests/unit/test_delete_cli.py (valid ID input, success message display)

**Test Files**: `tests/unit/test_task_service.py`, `tests/unit/test_delete_cli.py`

**Key Test Cases**:
```python
def test_delete_existing_task():
    """Task with valid ID is removed from list"""

def test_delete_preserves_remaining_ids():
    """After deleting task #2 from [1, 2, 3], result is [1, 3]"""

def test_delete_only_task_results_in_empty_list():
    """Deleting last task leaves empty list"""

def test_delete_success_message_includes_id_and_title():
    """Confirmation shows: Task #5 'Meeting' deleted successfully"""
```

### Implementation

- [X] T005 [US1] Implement TaskList.delete_task(task_id) method in src/models/task.py (find task, remove from list, return success/error tuple)
- [X] T006 [US1] Create CLI handler handle_delete_task() in src/cli/task_cli.py (prompt for ID, validate input, call delete_task, display confirmation)
- [X] T007 [US1] Integrate delete handler into main menu in main.py (add "Delete Task" option, route to handler)

**Files Created**: `src/cli/task_cli.py` (if not exists from add task)
**Files Modified**: `src/models/task.py`, `main.py`

**Verification (Manual)**:
```bash
python main.py
# Add tasks first (IDs 1, 2, 3)
# Select "Delete Task"
# Enter ID: 2
# See: "Task #2 'Task Title' deleted successfully"
# View tasks - only IDs 1 and 3 remain
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_task_service.py::test_delete_existing_task -v
pytest tests/unit/test_delete_cli.py -v
```

---

## Phase 2: User Story 2 - Handle Delete Errors Gracefully (P2)

**Goal**: Validate delete operations and provide clear error messages

**Story**: A user attempts to delete a task that doesn't exist or provides invalid input, and receives clear guidance on how to correct the issue.

**Independent Test Criteria**:
✅ Non-existent task ID rejected with specific error
✅ Non-numeric input rejected with clear error
✅ Empty input rejected with clear error
✅ Empty task list handled gracefully
✅ User can cancel deletion operation

### Tests (TDD - Write First)

- [X] T008 [P] [US2] Write unit tests for non-existent task ID in tests/unit/test_task_service.py (attempt delete of ID 99, verify error message)
- [X] T009 [P] [US2] Write unit tests for invalid input validation in tests/unit/test_delete_cli.py (non-numeric, empty, special characters)
- [X] T010 [P] [US2] Write unit tests for empty list scenario in tests/unit/test_task_service.py (delete on empty list returns error)
- [X] T011 [P] [US2] Write unit tests for cancel operation in tests/unit/test_delete_cli.py (user types "cancel", operation aborted)
- [X] T012 [P] [US2] Write unit tests for leading zeros in tests/unit/test_delete_cli.py (ID "007" interpreted as 7)

**Key Test Cases**:
```python
def test_delete_nonexistent_task_returns_error():
    """Attempting to delete ID 99 returns error message"""

def test_delete_with_non_numeric_input_rejected():
    """Input 'abc' rejected with clear error"""

def test_delete_on_empty_list_shows_no_tasks_message():
    """Empty list returns 'No tasks available to delete'"""

def test_cancel_delete_operation():
    """Typing 'cancel' aborts deletion and returns to menu"""

def test_leading_zeros_stripped():
    """ID '005' treated as 5"""
```

### Implementation

- [X] T013 [US2] Add input validation to CLI delete handler in src/cli/task_cli.py (check numeric, check empty, check cancel, strip leading zeros, display errors)

**Files Modified**: `src/cli/task_cli.py`

**Verification (Manual)**:
```bash
python main.py
# Try deleting non-existent ID: 99
# See: "Error: Task #99 not found. Please enter a valid task ID."
# Try non-numeric input: abc
# See: "Error: Invalid task ID. Please enter a numeric ID."
# Try cancel: cancel
# See: "Delete operation cancelled"
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_task_service.py::test_delete_nonexistent_task -v
pytest tests/unit/test_delete_cli.py -v
```

---

## Phase 3: User Story 3 - Delete Confirmation for Safety (P3)

**Goal**: Add confirmation prompt before deletion to prevent accidental removals

**Story**: A user is prompted to confirm deletion before a task is permanently removed, preventing accidental deletions.

**Independent Test Criteria**:
✅ Confirmation prompt appears with task ID and title
✅ User can confirm with y/yes (case-insensitive)
✅ User can cancel with n/no (case-insensitive)
✅ Invalid confirmation input re-prompts
✅ Task deleted only on confirmation

### Tests (TDD - Write First)

- [X] T014 [P] [US3] Write unit tests for confirmation prompt in tests/unit/test_delete_cli.py (prompt appears with task details)
- [X] T015 [P] [US3] Write unit tests for confirmation responses in tests/unit/test_delete_cli.py (y/yes confirms, n/no cancels, case-insensitive)
- [X] T016 [US3] Write unit tests for invalid confirmation input in tests/unit/test_delete_cli.py (re-prompts on invalid input)

**Key Test Cases**:
```python
def test_confirmation_prompt_displays_task_details():
    """Prompt shows: Delete task #5: 'Meeting'? (y/n):"""

def test_confirmation_yes_deletes_task():
    """Input 'y' or 'yes' (any case) proceeds with deletion"""

def test_confirmation_no_cancels_deletion():
    """Input 'n' or 'no' (any case) cancels, task remains"""

def test_invalid_confirmation_input_reprompts():
    """Input 'maybe' shows error and re-prompts"""
```

### Implementation

- [X] T017 [US3] Add confirmation prompt to CLI delete handler in src/cli/task_cli.py (display task details, prompt for y/n, validate response, delete only on yes)

**Files Modified**: `src/cli/task_cli.py`

**Verification (Manual)**:
```bash
python main.py
# Add task "Important meeting"
# Select "Delete Task", enter ID
# See prompt: "Delete task #1: 'Important meeting'? (y/n):"
# Enter: n
# See: "Deletion cancelled"
# Task still in list
# Try again, enter: y
# See: "Task #1 'Important meeting' deleted successfully"
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_delete_cli.py::test_confirmation -v
```

---

## Phase 4: Integration Testing & Polish

**Goal**: End-to-end testing and documentation

**Independent Test Criteria**:
✅ Full user workflows work end-to-end
✅ Edge cases handled correctly
✅ Documentation complete and accurate

### Integration Tests

- [X] T018 [P] Write integration test for full delete flow in tests/integration/test_delete_task_flow.py (add task, delete, verify removal, check list)
- [X] T019 [P] Write integration test for edge cases in tests/integration/test_delete_task_flow.py (delete first/last/only task, rapid deletions, special IDs)

**Files Created**: `tests/integration/test_delete_task_flow.py`

**Key Test Cases**:
```python
def test_full_delete_flow_end_to_end(capsys):
    """Add task → Delete → Confirm → Verify removed"""

def test_delete_first_task_from_list():
    """Deleting first task works correctly"""

def test_delete_last_task_from_list():
    """Deleting last task works correctly"""

def test_delete_only_task_results_in_empty_list():
    """Deleting only task shows 'No tasks available'"""
```

### Documentation & Polish

- [X] T020 Update README.md with delete feature description and usage examples

**Files Modified**: `README.md`

**Verification**:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
# Coverage should be >90%
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Deliver after Phase 1 (US1)**:
- ✅ Users can delete tasks by ID
- ✅ Remaining tasks retain IDs (no renumbering)
- ✅ Success confirmation displayed
- ✅ Basic delete menu option works

**Value**: Functional task deletion that solves core use case

### Incremental Delivery

1. **Phase 1 Complete** → Ship MVP (basic delete by ID)
2. **Phase 2 Complete** → Ship v1.1 (add error handling and validation)
3. **Phase 3 Complete** → Ship v1.2 (add confirmation prompts)
4. **Phase 4 Complete** → Ship v1.3 (fully tested and polished)

### Recommended Development Order

**Week 1**: US1 - Basic delete (T001-T007) → **Ship MVP**
**Week 2**: US2 - Error handling (T008-T013) → **Ship v1.1**
**Week 3**: US3 - Confirmation (T014-T017) + Integration (T018-T020) → **Ship v1.3**

---

## Task Format Validation

All tasks follow the required checklist format:

✅ **Checkbox**: Every task starts with `- [ ]`
✅ **Task ID**: Sequential T001, T002, etc.
✅ **[P] marker**: Present on parallelizable tasks
✅ **[Story] label**: Present on user story tasks (US1, US2, US3)
✅ **Description**: Clear action with exact file path

**Example**:
```
- [X] T005 [US1] Implement TaskList.delete_task(task_id) method in src/models/task.py
```

---

## Success Criteria Mapping

| Success Criterion | Validated By |
|-------------------|--------------|
| SC-001: Delete task in <10s | Manual test after T007 |
| SC-002: 100% invalid inputs rejected | Unit tests T008-T012 |
| SC-003: ID preservation works | Unit test T003 |
| SC-004: Empty list handled | Unit test T010 |
| SC-005: Confirmation prevents accidents | Unit tests T014-T016 |
| SC-006: Users understand errors | Manual test after T013 |
| SC-007: Cancel works | Unit test T011 |
| SC-008: Confirmation in <1s | Manual test after T017 |

---

## Dependencies with Other Features

**Requires**:
- **001-add-task**: Task and TaskList models must exist

**Enables**:
- **003-update-task**: Delete operation pattern reusable
- **004-view-task**: Updated list reflects deletions
- **005-mark-complete**: Deleted tasks cannot be marked

**Integration Points**:
- Extends `TaskList` class from 001-add-task
- Uses same `Task` entity model
- Integrates with main menu from 001-add-task

---

## Summary

| Phase | Tasks | Description | Can Ship After |
|-------|-------|-------------|----------------|
| **Phase 1** | T001-T007 | US1 - Basic Delete (P1) | **Yes - MVP** |
| **Phase 2** | T008-T013 | US2 - Error Handling (P2) | Yes - v1.1 |
| **Phase 3** | T014-T017 | US3 - Confirmation (P3) | Yes - v1.2 |
| **Phase 4** | T018-T020 | Integration & Polish | Yes - v1.3 (recommended) |

**Total**: 20 tasks organized into 4 phases
**MVP**: Achievable after 7 tasks (Phase 1)
**Parallel Opportunities**: 11 tasks can run in parallel
**Independent Stories**: US2 and US3 are independent (both depend only on US1)

---

**Status**: Ready for Implementation
**Next Command**: `/sp.implement` to begin TDD workflow
**Estimated Effort**: 1-2 weeks for full implementation (1 week for MVP)
