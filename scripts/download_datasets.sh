#!/usr/bin/env bash
# Baixa os datasets de pedidos e pagamentos para data/input/
set -euo pipefail

DESTINO="data/input"
mkdir -p "$DESTINO"

clonar() {
  local repo="$1"
  if [ -d "$DESTINO/$repo" ]; then
    echo "Dataset $repo já existe em $DESTINO/$repo"
  else
    git clone --depth 1 "https://github.com/infobarbosa/$repo.git" "$DESTINO/$repo"
  fi
}

clonar datasets-csv-pedidos
clonar dataset-json-pagamentos

echo "Datasets disponíveis em $DESTINO"
