# Implementation Plan: Add Task Feature

**Branch**: `001-add-task` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-add-task/spec.md`

## Summary

Implement the core "Add Task" feature for Phase I of the Todo App Evolution project. This feature enables users to create new tasks via a console interface, with title (required) and description (optional), stored in-memory using Python data structures. The implementation follows TDD principles and serves as the foundation for all other CRUD operations.

**Primary Requirement**: Console-based task creation with input validation, unique ID assignment, timestamp tracking, and in-memory storage.

**Technical Approach**: Python 3.13+ console application using native data structures (lists/dicts), pytest for testing, following clean code principles with type hints and comprehensive error handling.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Phase I: stdlib only)
**Storage**: In-memory Python data structures (lists, dictionaries) - No persistence
**Testing**: pytest (unit, integration), pytest-cov for coverage
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**:
- Task creation: < 1 second response time
- Support 1000+ tasks in memory without degradation
- Memory footprint: < 100MB for 1000 tasks

**Constraints**:
- Phase I: No file I/O or database (in-memory only)
- No external dependencies beyond testing tools
- Console interface only (no GUI)
- Data lost on application exit (expected behavior)

**Scale/Scope**:
- 5 core CRUD operations (add, view, update, delete, mark complete)
- Single-user application
- ~500-1000 tasks typical use case

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: Complete specification exists at `specs/001-add-task/spec.md` with user scenarios, functional requirements, and success criteria

✅ **Test-Driven Development**: Plan includes test-first approach with red-green-refactor cycle

✅ **Evolutionary Architecture**: Phase I implementation (simplest: in-memory) with clear path to Phase II (file persistence)

✅ **Clean Code & Python Standards**:
- Python 3.13+ with type hints
- PEP 8 compliance
- Docstrings for modules/classes/functions
- Max 20 lines per function

✅ **Project Structure**: Follows constitution-defined structure with `src/`, `tests/`, `specs/` organization

✅ **Simplicity First (YAGNI)**:
- No premature optimization
- In-memory storage (simplest solution)
- No unnecessary abstractions
- Implements only specified features

✅ **Comprehensive Documentation**:
- Specification document complete
- Plan document (this file)
- Will include PHR, code comments, README updates

**Overall**: ✅ PASS - No constitution violations. All gates satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-add-task/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── task_model.py    # Task data model contract
└── tasks.md             # Phase 2 output (via /sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Task entity model with validation
├── services/
│   ├── __init__.py
│   └── task_service.py  # Task business logic (add, validate)
├── cli/
│   ├── __init__.py
│   ├── menu.py          # Main menu and navigation
│   └── task_cli.py      # Add task CLI interface
└── utils/
    ├── __init__.py
    └── validators.py    # Input validation utilities

tests/
├── unit/
│   ├── test_task_model.py      # Task entity tests
│   ├── test_task_service.py    # Service layer tests
│   └── test_validators.py      # Validation logic tests
├── integration/
│   └── test_add_task_flow.py   # End-to-end add task tests
└── contract/
    └── test_task_contract.py   # Task model contract tests

# Root level files
main.py                  # Application entry point
README.md                # Project documentation
requirements.txt         # Python dependencies (pytest, ruff, black, mypy)
pyproject.toml          # Python project configuration
```

**Structure Decision**: Selected single project structure as this is a Phase I console application. The structure separates concerns (models, services, CLI) to facilitate future evolution to web/API layers in later phases. The `src/` directory contains application code, `tests/` mirrors the `src/` structure, following pytest conventions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All complexity is justified by Phase I requirements.*

---

## Phase 0: Research & Technical Decisions

### Research Tasks

Based on Technical Context, the following research is needed:

1. **Task ID Generation Strategy**
   - **Question**: Best approach for unique ID generation in Python?
   - **Options**: Sequential integers, UUID, timestamp-based
   - **Research**: Evaluate trade-offs for in-memory console app

2. **Timestamp Format & Timezone Handling**
   - **Question**: How to handle timestamps in console app?
   - **Options**: UTC only, local time, timezone-aware
   - **Research**: Python datetime best practices

3. **Input Validation Patterns**
   - **Question**: Best practice for console input validation in Python?
   - **Options**: Inline validation, validator classes, decorators
   - **Research**: Clean, testable validation patterns

4. **Data Structure Choice**
   - **Question**: Best in-memory structure for task storage?
   - **Options**: List of dicts, List of Task objects, Dict with ID keys
   - **Research**: Performance and maintainability trade-offs

5. **Testing Strategy**
   - **Question**: How to test console I/O effectively?
   - **Options**: Mock stdin/stdout, pytest fixtures, capsys
   - **Research**: pytest patterns for CLI testing

### Research Deliverable

See `research.md` for detailed findings and decisions.

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for complete entity definitions.

**Summary**:
- **Task Entity**: id (int), title (str), description (str|None), completed (bool), created_at (datetime)
- **TaskList**: In-memory collection with ID counter
- **Validation Rules**: Title 1-200 chars, Description 0-1000 chars, no empty titles

### API Contracts

See `contracts/` directory for detailed contracts.

**Summary**:
- Task model schema (type hints and validation rules)
- Input validation contracts
- Service layer interfaces

### Implementation Quickstart

See `quickstart.md` for:
- Environment setup steps
- Running the application
- Running tests
- Development workflow

---

## Next Steps

1. ✅ **Complete Phase 0**: Generate `research.md` with technical decisions
2. ✅ **Complete Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
3. **Phase 2** (separate command): Run `/sp.tasks` to generate testable task breakdown
4. **Phase 3** (separate command): Run `/sp.implement` for TDD implementation

---

**Status**: Phase 0 and Phase 1 in progress
**Last Updated**: 2025-12-06
