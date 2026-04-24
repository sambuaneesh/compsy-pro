#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/text-machine-lab/extending_psycholinguistic_dataset"
TARGET_DIR="data/external/extending_psycholinguistic_dataset"

if [[ -d "${TARGET_DIR}/.git" ]]; then
  git -C "${TARGET_DIR}" pull --ff-only
  echo "Updated external dataset at ${TARGET_DIR}"
else
  mkdir -p "$(dirname "${TARGET_DIR}")"
  git clone "${REPO_URL}" "${TARGET_DIR}"
  echo "Cloned external dataset to ${TARGET_DIR}"
fi
