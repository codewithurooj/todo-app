# Implementation Tasks: Add Task Feature

**Feature**: 001-add-task
**Branch**: `001-add-task`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)
**Date**: 2025-12-06

---

## Overview

This document provides an ordered, testable breakdown of tasks for implementing the Add Task feature. Tasks are organized by user story to enable independent implementation and testing of each increment.

**Implementation Strategy**: MVP-first (User Story 1), then incremental delivery (US2, US3).

**Total Tasks**: 22 tasks across 5 phases

---

## User Story Mapping

| User Story | Priority | Tasks | Independent Test Criteria |
|------------|----------|-------|---------------------------|
| **US1**: Create Basic Task with Title Only | P1 | T006-T011 | Can create task with title, see it in list, verify ID/timestamp |
| **US2**: Create Task with Title and Description | P2 | T012-T014 | Can create task with description, verify both fields stored |
| **US3**: Handle Task Creation Errors Gracefully | P3 | T015-T019 | Invalid inputs rejected with clear errors, app remains stable |

---

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1 - P1) ← MVP - Can ship after this
    ↓
Phase 4 (US2 - P2) ← Enhancement
    ↓
Phase 5 (US3 - P3) ← Polish
    ↓
Phase 6 (Integration & Polish)
```

**Blocking Dependencies**:
- Phase 3+ require Phase 2 complete (Task and TaskList models)
- US2 and US3 require US1 complete (basic add functionality)

**Independent Stories**:
- US2 can be implemented independently of US3 (both depend only on US1)

---

## Parallel Execution Opportunities

### Phase 2 - Foundational (after T001-T005 complete)
- `T006 [P]` and `T007 [P]` - Different files, no shared state

### Phase 3 - User Story 1
- `T008 [P]` and `T009 [P]` - Test and implementation in different files
- `T010 [P]` and `T011 [P]` - Different components (service vs CLI)

### Phase 4 - User Story 2
- `T012 [P]` and `T013 [P]` - Test and implementation can run in parallel

### Phase 5 - User Story 3
- `T015 [P]`, `T016 [P]`, `T017 [P]` - Multiple validation tests for different error scenarios

### Phase 6 - Polish
- `T020 [P]` and `T021 [P]` - Documentation and integration tests independent

**Example Parallel Execution (Phase 3)**:
```bash
# Terminal 1
pytest tests/unit/test_task_model.py  # T008

# Terminal 2
# Implement TaskList.add_task() method  # T010

# Terminal 3
# Implement CLI add task handler  # T011
```

---

## Phase 1: Setup & Project Initialization

**Goal**: Bootstrap project structure and dependencies

**Independent Test**: Project can be initialized, dependencies installed, tests run (even if empty)

-[x] T001 Create project directory structure (src/, tests/, specs/)
-[x] T002 Initialize Python project with pyproject.toml and requirements.txt
-[x] T003 Configure pytest with pyproject.toml (test discovery, coverage)
-[x] T004 Configure code quality tools (ruff for linting, black for formatting, mypy for type checking)
-[x] T005 Create main.py application entry point with basic menu structure

**Files Created/Modified**:
- `src/`, `tests/unit/`, `tests/integration/`, `specs/001-add-task/`
- `pyproject.toml`, `requirements.txt`
- `main.py`
- `.github/workflows/` (optional CI/CD)

**Verification**:
```bash
python -m pytest --version  # pytest installed
ruff check src/  # linter runs
black --check src/  # formatter runs
mypy src/  # type checker runs
```

---

## Phase 2: Foundational Components

**Goal**: Implement core data models and validation (blocking prerequisites for all user stories)

**Independent Test**: Task and TaskList classes exist, can create tasks programmatically, validation works

### Task Model & Data Structures

-[x] T006 [P] Create Task dataclass in src/models/task.py with type hints (id, title, description, completed, created_at)
-[x] T007 [P] Create TaskList class in src/models/task.py with in-memory storage (_tasks list, _next_id counter)

**Files Created**: `src/models/__init__.py`, `src/models/task.py`

### Validation Logic

-[x] T008 Create validator functions in src/utils/validators.py (validate_title, validate_description)
-[x] T009 Write unit tests for validators in tests/unit/test_validators.py (empty title, too long, valid cases)

**Files Created**: `src/utils/__init__.py`, `src/utils/validators.py`, `tests/unit/test_validators.py`

**Verification**:
```python
# Can import and use
from src.models.task import Task, TaskList
from src.utils.validators import validate_title

# Validators work
assert validate_title("Valid Title")[0] == True
assert validate_title("")[0] == False
```

---

## Phase 3: User Story 1 - Create Basic Task with Title Only (P1 - MVP)

**Goal**: Implement core task creation with title only

**Story**: A user wants to quickly capture a task idea by entering just a title, without needing to provide additional details.

**Independent Test Criteria**:
✅ User can launch app, select "Add Task", enter title, see confirmation
✅ Task appears in task list with unique ID and timestamp
✅ Multiple tasks can be added in sequence with different IDs
✅ Tasks stored in memory until app exits

### Tests (TDD - Write First)

-[x] T010 [P] [US1] Write unit tests for Task dataclass in tests/unit/test_task_model.py (task creation, attribute access, immutability)
-[x] T011 [P] [US1] Write unit tests for TaskList.add_task() in tests/unit/test_task_model.py (ID generation, task storage, retrieval)

**Test File**: `tests/unit/test_task_model.py`

**Key Test Cases**:
```python
def test_create_task_with_title_only():
    """Task can be created with just a title"""

def test_task_id_auto_increment():
    """Sequential IDs assigned correctly"""

def test_task_default_completed_false():
    """New tasks start as incomplete"""
```

### Implementation

-[x] T012 [US1] Implement TaskList.add_task() method in src/models/task.py (create task, assign ID, append to list, return task)
-[x] T013 [US1] Implement TaskList.get_all_tasks() method in src/models/task.py (return copy of tasks list)
-[x] T014 [US1] Create CLI handler for add task in src/cli/task_cli.py (prompt for title, call validation, call add_task, display confirmation)
-[x] T015 [US1] Integrate add task handler into main menu in main.py (menu option, route to handler)

**Files Created**: `src/cli/__init__.py`, `src/cli/task_cli.py`
**Files Modified**: `main.py`, `src/models/task.py`

**Verification (Manual)**:
```bash
python main.py
# Select "1. Add Task"
# Enter title: "Buy groceries"
# See: "Task #1 created: Buy groceries"
# Select "2. View Tasks" (if implemented)
# See task in list
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_task_model.py -v
```

---

## Phase 4: User Story 2 - Create Task with Title and Description (P2)

**Goal**: Allow optional description field for tasks

**Story**: A user wants to add additional context to a task by providing both a title and a detailed description.

**Independent Test Criteria**:
✅ User can enter description after title
✅ Description is optional (can press Enter to skip)
✅ Both title and description stored correctly
✅ Multi-line descriptions accepted (up to 1000 chars)

### Tests (TDD - Write First)

-[x] T016 [P] [US2] Write unit tests for task with description in tests/unit/test_task_model.py (task with description, None description, empty string description)
-[x] T017 [P] [US2] Write unit tests for description validation in tests/unit/test_validators.py (valid, too long, None, empty)

**Key Test Cases**:
```python
def test_create_task_with_description():
    """Task stores description field correctly"""

def test_create_task_description_optional():
    """Task can be created with description=None"""

def test_description_max_length():
    """Description validation enforces 1000 char limit"""
```

### Implementation

-[x] T018 [US2] Update CLI add task handler in src/cli/task_cli.py (prompt for description, validate, pass to add_task)
-[x] T019 [US2] Update task display in view tasks handler to show description preview (first 50 chars)

**Files Modified**: `src/cli/task_cli.py`

**Verification (Manual)**:
```bash
python main.py
# Select "1. Add Task"
# Enter title: "Prepare presentation"
# Enter description: "Create slides for quarterly review"
# See: "Task #2 created: Prepare presentation"
# View tasks - see description preview
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_task_model.py::test_create_task_with_description -v
pytest tests/unit/test_validators.py::test_description_validation -v
```

---

## Phase 5: User Story 3 - Handle Task Creation Errors Gracefully (P3)

**Goal**: Validate inputs and provide clear error messages

**Story**: A user encounters an error during task creation and receives clear guidance on how to correct the issue.

**Independent Test Criteria**:
✅ Empty title rejected with clear error
✅ Title >200 chars rejected with char count
✅ Description >1000 chars rejected
✅ User can retry after validation error
✅ User can cancel task creation and return to menu

### Tests (TDD - Write First)

-[x] T020 [P] [US3] Write unit tests for empty title validation in tests/unit/test_validators.py
-[x] T021 [P] [US3] Write unit tests for title length validation in tests/unit/test_validators.py (boundary: 200 chars, 201 chars)
-[x] T022 [P] [US3] Write unit tests for description length validation in tests/unit/test_validators.py (boundary: 1000 chars, 1001 chars)

**Key Test Cases**:
```python
def test_empty_title_rejected():
    """Empty string and whitespace-only titles fail validation"""

def test_title_exactly_200_chars_accepted():
    """Boundary case: 200 chars is valid"""

def test_title_201_chars_rejected():
    """Boundary case: 201 chars is invalid"""
```

### Implementation

-[x] T023 [US3] Add validation to CLI add task handler in src/cli/task_cli.py (call validate_title, display errors, retry loop)
-[x] T024 [US3] Add description validation to CLI handler (call validate_description, display errors, retry loop)
-[x] T025 [US3] Implement cancel functionality in CLI handler (detect "cancel" input, discard task, return to menu)
-[x] T026 [US3] Add error message formatting helper in src/utils/validators.py (format validation errors consistently)

**Files Modified**: `src/cli/task_cli.py`, `src/utils/validators.py`

**Verification (Manual)**:
```bash
python main.py
# Select "1. Add Task"
# Enter title: "" (empty)
# See error: "Error: Task title cannot be empty. Please enter a title."
# Retry with valid title
# See success confirmation
```

**Verification (Automated)**:
```bash
pytest tests/unit/test_validators.py -v
```

---

## Phase 6: Integration Testing & Polish

**Goal**: End-to-end testing and cross-cutting concerns

**Independent Test Criteria**:
✅ Full user workflows work end-to-end
✅ Edge cases handled correctly
✅ Documentation complete and accurate

### Integration Tests

- [x] - T027 [P] Write integration test for full add task flow in tests/integration/test_add_task_flow.py (title only, with description, error handling, cancel)
- [x] - T028 [P] Write integration test for edge cases (unicode, special chars, rapid creation, whitespace trimming)

**Files Created**: `tests/integration/test_add_task_flow.py`

**Key Test Cases**:
```python
def test_full_add_task_title_only_flow(capsys):
    """End-to-end: Launch app -> Add task with title -> Confirm -> View"""

def test_add_task_with_unicode_title():
    """Edge case: Task title with emoji and international characters"""

def test_whitespace_trimming():
    """Title '  Task  ' stored as 'Task'"""
```

### Documentation & Polish

- [x] - T029 Add comprehensive docstrings to all classes and functions in src/
- [x] - T030 Update README.md with feature description, setup instructions, usage examples
- [x] - T031 Run code quality tools and fix all violations (ruff, black, mypy)
- [x] - T032 Measure and document test coverage (pytest-cov, aim for >90%)

**Files Modified**: All `src/` files, `README.md`

**Verification**:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
# Coverage should be >90%

ruff check src/
black --check src/
mypy src/
# All checks pass
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Deliver after Phase 3 (US1)**:
- ✅ Users can add tasks with title
- ✅ Tasks have unique IDs and timestamps
- ✅ Tasks stored in memory
- ✅ Basic menu system works

**Value**: Functional todo list that solves core use case

### Incremental Delivery

1. **Phase 3 Complete** → Ship MVP (title-only task creation)
2. **Phase 4 Complete** → Ship v1.1 (add description support)
3. **Phase 5 Complete** → Ship v1.2 (add validation and error handling)
4. **Phase 6 Complete** → Ship v1.3 (fully tested and polished)

### Recommended Development Order

**Week 1**: Setup + Foundational (T001-T009)
**Week 2**: US1 - MVP (T010-T015) → **Ship MVP**
**Week 3**: US2 - Description support (T016-T019) → **Ship v1.1**
**Week 4**: US3 - Error handling (T020-T026) + Integration (T027-T032) → **Ship v1.3**

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
-[x] T012 [US1] Implement TaskList.add_task() method in src/models/task.py
```

---

## Success Criteria Mapping

| Success Criterion | Validated By |
|-------------------|--------------|
| SC-001: Create task in <10s | Manual test after T015 |
| SC-002: Create task with description in <20s | Manual test after T019 |
| SC-003: 100% invalid inputs rejected | Unit tests T020-T022 |
| SC-004: 1000+ tasks without degradation | Performance test (not in scope) |
| SC-005: Users understand errors | Manual test after T026 |
| SC-006: 100% data integrity | Unit tests T010-T011 |
| SC-007: Cancel in <2s | Manual test after T025 |
| SC-008: Confirmation in <1s | Manual test after T015 |

---

## Summary

| Phase | Tasks | Description | Can Ship After |
|-------|-------|-------------|----------------|
| **Phase 1** | T001-T005 | Setup & Project Init | No (no features) |
| **Phase 2** | T006-T009 | Foundational (models, validation) | No (no UI) |
| **Phase 3** | T010-T015 | US1 - Basic Add Task (P1) | **Yes - MVP** |
| **Phase 4** | T016-T019 | US2 - Add Description (P2) | Yes - v1.1 |
| **Phase 5** | T020-T026 | US3 - Error Handling (P3) | Yes - v1.2 |
| **Phase 6** | T027-T032 | Integration & Polish | Yes - v1.3 (recommended) |

**Total**: 32 tasks organized into 6 phases
**MVP**: Achievable after 15 tasks (Phase 1-3)
**Parallel Opportunities**: 12 tasks can run in parallel
**Independent Stories**: US2 and US3 are independent (both depend only on US1)

---

**Status**: Ready for Implementation
**Next Command**: `/sp.implement` to begin TDD workflow
**Estimated Effort**: 2-4 weeks for full implementation (1 week for MVP)
