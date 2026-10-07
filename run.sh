#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo ".venv bulunamadi. Ilk once ./setup.sh calistirin."
  exit 1
fi

source .venv/bin/activate
export PYTHONPATH="$PWD"
python main.py
