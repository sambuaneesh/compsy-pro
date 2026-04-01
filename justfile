set shell := ["bash", "-lc"]

sync:
    uv sync --all-groups

check:
    uv run ruff check .
    uv run ruff format --check .
    uv run ty check
    uv run pytest

fmt:
    uv run ruff format .
    uv run ruff check --fix .

test:
    uv run pytest

lock:
    uv lock
