#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

printf '\nKurulum tamamlandi. Calistirmak icin:\n'
printf '  source .venv/bin/activate\n'
printf '  PYTHONPATH="$PWD" python main.py\n'
