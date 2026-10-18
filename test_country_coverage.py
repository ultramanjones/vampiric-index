"""Coverage invariants for the documented nominal-GDP coverage roster."""

import json
import re
import unittest
from pathlib import Path

import calculate_hvi
import fetch_dispatches


ROOT = Path(__file__).parent


class CoverageRosterTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        self.countries = self.payload["countries"]

    def test_roster_has_expected_covered_countries_and_matches_country_data(self):
        roster = self.payload["metadata"]["coverage_roster"]
        codes = [country["country_code"] for country in self.countries]
        self.assertEqual(len(codes), 130)
        self.assertEqual(len(set(codes)), len(codes))
        self.assertEqual(codes, [item["country_code"] for item in roster["countries"]])
        self.assertEqual(roster["source"], "World Bank World Development Indicators, NY.GDP.MKTP.CD — GDP (current US$)")
        self.assertEqual([candidate["country_code"] for candidate in roster["blocked_candidates"]], ["UA", "SD", "LB"])

    def test_every_roster_country_has_fetch_dashboard_and_review_support(self):
        dashboard = (ROOT / "index.html").read_text(encoding="utf-8")
        for country in self.countries:
            code = country["country_code"]
            self.assertIn(code, fetch_dispatches.SEARCHES)
            self.assertRegex(dashboard, rf"\b{re.escape(code)}:\s*\"\d{{3}}\"")
            self.assertEqual(calculate_hvi.validate_country(country), [])
            self.assertGreaterEqual(len(country["acute_dispatch"]), 1)
            self.assertLessEqual(len(country["acute_dispatch"]), 2)
            self.assertIn("observed_readings", country["review"])
            self.assertTrue(country["review"]["decision"])


if __name__ == "__main__":
    unittest.main()
