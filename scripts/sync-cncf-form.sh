#!/usr/bin/env bash
set -euo pipefail

# Sync local CNCF form artifacts from cncf/sandbox application.yml.
#
# Prerequisites:
#   - python3
#   - PyYAML (pip install -r requirements-dev.txt)
#
# Usage:
#   ./scripts/sync-cncf-form.sh --report
#   ./scripts/sync-cncf-form.sh --check
#   ./scripts/sync-cncf-form.sh --write --merge-application
#   ./scripts/sync-cncf-form.sh --write --merge-application --ref main

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYNC="${ROOT_DIR}/scripts/sync_cncf_form.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required." >&2
  exit 1
fi

if ! python3 -c "import yaml" >/dev/null 2>&1; then
  echo "Error: PyYAML is required. Install with: pip install -r requirements-dev.txt" >&2
  exit 1
fi

exec python3 "${SYNC}" "$@"
