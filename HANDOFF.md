# Vampiric Index — Resumption Handoff

## Completed & Verified
- `calculate_hvi.py`: Deterministic HVI calculation (0-100) and grading engine verified.
- `data.json`: Pilot baseline data for US, GB, FR, DE, MX with 4 pillars, pathologies, and live news dispatches.
- `fetch_dispatches.py`: Google News RSS scraper parsed and verified.
- Model driver: Hermes running stably on `gpt-5.6-terra`.

## Pending Steps (From PROJECT_BLUEPRINT.md)
1. **Git Commit & Push**:
   - Files staged: `calculate_hvi.py`, `data.json`, `fetch_dispatches.py`, `TASK.md`.
   - Complete GitHub CLI authentication (`gh auth login`) to push to remote.
2. **Step 4: Frontend Web Dashboard (`index.html`)**:
   - D3.js SVG world map (Equal Earth projection).
   - Dynamic fetch of `./data.json` coloring nations by HVI Grade.
   - Interactive dossier slide-out modal.
3. **Step 5: Pipeline Runner (`run_pipeline.sh`)**:
   - Orchestrates fetch and calculation validation.
