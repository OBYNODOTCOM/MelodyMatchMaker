.PHONY: help install install-dev test test-cov lint format type-check security pre-commit clean docs

help:
	@echo "MelodyMatchMaker Development Tasks"
	@echo "===================================="
	@echo ""
	@echo "Install and Setup:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo "  make pre-commit-setup - Set up pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run tests"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make test-watch       - Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run all linters (flake8, pylint, mypy)"
	@echo "  make format           - Auto-format code with Black and isort"
	@echo "  make format-check     - Check formatting without changes"
	@echo "  make type-check       - Run type checking with mypy"
	@echo "  make security         - Run security checks (bandit)"
	@echo "  make quality-all      - Run all quality checks"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            - Remove build artifacts and cache"
	@echo "  make docs             - Build documentation"
	@echo ""

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

pre-commit-setup:
	pre-commit install
	@echo "Pre-commit hooks installed successfully"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

test-watch:
	pytest-watch tests/ -v

lint:
	@echo "Running flake8..."
	flake8 . --max-line-length=100 --extend-ignore=E203,W503 || true
	@echo ""
	@echo "Running pylint..."
	pylint **/*.py --disable=all --enable=E,F,W || true
	@echo ""
	@echo "Running mypy..."
	mypy . --ignore-missing-imports || true

format:
	@echo "Formatting with Black..."
	black .
	@echo ""
	@echo "Sorting imports with isort..."
	isort . --profile=black
	@echo "Code formatted successfully"

format-check:
	@echo "Checking Black formatting..."
	black --check --diff . || true
	@echo ""
	@echo "Checking isort import sorting..."
	isort --check-only --diff . || true

type-check:
	mypy . --ignore-missing-imports --warn-redundant-casts --warn-unused-ignores

security:
	@echo "Running Bandit security check..."
	bandit -r . -f csv -o bandit-report.csv || true
	@echo "Security report: bandit-report.csv"

quality-all: format lint type-check security
	@echo ""
	@echo "All quality checks completed!"

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info
	@echo "Cleaned up build artifacts and cache files"
