SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.13
PROJECT = mcp_server_metabase


.PHONY: all
all: test

.PHONY: install
install: sync

sync:
	uv sync --extra test

.PHONY: test
test: clean install lint
	uv run pytest

.PHONY: format
format:
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: lint
lint:
	uv run ruff check .
	uv run ruff format --check .
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
	fastmcp dev mcp_server_metabase/app.py
