# Implementation Plan: Update Task Feature

**Branch**: `003-update-task` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-update-task/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the "Update Task" feature for Phase I of the Todo App Evolution project. This feature enables users to modify existing tasks by updating title, description, or completion status. The implementation builds on the existing foundation from Add Task (001) and Delete Task (002).

**Primary Requirement**: Console-based task modification with field selection, validation, error handling, and optional multi-field updates in a single operation.

**Technical Approach**: Extend existing TaskList service with update operations, reuse validation from Add Task, implement field selection UI in CLI, and preserve all unmodified attributes during updates.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only for Phase I)
**Storage**: In-memory (Python lists) - extends existing TaskList from 001-add-task
**Testing**: pytest with pytest-cov, capsys for CLI testing
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**:
- Task update: < 1 second response time
- Validation overhead: < 100ms per check
- Support 1000+ tasks without degradation

**Constraints**:
- Phase I: No persistence (in-memory only)
- Must preserve unmodified task attributes
- Build on existing Task and TaskList models from 001-add-task
- Reuse validators from 001-add-task where possible
- No external dependencies beyond testing tools

**Scale/Scope**:
- 5 core CRUD operations (add, delete, update, view, mark complete)
- Single-user application
- Extends existing in-memory task list

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: Complete specification exists at `specs/003-update-task/spec.md` with 5 user stories, 28 functional requirements, and 8 success criteria

✅ **Test-Driven Development**: Plan includes test-first approach with red-green-refactor cycle for all update operations

✅ **Evolutionary Architecture**: Phase I implementation builds on existing TaskList from 001-add-task, extends validation from 001, with clear evolution path

✅ **Clean Code & Python Standards**:
- Python 3.13+ with type hints
- PEP 8 compliance
- Docstrings for modules/classes/functions
- Extends existing clean code patterns from Add and Delete Task

✅ **Project Structure**: Follows established structure from 001-add-task with `src/`, `tests/`, `specs/` organization

✅ **Simplicity First (YAGNI)**:
- Extends existing TaskList with update methods
- Reuses validation from 001-add-task (title, description)
- No premature optimization
- Implements only specified features

✅ **Comprehensive Documentation**:
- Specification document complete
- Plan document (this file)
- Will include PHR, code comments, updated README

**Overall**: ✅ PASS - No constitution violations. Builds on existing foundation (001, 002).

## Project Structure

### Documentation (this feature)

```text
specs/003-update-task/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   ├── task_service.md  # Extended TaskService with update operations
│   └── update_cli.md    # Update CLI flow and field selection
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
│   └── task_service.py  # EXTENDED: Add update_task() methods
├── cli/
│   ├── __init__.py
│   ├── menu.py          # UPDATED: Add "Update Task" menu option
│   └── task_cli.py      # NEW: update_task_cli() function with field selection
└── utils/
    ├── __init__.py
    └── validators.py    # REUSED: validate_title(), validate_description() from 001

tests/
├── unit/
│   ├── test_task_model.py      # No changes (from 001-add-task)
│   ├── test_task_service.py    # EXTENDED: Add update tests
│   └── test_validators.py      # Reuse existing validators
├── integration/
│   └── test_update_task_flow.py # NEW: End-to-end update flow tests
└── contract/
    └── test_update_contract.py   # NEW: Update operation contract tests

# Root level files
main.py                  # UPDATED: Wire update CLI to menu
README.md                # UPDATED: Document update feature
requirements.txt         # No changes
pyproject.toml          # No changes
```

**Structure Decision**: Extends existing single project structure from 001-add-task and 002-delete-task. Update functionality integrates into existing TaskService and CLI layers. Minimal new code - primarily extends existing components and reuses validators.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All complexity justified by update feature requirements.*

---

## Phase 0: Research & Technical Decisions

### Research Tasks

Based on Technical Context and feature requirements, research needed:

1. **Update Operation Design**
   - **Question**: Best approach for updating task fields in-memory?
   - **Options**: Direct attribute modification, create new task, copy-and-modify
   - **Research**: Python object mutation patterns

2. **Field Selection UI**
   - **Question**: How to let users choose which fields to update?
   - **Options**: Menu-based selection, update all fields, individual prompts
   - **Research**: CLI interaction patterns for selective updates

3. **Validation Reuse Strategy**
   - **Question**: Can we reuse validators from Add Task?
   - **Options**: Reuse directly, extend validators, create new validators
   - **Research**: Validator composition patterns

4. **Partial Update Handling**
   - **Question**: How to handle updating only some fields?
   - **Options**: Pass None for unchanged, use separate flags, optional parameters
   - **Research**: Partial update patterns in Python

5. **Status Toggle Logic**
   - **Question**: Separate operation or part of general update?
   - **Options**: Dedicated toggle method, general update with boolean flip, user choice
   - **Research**: Task completion status management patterns

### Research Deliverable

See `research.md` for detailed findings and decisions.

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for complete entity definitions.

**Summary**:
- **Task Entity**: No changes (defined in 001-add-task)
- **TaskList**: Extended with `update_task()` methods (title, description, status)
- **Validation Rules**: Reuse from 001-add-task (title 1-200 chars, description 0-1000 chars)
- **Update Semantics**: Direct attribute modification, preserve unmodified fields

### API Contracts

See `contracts/` directory for detailed contracts.

**Summary**:
- Extended TaskService interface with update operations
- Field selection and partial update contracts
- CLI flow for field selection and confirmation

### Implementation Quickstart

See `quickstart.md` for:
- Testing update functionality
- Running update-specific tests
- Debugging update flow

---

## Next Steps

1. ✅ **Complete Phase 0**: Generate `research.md` with technical decisions
2. ✅ **Complete Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
3. **Phase 2** (separate command): Run `/sp.tasks` to generate testable task breakdown
4. **Phase 3** (separate command): Run `/sp.implement` for TDD implementation

---

**Status**: Phase 0 and Phase 1 in progress
**Last Updated**: 2025-12-06
