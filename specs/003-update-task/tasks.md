---
description: "Task list for Update Task feature implementation"
---

# Tasks: Update Task Feature

**Input**: Design documents from `/specs/003-update-task/`
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

*No setup tasks needed - building on existing 001-add-task and 002-delete-task foundation*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T001 [P] Extend TaskService with update_task_title() method in src/services/task_service.py
- [X] T002 [P] Extend TaskService with update_task_description() method in src/services/task_service.py
- [X] T003 [P] Extend TaskService with update_task_status() method in src/services/task_service.py
- [X] T004 Create update_task_cli() function with ID prompt and validation in src/cli/task_cli.py
- [X] T005 Add "Update Task" menu option to main menu in src/cli/menu.py
- [X] T006 Wire update_task_cli() to menu selection in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Update Task Title (Priority: P1) 🎯 MVP

**Goal**: Users can modify task titles to correct typos, add clarification, or update task names

**Independent Test**: Add tasks, select "Update Task", enter task ID, choose to update title, enter new title, verify change appears in task list

### Implementation for User Story 1

- [X] T007 [US1] Implement task ID validation in update_task_cli() - numeric check, existence check in src/cli/task_cli.py
- [X] T008 [US1] Implement display current task values before update in update_task_cli() in src/cli/task_cli.py
- [X] T009 [US1] Implement field selection menu (title/description/status/multiple/cancel) in update_task_cli() in src/cli/task_cli.py
- [X] T010 [US1] Implement title update flow - show current title, prompt for new title in update_task_cli() in src/cli/task_cli.py
- [X] T011 [US1] Integrate validate_title() from utils.validators into title update flow in src/cli/task_cli.py
- [X] T012 [US1] Implement title update confirmation message in update_task_cli() in src/cli/task_cli.py
- [X] T013 [US1] Add empty task list check at start of update flow in update_task_cli() in src/cli/task_cli.py
- [X] T014 [US1] Add "cancel" keyword support at task ID prompt in update_task_cli() in src/cli/task_cli.py
- [X] T015 [US1] Add "cancel" keyword support at title input prompt in update_task_cli() in src/cli/task_cli.py
- [X] T016 [US1] Implement title length validation (max 200 chars) error handling in update_task_cli() in src/cli/task_cli.py
- [X] T017 [US1] Implement empty title validation error handling in update_task_cli() in src/cli/task_cli.py
- [X] T018 [US1] Implement whitespace trimming for updated titles in update_task_cli() in src/cli/task_cli.py

**Checkpoint**: At this point, User Story 1 (Update Title) should be fully functional and testable independently

---

## Phase 4: User Story 3 - Update Task Completion Status (Priority: P1)

**Goal**: Users can toggle task completion status to track progress

**Independent Test**: Create tasks, mark them complete, verify status changes, unmark them, verify the cycle works

**Note**: Prioritized as P1 alongside US1 per spec.md - essential for task management

### Implementation for User Story 3

- [X] T019 [US3] Implement status toggle option in field selection menu in update_task_cli() in src/cli/task_cli.py
- [X] T020 [US3] Implement status toggle flow - flip completed boolean in update_task_cli() in src/cli/task_cli.py
- [X] T021 [US3] Implement status-specific confirmation messages ("marked as complete" / "marked as incomplete") in update_task_cli() in src/cli/task_cli.py
- [X] T022 [US3] Display completion status visual indicator when showing current task values in update_task_cli() in src/cli/task_cli.py

**Checkpoint**: At this point, User Stories 1 AND 3 (Title + Status) should both work independently

---

## Phase 5: User Story 2 - Update Task Description (Priority: P2)

**Goal**: Users can modify task descriptions to add details or update context

**Independent Test**: Add tasks with descriptions, select "Update Task", choose to update description, enter new description, verify change

### Implementation for User Story 2

- [X] T023 [US2] Implement description update option in field selection menu in update_task_cli() in src/cli/task_cli.py
- [X] T024 [US2] Implement description update flow - show current description, prompt for new in update_task_cli() in src/cli/task_cli.py
- [X] T025 [US2] Integrate validate_description() from utils.validators into description update flow in src/cli/task_cli.py
- [X] T026 [US2] Implement empty description handling - set to None when user presses Enter in update_task_cli() in src/cli/task_cli.py
- [X] T027 [US2] Implement description length validation (max 1000 chars) error handling in update_task_cli() in src/cli/task_cli.py
- [X] T028 [US2] Add "cancel" keyword support at description input prompt in update_task_cli() in src/cli/task_cli.py
- [X] T029 [US2] Implement description update confirmation message in update_task_cli() in src/cli/task_cli.py

**Checkpoint**: At this point, all P1 and P2 user stories should be independently functional

---

## Phase 6: User Story 5 - Handle Update Errors Gracefully (Priority: P2)

**Goal**: Users receive clear guidance when encountering update errors and can recover without frustration

**Independent Test**: Enter invalid inputs (non-existent task ID, empty title, oversized text), verify error messages appear without data corruption

### Implementation for User Story 5

- [X] T030 [US5] Implement non-existent task ID error message with specific ID in update_task_cli() in src/cli/task_cli.py
- [X] T031 [US5] Implement non-numeric task ID error message and re-prompt in update_task_cli() in src/cli/task_cli.py
- [X] T032 [US5] Add task ID input with leading zeros handling (e.g., "007" → 7) in update_task_cli() in src/cli/task_cli.py
- [ ] T033 [US5] Enhance validation error messages to include constraints (max/min values) in update_task_cli() in src/cli/task_cli.py
- [ ] T034 [US5] Show current/original value when re-prompting after validation error in update_task_cli() in src/cli/task_cli.py
- [ ] T035 [US5] Ensure all error paths return to main menu without modifying task data in update_task_cli() in src/cli/task_cli.py

**Checkpoint**: Error handling complete - all error scenarios handled gracefully

---

## Phase 7: User Story 4 - Update Multiple Task Fields in One Operation (Priority: P3)

**Goal**: Users can update both title and description (or combinations) in a single operation for convenience

**Independent Test**: Select to update multiple fields, verify all changes apply simultaneously

### Implementation for User Story 4

- [ ] T036 [US4] Implement "Update Multiple Fields" option in field selection menu in update_task_cli() in src/cli/task_cli.py
- [ ] T037 [US4] Implement multi-field selection submenu (checkboxes or sequential prompts) in update_task_cli() in src/cli/task_cli.py
- [ ] T038 [US4] Collect all field updates before applying any changes (atomic update preparation) in update_task_cli() in src/cli/task_cli.py
- [ ] T039 [US4] Validate all fields before applying changes - cancel all updates on any validation error in update_task_cli() in src/cli/task_cli.py
- [ ] T040 [US4] Apply all validated changes atomically in update_task_cli() in src/cli/task_cli.py
- [ ] T041 [US4] Implement multi-field confirmation message listing modified fields in update_task_cli() in src/cli/task_cli.py
- [ ] T042 [US4] Handle partial field selection - update only selected fields, preserve others in update_task_cli() in src/cli/task_cli.py

**Checkpoint**: All user stories (P1, P2, P3) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T043 [P] Add docstrings to all new/modified functions in src/cli/task_cli.py
- [ ] T044 [P] Add type hints to update_task_cli() and helper functions in src/cli/task_cli.py
- [ ] T045 [P] Update README.md with Update Task feature documentation
- [ ] T046 [P] Add code comments for complex update logic (multi-field, validation) in src/cli/task_cli.py
- [ ] T047 Verify PEP 8 compliance with ruff for all modified files
- [ ] T048 Run manual testing per quickstart.md validation scenarios
- [ ] T049 Test special characters and unicode in updated titles/descriptions
- [ ] T050 Test edge cases from spec.md (empty list, duplicate titles, special chars, whitespace)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Skipped - building on existing foundation
- **Foundational (Phase 2)**: No dependencies - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 3 (Phase 4)**: Depends on Foundational (Phase 2) - Can run parallel to US1
- **User Story 2 (Phase 5)**: Depends on Foundational (Phase 2) - Can run parallel to US1/US3
- **User Story 5 (Phase 6)**: Depends on US1, US2, US3 (enhances error handling for all)
- **User Story 4 (Phase 7)**: Depends on US1, US2, US3 (combines all update types)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Update Title**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P1) - Toggle Status**: Can start after Foundational - No dependencies on other stories (parallel to US1)
- **User Story 2 (P2) - Update Description**: Can start after Foundational - No dependencies on other stories (parallel to US1/US3)
- **User Story 5 (P2) - Error Handling**: Needs US1, US2, US3 complete to add error handling to all flows
- **User Story 4 (P3) - Multi-Field Update**: Needs US1, US2, US3 complete to combine update operations

### Within Each User Story

- Foundational TaskService methods before CLI implementation
- Field selection menu before individual field flows
- Core implementation before error handling enhancements
- Validation integration before confirmation messages
- Story complete before moving to next priority

### Parallel Opportunities

- **Foundational Phase (Phase 2)**: T001, T002, T003 can run in parallel (different methods in same file - merge carefully)
- **User Stories Start**: After Phase 2 completes:
  - US1 (Phase 3), US3 (Phase 4), US2 (Phase 5) can all start in parallel if team capacity allows
  - All are independent and only depend on Foundational completion
- **Polish Phase (Phase 8)**: T043, T044, T045, T046 can run in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Launch foundational methods together (careful merge - same file):
Task T001: "Extend TaskService with update_task_title()"
Task T002: "Extend TaskService with update_task_description()"
Task T003: "Extend TaskService with update_task_status()"

# Review: These modify the same file - coordinate merging
```

## Parallel Example: User Stories (after Foundational complete)

```bash
# Launch user stories in parallel (different developers):
Developer A: Phase 3 (US1 - Update Title) - T007 through T018
Developer B: Phase 4 (US3 - Toggle Status) - T019 through T022
Developer C: Phase 5 (US2 - Update Description) - T023 through T029

# Each story is independently testable
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 3 Only - Both P1)

1. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
2. Complete Phase 3: User Story 1 (Update Title)
3. Complete Phase 4: User Story 3 (Toggle Status)
4. **STOP and VALIDATE**: Test US1 and US3 independently
5. Deploy/demo basic update functionality (title + status)

### Incremental Delivery

1. Complete Foundational → Foundation ready
2. Add User Story 1 (Title) → Test independently → Deploy/Demo
3. Add User Story 3 (Status) → Test independently → Deploy/Demo (MVP with P1 features!)
4. Add User Story 2 (Description) → Test independently → Deploy/Demo
5. Add User Story 5 (Error Handling) → Test independently → Deploy/Demo
6. Add User Story 4 (Multi-Field) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Foundational together (Phase 2)
2. Once Foundational is done:
   - Developer A: User Story 1 (Title)
   - Developer B: User Story 3 (Status)
   - Developer C: User Story 2 (Description)
3. After US1/US2/US3 complete:
   - Developer A: User Story 5 (Error Handling)
   - Developer B: User Story 4 (Multi-Field)
4. Stories complete and integrate independently

---

## Task Count Summary

- **Phase 2 (Foundational)**: 6 tasks (T001-T006)
- **Phase 3 (US1 - Update Title, P1)**: 12 tasks (T007-T018)
- **Phase 4 (US3 - Toggle Status, P1)**: 4 tasks (T019-T022)
- **Phase 5 (US2 - Update Description, P2)**: 7 tasks (T023-T029)
- **Phase 6 (US5 - Error Handling, P2)**: 6 tasks (T030-T035)
- **Phase 7 (US4 - Multi-Field, P3)**: 7 tasks (T036-T042)
- **Phase 8 (Polish)**: 8 tasks (T043-T050)

**Total Tasks**: 50 tasks

**Parallel Opportunities**: 3 foundational tasks (same file), 3 user stories (different sections), 4 polish tasks (different files)

**MVP Scope**: Foundational + US1 + US3 = 6 + 12 + 4 = 22 tasks (44% of total)

---

## Notes

- [P] tasks = different files or safely parallelizable
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests not included per specification (not explicitly requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks reuse existing validators from 001-add-task (validate_title, validate_description)
- All tasks extend existing TaskService and CLI structure from 001-add-task and 002-delete-task
- Focus on smallest viable changes per task
