---
description: "Task list for View Tasks feature implementation"
---

# Tasks: View Tasks Feature

**Input**: Design documents from `/specs/004-view-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - skipping test generation per template guidelines

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (Python console app)
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

*No setup tasks needed - building on existing 001-add-task, 002-delete-task, and 003-update-task foundation*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T001 Create display formatting module src/lib/display.py with module docstring
- [ ] T002 [P] Implement truncate_title() function in src/lib/display.py
- [ ] T003 [P] Implement format_status() function in src/lib/display.py
- [ ] T004 [P] Implement format_timestamp() function in src/lib/display.py
- [ ] T005 [P] Implement format_task_list() function in src/lib/display.py
- [ ] T006 [P] Implement format_task_detail() function in src/lib/display.py
- [ ] T007 Extend TaskList with get_all_tasks() method in src/models/task.py
- [ ] T008 Extend TaskList with get_task_by_id() method in src/models/task.py
- [ ] T009 Extend TaskList with filter_tasks_by_status() method in src/models/task.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can view all tasks in their task list with ID, title, and status displayed in a clear format

**Independent Test**: Create multiple tasks with varying titles, descriptions, and statuses. View all tasks and verify all fields display correctly with proper formatting (ID, title truncated if >50 chars, status icon).

### Implementation for User Story 1

- [ ] T010 [US1] Create view_all_tasks_cli() function in src/cli/todo_cli.py
- [ ] T011 [US1] Implement task retrieval using TaskList.get_all_tasks() in view_all_tasks_cli()
- [ ] T012 [US1] Implement display formatting using format_task_list() with context="all" in view_all_tasks_cli()
- [ ] T013 [US1] Add console output for formatted task list in view_all_tasks_cli()
- [ ] T014 [US1] Add "View All Tasks" menu option to main menu in src/cli/menu.py
- [ ] T015 [US1] Wire view_all_tasks_cli() to menu selection in main.py

**Checkpoint**: At this point, User Story 1 (View All Tasks) should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Empty Task List (Priority: P1)

**Goal**: Users see a helpful message when their task list is empty so they understand there are no tasks

**Independent Test**: Start with an empty task list and verify the empty state message displays correctly. Then add tasks, delete them all, and verify the message reappears.

### Implementation for User Story 2

- [ ] T016 [US2] Implement empty list check in view_all_tasks_cli() in src/cli/todo_cli.py
- [ ] T017 [US2] Add empty list message handling in format_task_list() for context="all" in src/lib/display.py
- [ ] T018 [US2] Verify empty list message displays correctly when no tasks exist in view_all_tasks_cli()

**Checkpoint**: At this point, User Stories 1 AND 2 (View All + Empty State) should both work independently

---

## Phase 5: User Story 3 - View Single Task Details (Priority: P2)

**Goal**: Users can view complete details of a single task without truncation, including full title, description, status, and timestamps

**Independent Test**: Create tasks with various description lengths. View details for each and verify all fields display completely. Test with invalid IDs to verify error handling.

### Implementation for User Story 3

- [ ] T019 [US3] Create view_task_details_cli() function in src/cli/todo_cli.py
- [ ] T020 [US3] Add task ID prompt "Enter task ID: " in view_task_details_cli()
- [ ] T021 [US3] Integrate validate_task_id() from utils.validators into view_task_details_cli()
- [ ] T022 [US3] Implement invalid ID format error handling in view_task_details_cli()
- [ ] T023 [US3] Implement invalid ID range error handling (zero, negative) in view_task_details_cli()
- [ ] T024 [US3] Implement task retrieval using TaskList.get_task_by_id() in view_task_details_cli()
- [ ] T025 [US3] Implement task not found error handling with specific ID in message in view_task_details_cli()
- [ ] T026 [US3] Implement detail display using format_task_detail() in view_task_details_cli()
- [ ] T027 [US3] Add console output for formatted task details in view_task_details_cli()
- [ ] T028 [US3] Add "View Task Details" menu option to main menu in src/cli/menu.py
- [ ] T029 [US3] Wire view_task_details_cli() to menu selection in main.py

**Checkpoint**: At this point, all P1 and User Story 3 (Detail View) should be independently functional

---

## Phase 6: User Story 4 - Filter Tasks by Status (Priority: P2)

**Goal**: Users can filter tasks by completion status (completed or pending) to focus on relevant tasks

**Independent Test**: Create mix of completed and pending tasks. Test each filter option and verify only matching tasks appear. Verify messages for empty filter results.

### Implementation for User Story 4

- [ ] T030 [P] [US4] Create view_pending_tasks_cli() function in src/cli/todo_cli.py
- [ ] T031 [P] [US4] Create view_completed_tasks_cli() function in src/cli/todo_cli.py
- [ ] T032 [US4] Implement pending filter using TaskList.filter_tasks_by_status(completed=False) in view_pending_tasks_cli()
- [ ] T033 [US4] Implement completed filter using TaskList.filter_tasks_by_status(completed=True) in view_completed_tasks_cli()
- [ ] T034 [US4] Implement display formatting using format_task_list() with context="pending" in view_pending_tasks_cli()
- [ ] T035 [US4] Implement display formatting using format_task_list() with context="completed" in view_completed_tasks_cli()
- [ ] T036 [US4] Add empty pending list message "No pending tasks found." in format_task_list() in src/lib/display.py
- [ ] T037 [US4] Add empty completed list message "No completed tasks found." in format_task_list() in src/lib/display.py
- [ ] T038 [US4] Add console output for pending tasks in view_pending_tasks_cli()
- [ ] T039 [US4] Add console output for completed tasks in view_completed_tasks_cli()
- [ ] T040 [US4] Add "View Pending Tasks" menu option to main menu in src/cli/menu.py
- [ ] T041 [US4] Add "View Completed Tasks" menu option to main menu in src/cli/menu.py
- [ ] T042 [US4] Wire view_pending_tasks_cli() to menu selection in main.py
- [ ] T043 [US4] Wire view_completed_tasks_cli() to menu selection in main.py

**Checkpoint**: All P1 and P2 user stories (View All, Empty State, Details, Filters) should be independently functional

---

## Phase 7: User Story 5 - Handle View Errors Gracefully (Priority: P2)

**Goal**: Users receive clear error messages when viewing operations fail and can recover without frustration

**Independent Test**: Test all invalid inputs (non-numeric, negative, zero, non-existent IDs) and verify appropriate error messages. Verify application remains stable after errors.

### Implementation for User Story 5

- [ ] T044 [US5] Enhance non-numeric ID error message with clear format guidance in view_task_details_cli()
- [ ] T045 [US5] Enhance negative/zero ID error message with clear range guidance in view_task_details_cli()
- [ ] T046 [US5] Enhance non-existent ID error message to include the specific ID attempted in view_task_details_cli()
- [ ] T047 [US5] Verify all error paths return to main menu without modifying data in view_task_details_cli()
- [ ] T048 [US5] Add error recovery test for invalid input handling in view_task_details_cli()
- [ ] T049 [US5] Handle task ID with leading zeros (e.g., "007" → 7) correctly in view_task_details_cli()

**Checkpoint**: Error handling complete - all error scenarios handled gracefully

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 [P] Add docstrings to all formatting functions in src/lib/display.py
- [ ] T051 [P] Add docstrings to all view CLI functions in src/cli/todo_cli.py
- [ ] T052 [P] Add docstrings to all TaskList query methods in src/models/task.py
- [ ] T053 [P] Add type hints to all formatting functions in src/lib/display.py
- [ ] T054 [P] Add type hints to all view CLI functions in src/cli/todo_cli.py
- [ ] T055 [P] Add type hints to all TaskList query methods in src/models/task.py
- [ ] T056 [P] Update README.md with View Tasks feature documentation
- [ ] T057 [P] Add code comments for complex formatting logic in src/lib/display.py
- [ ] T058 Verify PEP 8 compliance with ruff for all modified files
- [ ] T059 Run manual testing per quickstart.md validation scenarios
- [ ] T060 Test special characters and unicode in titles/descriptions for display
- [ ] T061 Test edge cases from spec.md (empty list, very long titles, special chars)
- [ ] T062 Test display with 100+ tasks to verify performance goals (<2s)
- [ ] T063 Verify consistent formatting across all view types (all/pending/completed)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Skipped - building on existing foundation
- **Foundational (Phase 2)**: No dependencies - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on US1 (Phase 3) - enhances empty state handling
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) - Can run parallel to US1/US2
- **User Story 4 (Phase 6)**: Depends on Foundational (Phase 2) - Can run parallel to US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on US3 (Phase 5) - enhances error handling for detail view
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - View All Tasks**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1) - Empty List Message**: Depends on US1 (enhances US1 with empty state)
- **User Story 3 (P2) - View Task Details**: Can start after Foundational - No dependencies on other stories (parallel to US1/US2)
- **User Story 4 (P2) - Filter by Status**: Can start after Foundational - No dependencies on other stories (parallel to US1/US2/US3)
- **User Story 5 (P2) - Error Handling**: Depends on US3 (enhances detail view errors)

### Within Each User Story

- Foundational display functions before CLI implementation
- TaskList query methods before CLI calls them
- Core implementation before error handling enhancements
- Validation integration before error messages
- Story complete before moving to next priority

### Parallel Opportunities

- **Foundational Phase (Phase 2)**: T002, T003, T004, T005, T006 can run in parallel (different functions in display.py)
- **User Stories Start**: After Phase 2 completes:
  - US1 (Phase 3) must complete first (establishes view pattern)
  - US2 (Phase 4) enhances US1, runs after US1
  - US3 (Phase 5), US4 (Phase 6) can start after Phase 2 and run in parallel
- **Within US4**: T030 and T031 can run in parallel (different CLI functions)
- **Within US4**: T034 and T035 can run in parallel (same function, different context)
- **Polish Phase (Phase 8)**: T050-T057 can run in parallel (different files/functions)

---

## Parallel Example: Foundational Phase

```bash
# Launch foundational display functions together:
Task T002: "Implement truncate_title() in src/lib/display.py"
Task T003: "Implement format_status() in src/lib/display.py"
Task T004: "Implement format_timestamp() in src/lib/display.py"
Task T005: "Implement format_task_list() in src/lib/display.py"
Task T006: "Implement format_task_detail() in src/lib/display.py"

# All work on different functions in same file - coordinate merging
```

## Parallel Example: User Stories (after Foundational complete)

```bash
# After US1 and US2 complete, launch detail view and filters in parallel:
Developer A: Phase 5 (US3 - View Task Details) - T019 through T029
Developer B: Phase 6 (US4 - Filter by Status) - T030 through T043

# Each story is independently testable
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only - Both P1)

1. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
2. Complete Phase 3: User Story 1 (View All Tasks)
3. Complete Phase 4: User Story 2 (Empty List Message)
4. **STOP and VALIDATE**: Test US1 and US2 independently
5. Deploy/demo basic view functionality (see all tasks, handle empty state)

### Incremental Delivery

1. Complete Foundational → Foundation ready
2. Add User Story 1 (View All) → Test independently → Deploy/Demo
3. Add User Story 2 (Empty State) → Test independently → **MVP DEMO** with P1 features!
4. Add User Story 3 (Details) → Test independently → Deploy/Demo
5. Add User Story 4 (Filters) → Test independently → Deploy/Demo
6. Add User Story 5 (Error Handling) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Foundational together (Phase 2)
2. Developer A completes US1 (Phase 3)
3. Developer A completes US2 (Phase 4) - depends on US1
4. Once Foundational done:
   - Developer B: User Story 3 (Details) - can start early
   - Developer C: User Story 4 (Filters) - can start early
5. After US3 complete:
   - Developer B: User Story 5 (Error Handling)
6. Stories complete and integrate independently

---

## Task Count Summary

- **Phase 2 (Foundational)**: 9 tasks (T001-T009)
- **Phase 3 (US1 - View All Tasks, P1)**: 6 tasks (T010-T015)
- **Phase 4 (US2 - Empty List Message, P1)**: 3 tasks (T016-T018)
- **Phase 5 (US3 - View Task Details, P2)**: 11 tasks (T019-T029)
- **Phase 6 (US4 - Filter by Status, P2)**: 14 tasks (T030-T043)
- **Phase 7 (US5 - Error Handling, P2)**: 6 tasks (T044-T049)
- **Phase 8 (Polish)**: 14 tasks (T050-T063)

**Total Tasks**: 63 tasks

**Parallel Opportunities**: 5 display functions (same file), 2 CLI functions (different files), 6 documentation tasks (different scopes)

**MVP Scope**: Foundational + US1 + US2 = 9 + 6 + 3 = 18 tasks (29% of total)

---

## Notes

- [P] tasks = different files or safely parallelizable
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests not included per specification (not explicitly requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks reuse existing Task and TaskList entities from 001-add-task
- All tasks reuse existing validate_task_id() from 002-delete-task
- Focus on smallest viable changes per task
- New display.py module keeps formatting logic separate from data model
