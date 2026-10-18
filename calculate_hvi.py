"""Validate and report Host Viability Index (HVI) pilot data."""

import json
import sys
from pathlib import Path

PILLARS = (
    "survival_floor",
    "sovereign_cannibalization",
    "labor_retention",
    "state_coercion",
)


def calculate_grade(score):
    """Return the strict classic letter grade for an HVI score from 0 to 100."""
    if score >= 93:
        return "A"
    if score >= 85:
        return "B"
    if score >= 66:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def calculate_hvi(pillars):
    """Return the declared one-decimal HVI sum without binary-float artifacts."""
    return round(sum(pillars[name] for name in PILLARS), 1)


def validate_country(country):
    """Return validation errors for one country without modifying its data."""
    errors = []
    name = country.get("name", "<unnamed>") if isinstance(country, dict) else "<invalid>"

    if not isinstance(country, dict):
        return [f"{name}: entry must be an object"]

    for field in ("country_code", "name"):
        if not isinstance(country.get(field), str) or not country[field].strip():
            errors.append(f"{name}: {field} must be a non-empty string")

    pillars = country.get("pillars")
    if not isinstance(pillars, dict):
        return errors + [f"{name}: pillars must be an object"]

    for pillar in PILLARS:
        value = pillars.get(pillar)
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not 0 <= value <= 25
        ):
            errors.append(f"{name}: {pillar} must be a number from 0 to 25")

    pathologies = country.get("chronic_pathologies")
    if not isinstance(pathologies, list) or not 4 <= len(pathologies) <= 5:
        errors.append(f"{name}: chronic_pathologies must contain 4 or 5 entries")
    elif not all(isinstance(item, str) and item.strip() for item in pathologies):
        errors.append(f"{name}: chronic_pathologies entries must be non-empty strings")

    dispatches = country.get("acute_dispatch")
    if not isinstance(dispatches, list) or len(dispatches) > 2:
        errors.append(f"{name}: acute_dispatch must contain zero to two entries")
    else:
        for dispatch in dispatches:
            if not isinstance(dispatch, dict) or not all(
                isinstance(dispatch.get(field), str) and dispatch[field].strip()
                for field in ("title", "source", "publication_date", "url")
            ):
                errors.append(
                    f"{name}: acute_dispatch entries need title, source, publication_date, and url"
                )
                break

    if not errors:
        computed_score = calculate_hvi(pillars)
        computed_grade = calculate_grade(computed_score)
        if country.get("hvi_score") != computed_score:
            errors.append(
                f"{name}: hvi_score is {country.get('hvi_score')!r}, expected {computed_score:.1f}"
            )
        if country.get("grade") != computed_grade:
            errors.append(
                f"{name}: grade is {country.get('grade')!r}, expected {computed_grade!r}"
            )

    return errors


def print_table(countries):
    headers = ("Code", "Country", "Survival", "Sovereign", "Labor", "Coercion", "HVI", "Grade")
    rows = [[str(value) for value in headers]]
    for country in countries:
        pillars = country["pillars"]
        score = calculate_hvi(pillars)
        rows.append([
            country["country_code"],
            country["name"],
            f"{pillars['survival_floor']:.1f}",
            f"{pillars['sovereign_cannibalization']:.1f}",
            f"{pillars['labor_retention']:.1f}",
            f"{pillars['state_coercion']:.1f}",
            f"{score:.1f}",
            calculate_grade(score),
        ])

    widths = [max(len(row[index]) for row in rows) for index in range(len(headers))]
    for index, row in enumerate(rows):
        print("  ".join(value.ljust(widths[column]) for column, value in enumerate(row)))
        if index == 0:
            print("  ".join("-" * width for width in widths))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("data.json")
    if len(sys.argv) > 2:
        print("Usage: python3 calculate_hvi.py [data.json]", file=sys.stderr)
        return 2

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to load {path}: {error}", file=sys.stderr)
        return 1

    countries = payload.get("countries") if isinstance(payload, dict) else None
    if not isinstance(countries, list):
        print("Validation failed: top-level JSON must contain a countries array.", file=sys.stderr)
        return 1

    errors = []
    for country in countries:
        errors.extend(validate_country(country))

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print_table(countries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
