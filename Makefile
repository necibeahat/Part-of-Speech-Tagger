# Makefile for NLP POS Tagging Project

.PHONY: help install test lint format clean docs docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run all tests"
	@echo "  test-unit   - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black and isort"
	@echo "  format-check - Check code formatting without making changes"
	@echo "  clean       - Clean up temporary files"
	@echo "  docs        - Build documentation"
	@echo "  notebook    - Start Jupyter notebook server"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  security    - Run security checks"
	@echo "  all         - Run format, lint, and test"

# Installation
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('brown'); nltk.download('universal_tagset')"

# Testing
test:
	pytest test_helpers.py test_integration.py -v

test-unit:
	pytest test_helpers.py -v

test-integration:
	pytest test_integration.py -v

test-coverage:
	pytest test_helpers.py test_integration.py -v --cov=helpers --cov-report=html --cov-report=term-missing

test-slow:
	pytest test_integration.py -v -m slow

# Code quality
lint:
	flake8 .
	@echo "✓ Linting passed"

format:
	black .
	isort .
	@echo "✓ Code formatted"

format-check:
	black --check --diff .
	isort --check-only --diff .
	@echo "✓ Code formatting is correct"

# Security
security:
	safety check
	bandit -r . -ll
	@echo "✓ Security checks completed"

# Documentation
docs:
	@echo "Building documentation..."
	mkdir -p docs/source
	sphinx-apidoc -o docs/source . --separate --force
	cd docs && sphinx-build -b html source build/html
	@echo "✓ Documentation built in docs/build/html/"

# Jupyter
notebook:
	jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# Docker
docker-build:
	docker build -t nlp-pos-tagging .

docker-run:
	docker run -p 8888:8888 -v $(PWD):/app nlp-pos-tagging

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf docs/build/
	@echo "✓ Cleaned up temporary files"

# Comprehensive check
all: format lint test
	@echo "✓ All checks passed!"

# Development setup
dev-setup: install
	pip install pre-commit
	pre-commit install
	@echo "✓ Development environment set up"

# Release preparation
release-check: format-check lint test-coverage security
	@echo "✓ Release checks passed!"

# Validate notebooks
validate-notebooks:
	jupyter nbconvert --to notebook --execute --inplace HiddenMarkovModelforPOS.ipynb --ExecutePreprocessor.timeout=600
	jupyter nbconvert --to notebook --execute --inplace DownloadDataset.ipynb --ExecutePreprocessor.timeout=300
	@echo "✓ Notebooks validated"

# Convert notebooks to HTML
notebooks-html:
	jupyter nbconvert --to html HiddenMarkovModelforPOS.ipynb
	jupyter nbconvert --to html DownloadDataset.ipynb
	@echo "✓ Notebooks converted to HTML"