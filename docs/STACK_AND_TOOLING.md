# Stack And Tooling

Last updated: `2026-04-24`

## Goals

- Stay on a modern, high-performance Python stack.
- Prefer tools with active development and strong ecosystem integration.
- Keep one consistent workflow across local dev, experiments, and CI.

## Selected Stack (By Use Case)

| Use case | Tool | Why this choice |
| --- | --- | --- |
| Python/version/env/deps | `uv` | Single fast tool for Python install, envs, lockfile, dependency management, script execution |
| Lint + format | `ruff` | High-performance linter/formatter in one tool |
| Type checking + language services | `ty` | Latest Astral type checker + language server, fast incremental checks |
| Testing | `pytest` | Standard, composable, mature testing framework |
| Local quality gates | `pre-commit` | Enforces consistent checks before commits |
| Experiment libs | `torch`, `transformers`, `datasets`, `evaluate`, `accelerate` | Core modern LLM experimentation stack |
| Data science stack | `numpy`, `pandas`, `scipy`, `scikit-learn`, `statsmodels` | Numeric, statistical, probing/evaluation workflows |
| Visualization | `matplotlib`, `seaborn` | Layer-wise and correlation visualization |
| Secret management | `.env` + `python-dotenv` | Simple, standard local secret loading |

## Current Project Policy

- Prefer Astral toolchain first (`uv`, `ruff`, `ty`).
- Run everything via `uv run` / `uvx`.
- Keep dependencies in `pyproject.toml` + `uv.lock`.
- Keep secrets outside Git (`.env`).
- Keep external role/negation source under `data/external/extending_psycholinguistic_dataset` and import into canonical JSONL.

## Recommended Next Adoptions (After Baseline Pipeline)

| Use case | Candidate tool | Notes |
| --- | --- | --- |
| Data/model versioning | `dvc` | Track large datasets and artifacts outside Git while versioning metadata in repo |
| Experiment tracking | `mlflow` or `wandb` | Record parameters, metrics, artifacts, and run lineage |
| Documentation site | `mkdocs-material` | Publish project docs with searchable navigation |
| CI matrix | GitHub Actions + `uv` | Reproducible lint/type/test jobs across Python versions |
| Notebook replacement | `marimo` | Reproducible notebook workflows with dependency-aware execution |

## Primary References

- uv docs: https://docs.astral.sh/uv/
- uv features: https://docs.astral.sh/uv/getting-started/features/
- uv workspaces: https://docs.astral.sh/uv/concepts/projects/workspaces/
- ruff docs: https://docs.astral.sh/ruff/
- ty docs: https://docs.astral.sh/ty/
- ty configuration: https://docs.astral.sh/ty/reference/configuration/
- Python 3.14 release: https://www.python.org/downloads/release/python-3140/
