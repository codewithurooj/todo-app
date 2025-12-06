---
description: "Task list for Mark Task Complete feature implementation"
---

# Tasks: Mark Task Complete Feature

**Input**: Design documents from `/specs/005-mark-complete/`
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

*No setup tasks needed - building on existing 001-add-task, 002-delete-task, 003-update-task, and 004-view-task foundation*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T001 Extend TaskList with mark_complete() method in src/models/tasklist.py
- [ ] T002 Extend TaskList with unmark_complete() method in src/models/tasklist.py
- [ ] T003 Implement task_id validation in mark_complete() method in src/models/tasklist.py
- [ ] T004 Implement task_id validation in unmark_complete() method in src/models/tasklist.py
- [ ] T005 Implement idempotent behavior for already-completed tasks in mark_complete() in src/models/tasklist.py
- [ ] T006 Implement idempotent behavior for already-pending tasks in unmark_complete() in src/models/tasklist.py
- [ ] T007 Implement atomic update of completed field and updated_at timestamp in mark_complete() in src/models/tasklist.py
- [ ] T008 Implement atomic update of completed field and updated_at timestamp in unmark_complete() in src/models/tasklist.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Mark Pending Task as Complete (Priority: P1) 🎯 MVP

**Goal**: Users can mark pending tasks as complete to track which tasks they have finished

**Independent Test**: Create pending task, mark complete, verify status changes to "Completed" and timestamp updates correctly.

### Implementation for User Story 1

- [ ] T009 [US1] Create handle_mark_complete() function in src/cli/handlers.py
- [ ] T010 [US1] Add task ID prompt "Enter task ID to mark complete: " in handle_mark_complete()
- [ ] T011 [US1] Integrate validate_task_id() from utils.validators into handle_mark_complete()
- [ ] T012 [US1] Implement invalid ID format error handling in handle_mark_complete()
- [ ] T013 [US1] Implement invalid ID range error handling (zero, negative) in handle_mark_complete()
- [ ] T014 [US1] Call TaskList.mark_complete() with validated task_id in handle_mark_complete()
- [ ] T015 [US1] Display success message from mark_complete() response in handle_mark_complete()
- [ ] T016 [US1] Display error message from mark_complete() response in handle_mark_complete()
- [ ] T017 [US1] Display idempotent warning message when task already completed in handle_mark_complete()
- [ ] T018 [US1] Return to main menu after mark complete operation in handle_mark_complete()
- [ ] T019 [US1] Add "Mark Task Complete" menu option to main menu in src/cli/menu.py
- [ ] T020 [US1] Wire handle_mark_complete() to menu selection in main.py

**Checkpoint**: At this point, User Story 1 (Mark Complete) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Unmark Completed Task to Reopen (Priority: P1)

**Goal**: Users can unmark completed tasks to reopen them and resume work on tasks needing more attention

**Independent Test**: Complete a task, reopen it, verify status returns to "Pending" and timestamp updates.

### Implementation for User Story 2

- [ ] T021 [US2] Create handle_reopen_task() function in src/cli/handlers.py
- [ ] T022 [US2] Add task ID prompt "Enter task ID to reopen: " in handle_reopen_task()
- [ ] T023 [US2] Integrate validate_task_id() from utils.validators into handle_reopen_task()
- [ ] T024 [US2] Implement invalid ID format error handling in handle_reopen_task()
- [ ] T025 [US2] Implement invalid ID range error handling (zero, negative) in handle_reopen_task()
- [ ] T026 [US2] Call TaskList.unmark_complete() with validated task_id in handle_reopen_task()
- [ ] T027 [US2] Display success message from unmark_complete() response in handle_reopen_task()
- [ ] T028 [US2] Display error message from unmark_complete() response in handle_reopen_task()
- [ ] T029 [US2] Display idempotent warning message when task already pending in handle_reopen_task()
- [ ] T030 [US2] Return to main menu after reopen operation in handle_reopen_task()
- [ ] T031 [US2] Add "Reopen Completed Task" menu option to main menu in src/cli/menu.py
- [ ] T032 [US2] Wire handle_reopen_task() to menu selection in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 (Mark Complete + Reopen) should both work independently

---

## Phase 5: User Story 3 - Handle Invalid Operations (Priority: P2)

**Goal**: Users receive clear error messages when operations fail so they understand what went wrong

**Independent Test**: Attempt invalid operations (non-existent IDs, invalid formats), verify error messages appear without crashes.

### Implementation for User Story 3

- [ ] T033 [US3] Enhance non-existent task error message with specific task ID in handle_mark_complete()
- [ ] T034 [US3] Enhance non-existent task error message with specific task ID in handle_reopen_task()
- [ ] T035 [US3] Add task ID with leading zeros handling (e.g., "007" → 7) in handle_mark_complete()
- [ ] T036 [US3] Add task ID with leading zeros handling (e.g., "007" → 7) in handle_reopen_task()
- [ ] T037 [US3] Implement empty task list check at start of mark complete flow in handle_mark_complete()
- [ ] T038 [US3] Implement empty task list check at start of reopen flow in handle_reopen_task()
- [ ] T039 [US3] Verify all error paths return to main menu without data corruption in handle_mark_complete()
- [ ] T040 [US3] Verify all error paths return to main menu without data corruption in handle_reopen_task()
- [ ] T041 [US3] Add clear error message formatting for all validation failures in handle_mark_complete()
- [ ] T042 [US3] Add clear error message formatting for all validation failures in handle_reopen_task()

**Checkpoint**: Error handling complete - all error scenarios handled gracefully

---

## Phase 6: Integration & Verification

**Purpose**: Ensure mark complete integrates correctly with existing features

- [ ] T043 Verify mark complete updates are reflected in View All Tasks from 004-view-task
- [ ] T044 Verify mark complete updates are reflected in View Task Details from 004-view-task
- [ ] T045 Verify mark complete updates are reflected in Filter Pending Tasks from 004-view-task
- [ ] T046 Verify mark complete updates are reflected in Filter Completed Tasks from 004-view-task
- [ ] T047 Verify completed field is preserved when using Update Task from 003-update-task
- [ ] T048 Verify marking complete doesn't affect task ID, title, description, or created_at fields
- [ ] T049 Verify timestamp updates are accurate within ±1 second per success criteria
- [ ] T050 Test rapid toggle operations (mark complete → reopen → mark complete)
- [ ] T051 Verify all tasks completed scenario displays correctly in filters
- [ ] T052 Verify no completed tasks scenario displays correctly in filters

**Checkpoint**: Integration verified - mark complete works seamlessly with all existing features

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T053 [P] Add docstrings to mark_complete() method in src/models/tasklist.py
- [ ] T054 [P] Add docstrings to unmark_complete() method in src/models/tasklist.py
- [ ] T055 [P] Add docstrings to handle_mark_complete() function in src/cli/handlers.py
- [ ] T056 [P] Add docstrings to handle_reopen_task() function in src/cli/handlers.py
- [ ] T057 [P] Add type hints to mark_complete() method signature in src/models/tasklist.py
- [ ] T058 [P] Add type hints to unmark_complete() method signature in src/models/tasklist.py
- [ ] T059 [P] Add type hints to handle_mark_complete() function in src/cli/handlers.py
- [ ] T060 [P] Add type hints to handle_reopen_task() function in src/cli/handlers.py
- [ ] T061 [P] Update README.md with Mark Complete feature documentation
- [ ] T062 [P] Add code comments for idempotent behavior logic in mark_complete()
- [ ] T063 [P] Add code comments for idempotent behavior logic in unmark_complete()
- [ ] T064 Verify PEP 8 compliance with ruff for all modified files
- [ ] T065 Run manual testing per quickstart.md validation scenarios
- [ ] T066 Test special characters in titles with completion status display
- [ ] T067 Test edge cases from spec.md (empty list, rapid toggles, deleted tasks)
- [ ] T068 Verify performance goals (<1 second for status changes)
- [ ] T069 Test completion status with 100+ tasks to verify scale

**Checkpoint**: All polish tasks complete - feature ready for production

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Skipped - building on existing foundation
- **Foundational (Phase 2)**: No dependencies - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - Can run parallel to US1
- **User Story 3 (Phase 5)**: Depends on US1 and US2 (Phase 3 & 4) - enhances error handling for both
- **Integration (Phase 6)**: Depends on US1 and US2 being complete
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Mark Complete**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1) - Reopen Task**: Can start after Foundational - No dependencies on other stories (parallel to US1)
- **User Story 3 (P2) - Error Handling**: Depends on US1 and US2 (enhances error handling for both operations)

### Within Each User Story

- Foundational TaskList methods before CLI handlers
- CLI handlers before menu integration
- Validation before method calls
- Error handling after core implementation
- Menu wiring after handler complete
- Story complete before moving to next priority

### Parallel Opportunities

- **Foundational Phase (Phase 2)**: T001 and T002 can run in parallel (different methods, same file - coordinate merge)
- **User Stories Start**: After Phase 2 completes:
  - US1 (Phase 3) and US2 (Phase 4) can start in parallel - both are P1 and independent
  - Different CLI handlers, different menu options
- **Within US3**: T033-T034, T035-T036, T037-T038, T039-T040, T041-T042 can run in pairs (one for mark, one for reopen)
- **Integration Phase (Phase 6)**: T043-T046 can run in parallel (different view operations)
- **Polish Phase (Phase 7)**: T053-T060 can run in parallel (different functions), T061-T063 can run in parallel (different scopes)

---

## Parallel Example: Foundational Phase

```bash
# Launch foundational methods together (careful merge - same file):
Task T001: "Extend TaskList with mark_complete() method"
Task T002: "Extend TaskList with unmark_complete() method"

# Both modify src/models/tasklist.py - coordinate merging
```

## Parallel Example: User Stories (after Foundational complete)

```bash
# Launch mark and reopen in parallel (different developers):
Developer A: Phase 3 (US1 - Mark Complete) - T009 through T020
Developer B: Phase 4 (US2 - Reopen Task) - T021 through T032

# Each story is independently testable
# Different CLI handlers (handle_mark_complete vs handle_reopen_task)
# Different menu options
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 - Both P1)

1. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
2. Complete Phase 3: User Story 1 (Mark Complete)
3. Complete Phase 4: User Story 2 (Reopen Task)
4. **STOP and VALIDATE**: Test US1 and US2 independently
5. Deploy/demo basic completion management (mark complete + reopen)

### Incremental Delivery

1. Complete Foundational → Foundation ready
2. Add User Story 1 (Mark Complete) → Test independently → Deploy/Demo
3. Add User Story 2 (Reopen) → Test independently → **MVP DEMO** with P1 features!
4. Add User Story 3 (Error Handling) → Test independently → Deploy/Demo
5. Add Integration verification → Test with existing features → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Foundational together (Phase 2)
2. Once Foundational is done:
   - Developer A: User Story 1 (Mark Complete)
   - Developer B: User Story 2 (Reopen Task)
3. After US1/US2 complete:
   - Developer A: User Story 3 (Error Handling)
   - Developer B: Integration verification
4. Stories complete and integrate independently

---

## Task Count Summary

- **Phase 2 (Foundational)**: 8 tasks (T001-T008)
- **Phase 3 (US1 - Mark Complete, P1)**: 12 tasks (T009-T020)
- **Phase 4 (US2 - Reopen Task, P1)**: 12 tasks (T021-T032)
- **Phase 5 (US3 - Error Handling, P2)**: 10 tasks (T033-T042)
- **Phase 6 (Integration)**: 10 tasks (T043-T052)
- **Phase 7 (Polish)**: 17 tasks (T053-T069)

**Total Tasks**: 69 tasks

**Parallel Opportunities**: 2 foundational methods (same file), 2 user stories (different handlers), 10+ polish tasks (different scopes)

**MVP Scope**: Foundational + US1 + US2 = 8 + 12 + 12 = 32 tasks (46% of total)

---

## Notes

- [P] tasks = different files or safely parallelizable
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests not included per specification (not explicitly requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks extend existing TaskList from 001-add-task
- All tasks reuse existing validate_task_id() from 002-delete-task
- Idempotent operations: marking completed task again shows friendly message, not error
- Atomic updates: completed and updated_at always change together
- Focus on smallest viable changes per task
- Integration phase ensures compatibility with 003-update-task and 004-view-task
