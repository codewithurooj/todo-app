# Quick Start Guide: Add Task Feature

**Feature**: 001-add-task
**Date**: 2025-12-06
**Audience**: Developers

---

## Overview

This guide provides step-by-step instructions for setting up the development environment, running the application, executing tests, and contributing to the Add Task feature.

---

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.13 or higher
- **Git**: For version control
- **Terminal**: Bash, Zsh, or PowerShell

### Verify Python Installation

```bash
python --version
# Should output: Python 3.13.x or higher
```

If Python 3.13+ is not installed:
- **macOS/Linux**: Use `pyenv` or download from [python.org](https://www.python.org)
- **Windows**: Download installer from [python.org](https://www.python.org)

---

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Your prompt should now show `(venv)` prefix.

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -r requirements.txt
```

**Expected Output**:
```
Successfully installed pytest-8.x.x pytest-cov-5.x.x ruff-0.x.x black-24.x.x mypy-1.x.x
```

### 4. Verify Installation

```bash
# Check pytest
pytest --version

# Check ruff (linter)
ruff --version

# Check black (formatter)
black --version

# Check mypy (type checker)
mypy --version
```

---

## Project Structure

```
todo-app/
├── src/                    # Application source code
│   ├── models/            # Data models (Task entity)
│   ├── services/          # Business logic (TaskService)
│   ├── cli/               # CLI interface
│   └── utils/             # Utilities (validators)
├── tests/                 # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── contract/          # Contract tests
├── specs/                 # Feature specifications
│   └── 001-add-task/      # This feature
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── pyproject.toml         # Project configuration
```

---

## Running the Application

### Phase I: In-Memory Mode

**Note**: Phase I implementation uses in-memory storage. All data is lost when the application exits.

```bash
# Run the application
python main.py
```

**Expected Output**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Exit
Enter choice:
```

### Using Add Task Feature

1. Select option `1` (Add Task)
2. Enter task title when prompted
3. Optionally enter description (or press Enter to skip)
4. Task is created and confirmation displayed

**Example Session**:
```
Enter choice: 1

=== Add New Task ===
Enter task title: Buy groceries
Enter task description (optional):

✓ Task created successfully!
  ID: 1
  Title: Buy groceries
  Created: 2025-12-06T10:30:00
```

---

## Running Tests

### Run All Tests

```bash
# Run all tests with coverage
pytest --cov=src tests/

# Expected output shows all tests passing
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Contract tests only
pytest tests/contract/

# Specific test file
pytest tests/unit/test_task_model.py

# Specific test function
pytest tests/unit/test_task_model.py::test_create_task_with_title_only
```

### Run Tests with Verbose Output

```bash
# Show detailed output
pytest -v tests/

# Show print statements
pytest -s tests/

# Both verbose and print statements
pytest -vs tests/
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# Open coverage report (Linux/macOS)
open htmlcov/index.html

# Open coverage report (Windows)
start htmlcov/index.html
```

**Coverage Requirements**:
- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- **Critical Paths**: 100% coverage (validators, data models)

---

## Development Workflow

### TDD Cycle (Red-Green-Refactor)

1. **Red**: Write failing test
   ```bash
   # Create test file
   vim tests/unit/test_task_model.py

   # Run test (should fail)
   pytest tests/unit/test_task_model.py -v
   ```

2. **Green**: Write minimum code to pass
   ```bash
   # Implement feature
   vim src/models/task.py

   # Run test (should pass)
   pytest tests/unit/test_task_model.py -v
   ```

3. **Refactor**: Improve code quality
   ```bash
   # Run linter
   ruff check src/

   # Format code
   black src/

   # Type check
   mypy src/
   ```

### Code Quality Checks

```bash
# Lint code (check for errors)
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Format code
black src/ tests/

# Type check
mypy src/
```

### Pre-Commit Checklist

Before committing code:

```bash
# 1. Run all tests
pytest tests/

# 2. Check coverage
pytest --cov=src tests/

# 3. Lint code
ruff check src/ tests/

# 4. Format code
black src/ tests/

# 5. Type check
mypy src/
```

All checks must pass before committing.

---

## Common Tasks

### Add New Test

```bash
# Create test file
touch tests/unit/test_new_feature.py

# Write test
cat > tests/unit/test_new_feature.py << 'EOF'
import pytest

def test_example():
    assert True
EOF

# Run new test
pytest tests/unit/test_new_feature.py
```

### Debug Failing Test

```bash
# Run with debugger on failure
pytest --pdb tests/unit/test_task_model.py

# Run specific test with print output
pytest -vs tests/unit/test_task_model.py::test_specific_case
```

### Update Dependencies

```bash
# View outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pytest

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Ensure you're in project root
pwd  # Should show .../todo-app

# Verify PYTHONPATH (optional)
export PYTHONPATH=\${PYTHONPATH}:\$(pwd)
```

### Issue: Tests Not Found

**Problem**: `pytest` finds no tests

**Solution**:
```bash
# Verify test files start with test_
ls tests/unit/

# Run pytest with discovery
pytest --collect-only
```

### Issue: Import Errors in Tests

**Problem**: Cannot import from `src`

**Solution**:
```bash
# Install package in editable mode
pip install -e .
```

### Issue: Type Check Failures

**Problem**: `mypy` reports type errors

**Solution**:
```bash
# Check mypy configuration
cat pyproject.toml

# Run mypy with verbose output
mypy --show-error-codes src/
```

---

## Next Steps

After completing Add Task feature:

1. **Run Full Test Suite**: `pytest tests/ --cov=src`
2. **Review Code Coverage**: Ensure 90%+ coverage
3. **Manual Testing**: Test edge cases in console
4. **Documentation**: Update README.md if needed
5. **Git Workflow**:
   ```bash
   git add .
   git commit -m "feat: implement Add Task feature"
   git push origin 001-add-task
   ```

---

## Useful Commands Reference

```bash
# Development
python main.py                 # Run application
pytest tests/                  # Run all tests
pytest -v tests/               # Verbose test output
pytest --cov=src tests/        # With coverage

# Code Quality
ruff check src/                # Lint code
black src/                     # Format code
mypy src/                      # Type check

# Environment
source venv/bin/activate       # Activate venv (Linux/macOS)
venv\Scripts\activate         # Activate venv (Windows)
deactivate                     # Deactivate venv
pip list                       # List installed packages
pip freeze                     # Export dependencies

# Git
git status                     # Check status
git add .                      # Stage changes
git commit -m "message"        # Commit changes
git push origin <branch>       # Push to remote
```

---

## Additional Resources

- **Python Documentation**: https://docs.python.org/3.13/
- **pytest Documentation**: https://docs.pytest.org/
- **Type Hints (PEP 484)**: https://peps.python.org/pep-0484/
- **PEP 8 Style Guide**: https://peps.python.org/pep-0008/
- **Project Constitution**: `.specify/memory/constitution.md`
- **Feature Specification**: `specs/001-add-task/spec.md`
- **Data Model**: `specs/001-add-task/data-model.md`
- **Contracts**: `specs/001-add-task/contracts/`

---

**Status**: Development Guide Complete
**Last Updated**: 2025-12-06
