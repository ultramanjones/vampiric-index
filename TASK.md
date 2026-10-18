
# Task: Step 1 & Step 2 Implementation for Vampiric Index

Read this file and execute the following within the current directory:

1. Create `calculate_hvi.py`:
   - Purely deterministic Python arithmetic calculating the Host Viability Index (HVI) scaled 0–100.
   - Four 25-point pillars:
     * survival_floor (0–25)
     * sovereign_cannibalization (0–25)
     * labor_retention (0–25)
     * state_coercion (0–25)
   - Assign grades: A (85–100), B (70–84), C (55–69), D (40–54), F (<40).
   - Use standard library only (`json`, `sys`, `pathlib`).

2. Create `data.json`:
   - Baseline pilot entries for: US, FR, GB, DE, MX.
   - Schema per nation:
     * country_code (ISO-2)
     * name
     * pillars (the four sub-scores)
     * hvi_score & grade
     * chronic_pathologies (array of 4–5 verified systemic vulnerabilities)
     * acute_dispatch (empty array `[]`)

3. Verify:
   - Run `python3 calculate_hvi.py` against `data.json` to verify parsing and math.
   - Print the execution table to stdout when complete.
EOF
