.PHONY: help test test-all test-cov test-e2e install run clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install all dependencies (Python + Node)"
	@echo "  make run        - Run development server"
	@echo "  make test       - Run backend tests (pytest)"
	@echo "  make test-all   - Run ALL tests (backend + E2E)"
	@echo "  make test-cov   - Run backend tests with coverage"
	@echo "  make test-e2e   - Run frontend E2E tests (Playwright)"
	@echo "  make clean      - Clean build artifacts"

install:
	uv sync
	npm install

run:
	uv run uvicorn main:app --reload

test:
	uv run pytest -v

test-all:
	@echo "Running backend tests..."
	uv run pytest -v
	@echo "\nRunning E2E tests..."
	npm test

test-cov:
	uv run pytest --cov=. --cov-report=term-missing --cov-report=html

test-e2e:
	npm test

test-e2e-ui:
	npm run test:ui

clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf __pycache__
	rm -rf node_modules
	rm -rf test-results
	rm -rf playwright-report
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
