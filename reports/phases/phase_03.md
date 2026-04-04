# Phase 03 Report: Representation Extraction

Status: complete

What ran:
- `uv run python -m css.representations.extract_hidden --config configs/experiments/pilot.yaml --force`

Outputs:
- `cache/hidden/bert-base-uncased/*/hidden_cache.pkl`
- `cache/hidden/gpt2/*/hidden_cache.pkl`
- `cache/hidden/*/*/metadata.json`
- `results/manifests/extract_hidden_manifest.json`

Notes:
- Pilot extraction includes embedding + 12 layers.
- Cache metadata includes model/version/hash/seed/device.
