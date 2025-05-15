SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.13
PROJECT = mcp_server_metabase


.PHONY: all
all: test

.PHONY: venv
venv:
	uv venv

.PHONY: install
install:
	uv pip install

.PHONY: install-test
install-test:
	uv pip install -e ".[test]"

.PHONY: test
test: clean install-test lint
	pytest

.PHONY: format
format:
	uv run isort $(PROJECT) tests
	uv run ruff format $(PROJECT) tests
	uv run ruff check --fix $(PROJECT) tests

.PHONY: lint
lint:
	uv run ruff format --check $(PROJECT) tests
	uv run ruff check $(PROJECT) tests
	uv run mypy $(PROJECT) tests

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name '*.py[co]' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	find . -type f -name '.*~' -exec rm -f {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .cache .pytest_cache .ruff_cache htmlcov
	rm -rf build dist site coverage.xml
	rm -rf .mypy_cache

.PHONY: dev
dev:
	mcp dev mcp_server_metabase/app.py
