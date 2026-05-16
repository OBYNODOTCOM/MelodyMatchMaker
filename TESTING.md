# Testing & Quality Assurance Guide

This guide explains how to run tests, perform static analysis, and maintain code quality in the MelodyMatchMaker project.

## Quick Start

### Install Development Dependencies
```bash
make install-dev
# or manually:
pip install -r requirements-dev.txt
```

### Run All Tests
```bash
make test
```

### Run Tests with Coverage
```bash
make test-cov
```

### Format Code
```bash
make format
```

### Run All Quality Checks
```bash
make quality-all
```

---

## Testing Framework

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run specific test class
pytest tests/test_core.py::TestUtilityFunctions

# Run specific test function
pytest tests/test_core.py::TestUtilityFunctions::test_format_duration_valid

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests matching a pattern
pytest -k "test_format"

# Run with markers
pytest -m "not slow"
```

### Test Coverage

Coverage reports are generated in the `htmlcov/` directory. Open `htmlcov/index.html` in a browser to view detailed coverage.

```bash
make test-cov
# View report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```

**Coverage Goals:**
- Minimum 70% overall coverage
- Aim for 85%+ on critical paths (recommendation engine, auth)
- 100% on utility functions

---

## Code Quality Tools

### 1. **Black** - Code Formatting

Enforces consistent code style.

```bash
# Format all Python files
black .

# Check formatting without changes
black --check --diff .

# Format specific file
black melody_core.py
```

**Configuration:** `pyproject.toml` under `[tool.black]`

### 2. **isort** - Import Sorting

Automatically organizes imports.

```bash
# Sort all imports
isort .

# Check without changes
isort --check-only --diff .
```

**Configuration:** `pyproject.toml` under `[tool.isort]`

### 3. **Flake8** - Style Guide Enforcement

Checks PEP 8 compliance and common errors.

```bash
# Lint all files
flake8 .

# Lint with specific configuration
flake8 . --max-line-length=100

# Show statistics
flake8 . --statistics
```

**Configuration:** `pyproject.toml` under `[tool.pylint]`

### 4. **Pylint** - Code Analysis

Performs detailed code quality analysis.

```bash
# Run pylint
pylint **/*.py

# Run with specific options
pylint --disable=all --enable=E,F,W .

# Generate report
pylint --output-format=json . > pylint-report.json
```

**Configuration:** `pyproject.toml` under `[tool.pylint]`

### 5. **mypy** - Type Checking

Static type checking for Python.

```bash
# Type check all files
mypy .

# Check specific file
mypy melody_core.py

# Ignore missing imports
mypy . --ignore-missing-imports
```

**Configuration:** `pyproject.toml` under `[tool.mypy]`

### 6. **Bandit** - Security Analysis

Scans for common security issues.

```bash
# Run security check
bandit -r .

# Generate report
bandit -r . -f json -o security-report.json

# Exclude test files
bandit -r . --exclude tests/
```

**Configuration:** `.bandit` file

---

## Pre-commit Hooks

Automatically run quality checks before each commit.

### Setup

```bash
make pre-commit-setup
# or manually:
pre-commit install
```

### Run Manually

```bash
# Run on staged files
pre-commit run

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

### Bypass Hooks (when necessary)

```bash
git commit --no-verify
```

### Update Hooks

```bash
pre-commit autoupdate
```

---

## Continuous Integration

GitHub Actions automatically runs tests and quality checks on:
- Every push to `main` or `develop` branches
- Every pull request to `main` or `develop`

### Workflows

1. **tests.yml** - Unit tests across Python 3.9, 3.10, 3.11 on Ubuntu, Windows, macOS
2. **lint.yml** - Code quality and formatting checks
3. **security.yml** - Security analysis with Bandit

View results in the Actions tab on GitHub.

---

## Development Workflow

### Recommended Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make changes and write tests:
   ```bash
   # Your code changes
   ```

3. Run local tests:
   ```bash
   make test-cov
   ```

4. Format and lint:
   ```bash
   make format
   make lint
   ```

5. Run security check:
   ```bash
   make security
   ```

6. Commit changes:
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```
   Pre-commit hooks will run automatically.

7. Push and create PR:
   ```bash
   git push origin feature/my-feature
   ```

---

## Writing Tests

### Test Structure

```python
import pytest

class TestMyFeature:
    """Test my feature."""
    
    def test_something_works(self):
        """Test that something works as expected."""
        result = my_function(input_value)
        assert result == expected_value
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for tests."""
        return {"key": "value"}
    
    def test_with_fixture(self, sample_data):
        """Test using a fixture."""
        result = my_function(sample_data)
        assert result is not None
```

### Testing Best Practices

- **Test naming:** Use descriptive names like `test_feature_does_something_when_condition`
- **Arrange-Act-Assert:** Organize tests into setup, action, assertion
- **One assertion per test:** Focus on one behavior per test
- **Use fixtures:** Share setup code between tests
- **Mock external dependencies:** Use `pytest-mock` for external calls
- **Test edge cases:** Empty inputs, None values, boundary conditions
- **Document why:** Use docstrings to explain non-obvious tests

### Coverage Requirements

Maintain coverage above minimum thresholds:

```bash
pytest --cov=. --cov-fail-under=70
```

---

## Troubleshooting

### Import Errors in Tests

```bash
# Ensure working directory is project root
cd /path/to/MelodyMatchMaker

# Check Python path
python -c "import sys; print(sys.path)"

# Run pytest from project root
pytest tests/
```

### Dependency Issues

```bash
# Reinstall all dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Clear cache
make clean
pip cache purge

# Reinstall
pip install -r requirements.txt -r requirements-dev.txt
```

### Pre-commit Hook Issues

```bash
# Reinstall hooks
pre-commit install -f

# Clear cache
pre-commit clean

# Run on all files to ensure they pass
pre-commit run --all-files
```

### Type Checking Issues

If mypy reports errors but tests pass:

```bash
# Check mypy configuration
mypy --config-file=pyproject.toml .

# Ignore specific imports
mypy . --ignore-missing-imports
```

---

## Useful Commands Summary

| Command | Purpose |
|---------|---------|
| `make test` | Run all tests |
| `make test-cov` | Run tests with coverage report |
| `make format` | Auto-format code |
| `make lint` | Run all linters |
| `make type-check` | Type checking |
| `make security` | Security analysis |
| `make quality-all` | Run all quality checks |
| `make clean` | Clean build artifacts |
| `make help` | Show all available commands |

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://github.com/psf/black)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Bandit Security](https://bandit.readthedocs.io/)
- [GitHub Actions](https://github.com/features/actions)
