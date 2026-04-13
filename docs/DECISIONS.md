# Decisions Log

## 2026-04-24

### Decision: Adopt Astral-first developer stack

- **Chosen**: `uv` + `ruff` + `ty` as the default development backbone.
- **Reason**: unified workflow, high speed, active ecosystem, simplified toolchain.

### Decision: Pin project Python to 3.14

- **Chosen**: `.python-version = 3.14` (managed by uv).
- **Reason**: modern baseline and compatibility with latest language/tooling features.
- **Risk**: some ML packages can lag Python support; fallback path is to lower runtime version if required by package wheels.

### Decision: Frequent checkpoint commits + mandatory docs updates

- **Chosen**: small conventional commits after each logical chunk.
- **Reason**: safer iteration and easier rollback/review.

### Decision: Secret handling via `.env`

- **Chosen**: keep access tokens only in `.env` with gitignore protection.
- **Reason**: avoid accidental secret exposure in source control.

### Decision: Migrate role and negation to external psycholinguistic dataset

- **Chosen**: use `text-machine-lab/extending_psycholinguistic_dataset` as canonical source for role and negation.
- **Implementation**: `src/css/data/import_extending_psycholinguistic_dataset.py` converts source text files into `css_pair_v1` JSONL (`role_1500.jsonl`, `neg_1500.jsonl`), while attachment remains generated locally.
- **Reason**: align project data with requested upstream psycholinguistic resource and keep downstream CSS pipeline unchanged.
