# Makefile for Part-of-Speech Tagger project

.PHONY: help install install-dev test lint format check clean setup-dev run-notebook

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  setup-dev    - Set up development environment"
	@echo "  test         - Run tests"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black and isort"
	@echo "  check        - Run all checks (lint, format, test)"
	@echo "  clean        - Clean up temporary files"
	@echo "  run-notebook - Start Jupyter notebook server"
	@echo "  docs-check   - Check documentation"

# Installation targets
install:
	pip install -r requirements.txt

install-dev: install
	pip install pytest pytest-cov flake8 black isort jupyter notebook

setup-dev: install-dev
	@echo "Development environment setup complete!"
	@echo "You can now run 'make check' to verify everything works."

# Testing
test:
	python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

test-quick:
	python -m pytest tests/ -v

# Code quality
lint:
	flake8 . --count --statistics
	@echo "Linting complete!"

format:
	black .
	isort .
	@echo "Code formatting complete!"

format-check:
	black --check --diff .
	isort --check-only --diff .

# Combined checks
check: format-check lint test
	@echo "All checks passed!"

# Documentation checks
docs-check:
	@echo "Checking documentation..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint README.md --config .markdownlint.json; \
	else \
		echo "markdownlint not installed. Run: npm install -g markdownlint-cli"; \
	fi
	@if command -v markdown-link-check >/dev/null 2>&1; then \
		markdown-link-check README.md --config .markdown-link-check.json; \
	else \
		echo "markdown-link-check not installed. Run: npm install -g markdown-link-check"; \
	fi

# Jupyter notebook
run-notebook:
	jupyter notebook

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	@echo "Cleanup complete!"

# Data download (if needed)
download-data:
	python -c "import nltk; nltk.download('brown'); nltk.download('universal_tagset')"

# Run the main analysis
run-analysis:
	jupyter nbconvert --to notebook --execute HiddenMarkovModelforPOS.ipynb --output HiddenMarkovModelforPOS_executed.ipynb

# GitHub Actions simulation
simulate-ci: format-check lint test docs-check
	@echo "Simulating GitHub Actions CI pipeline..."
	@echo "All CI checks completed successfully!"