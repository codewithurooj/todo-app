# Implementation Plan: Delete Task Feature

**Branch**: `002-delete-task` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-delete-task/spec.md`

## Summary

Implement the "Delete Task" feature for Phase I of the Todo App Evolution project. This feature enables users to remove tasks from their list by ID, with validation, error handling, and optional confirmation. The implementation builds on the existing Add Task foundation and follows TDD principles.

**Primary Requirement**: Console-based task deletion with ID validation, confirmation prompts, clear error messages, and proper handling of edge cases (empty list, non-existent IDs).

**Technical Approach**: Extend existing TaskList service with delete operation, add validation for task existence, implement confirmation flow in CLI, and ensure ID preservation for remaining tasks.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only for Phase I)
**Storage**: In-memory (Python lists) - extends existing TaskList from 001-add-task
**Testing**: pytest with pytest-cov, capsys for CLI testing
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**:
- Task deletion: < 1 second response time
- Validation overhead: < 100ms per check
- Support 1000+ tasks without degradation

**Constraints**:
- Phase I: No persistence (in-memory only)
- Must preserve IDs of remaining tasks (no renumbering)
- Build on existing Task and TaskList models from 001-add-task
- No external dependencies beyond testing tools

**Scale/Scope**:
- 5 core CRUD operations (add, delete, update, view, mark complete)
- Single-user application
- Extends existing in-memory task list

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: Complete specification exists at `specs/002-delete-task/spec.md` with 3 user stories, 15 functional requirements, and 8 success criteria

✅ **Test-Driven Development**: Plan includes test-first approach with red-green-refactor cycle for all delete operations

✅ **Evolutionary Architecture**: Phase I implementation builds on existing TaskList from 001-add-task, with clear evolution path

✅ **Clean Code & Python Standards**:
- Python 3.13+ with type hints
- PEP 8 compliance
- Docstrings for modules/classes/functions
- Extends existing clean code patterns from Add Task

✅ **Project Structure**: Follows established structure from 001-add-task with `src/`, `tests/`, `specs/` organization

✅ **Simplicity First (YAGNI)**:
- Extends existing TaskList.delete_task() method
- No premature optimization
- Implements only specified features (delete by ID, validation, confirmation)

✅ **Comprehensive Documentation**:
- Specification document complete
- Plan document (this file)
- Will include PHR, code comments, updated README

**Overall**: ✅ PASS - No constitution violations. Builds on existing foundation.

## Project Structure

### Documentation (this feature)

```text
specs/002-delete-task/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   ├── task_service.md  # Extended TaskService with delete operation
│   └── validation.md    # Delete-specific validation contracts
└── tasks.md             # Phase 2 output (via /sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Task entity (from 001-add-task, no changes)
├── services/
│   ├── __init__.py
│   └── task_service.py  # EXTENDED: Add delete_task() method
├── cli/
│   ├── __init__.py
│   ├── menu.py          # UPDATED: Add "Delete Task" menu option
│   └── task_cli.py      # NEW: delete_task_cli() function
└── utils/
    ├── __init__.py
    └── validators.py    # EXTENDED: Add validate_task_id() function

tests/
├── unit/
│   ├── test_task_model.py      # No changes (from 001-add-task)
│   ├── test_task_service.py    # EXTENDED: Add delete tests
│   └── test_validators.py      # EXTENDED: Add ID validation tests
├── integration/
│   └── test_delete_task_flow.py # NEW: End-to-end delete flow tests
└── contract/
    └── test_delete_contract.py   # NEW: Delete operation contract tests

# Root level files
main.py                  # UPDATED: Wire delete CLI to menu
README.md                # UPDATED: Document delete feature
requirements.txt         # No changes
pyproject.toml          # No changes
```

**Structure Decision**: Extends existing single project structure from 001-add-task. Delete functionality integrates into existing TaskService and CLI layers. Minimal new files needed - primarily extending existing components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All complexity justified by delete feature requirements.*

---

## Phase 0: Research & Technical Decisions

### Research Tasks

Based on Technical Context and feature requirements, the following research is needed:

1. **Delete Operation Design**
   - **Question**: Best approach for deleting tasks from in-memory list?
   - **Options**: Remove by index, remove by ID search, filter out deleted
   - **Research**: Python list mutation best practices

2. **ID Preservation Strategy**
   - **Question**: How to ensure IDs are never reused after deletion?
   - **Options**: Track deleted IDs, never decrement counter, validation check
   - **Research**: ID management patterns in CRUD operations

3. **Confirmation Flow Design**
   - **Question**: Where to implement confirmation in the flow?
   - **Options**: Service layer, CLI layer, separate confirmation utility
   - **Research**: CLI user interaction patterns for destructive operations

4. **Error Handling Patterns**
   - **Question**: How to handle non-existent task ID gracefully?
   - **Options**: Return None, raise exception, return error tuple
   - **Research**: Python error handling best practices for user-facing apps

5. **Validation Integration**
   - **Question**: Reuse existing validators or create delete-specific ones?
   - **Options**: Extend validators.py, inline validation, service-level validation
   - **Research**: Validation layer architecture patterns

### Research Deliverable

See `research.md` for detailed findings and decisions.

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for complete entity definitions.

**Summary**:
- **Task Entity**: No changes (defined in 001-add-task)
- **TaskList**: Extended with `delete_task(task_id: int)` method
- **Validation Rules**: New rule for task ID existence validation
- **State Management**: Track that deleted IDs are never reused

### API Contracts

See `contracts/` directory for detailed contracts.

**Summary**:
- Extended TaskService interface with delete operation
- Delete-specific validation contracts
- Error handling contracts for delete failures

### Implementation Quickstart

See `quickstart.md` for:
- Testing delete functionality
- Running delete-specific tests
- Debugging delete flow

---

## Next Steps

1. ✅ **Complete Phase 0**: Generate `research.md` with technical decisions
2. ✅ **Complete Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
3. **Phase 2** (separate command): Run `/sp.tasks` to generate testable task breakdown
4. **Phase 3** (separate command): Run `/sp.implement` for TDD implementation

---

**Status**: Phase 0 and Phase 1 in progress
**Last Updated**: 2025-12-06
