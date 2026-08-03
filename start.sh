#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR/backend"
source ../.venv/bin/activate
export PYTHONPATH="$ROOT_DIR/backend${PYTHONPATH:+:$PYTHONPATH}"

if curl --fail --silent http://127.0.0.1:8000/health >/dev/null 2>&1; then
  echo "ARGUS backend already running on http://127.0.0.1:8000"
  exit 0
fi

python -m app.init_db
python -m app.load_feature_store
uvicorn app.main:app --host 0.0.0.0 --port 8000
