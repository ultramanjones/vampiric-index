#!/usr/bin/env bash
# Refresh acute dispatches, then verify the deterministic HVI dataset.
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

python3 fetch_dispatches.py data.json
python3 fetch_us_transmission.py us_transmission.json
python3 calculate_hvi.py data.json
