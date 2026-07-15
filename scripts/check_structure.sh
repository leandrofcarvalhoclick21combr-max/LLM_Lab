#!/bin/bash
set -euo pipefail

required=(
  README.md
  ROADMAP.md
  ARCHITECTURE.md
  CHANGELOG.md
  VERSION
  configs/default.yaml
  datasets/registry/index.yaml
  experiments/index.yaml
)

for item in "${required[@]}"; do
  if [ ! -e "$item" ]; then
    echo "ERRO: item ausente: $item"
    exit 1
  fi
done

echo "Estrutura básica válida."
