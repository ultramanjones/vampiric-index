"""Deterministic tests for the US liquidity transmission scoring helpers."""

import unittest
from datetime import date

import fetch_us_transmission as transmission


class TransmissionScoringTests(unittest.TestCase):
    def test_parse_fred_csv_skips_missing_values(self):
        raw_csv = (
            "observation_date,TEST\n"
            "2026-01-01,1.5\n"
            "2026-02-01,.\n"
            "2026-03-01,2.5\n"
        ).encode("utf-8")

        self.assertEqual(
            transmission.parse_fred_csv(raw_csv, "TEST"),
            [
                {"date": date(2026, 1, 1), "value": 1.5},
                {"date": date(2026, 3, 1), "value": 2.5},
            ],
        )

    def test_debt_saturation_increases_with_delinquency_and_credit_growth(self):
        low_score, _ = transmission.score_debt_saturation(
            {"value": 1.5, "change": -0.1}, {"percent_change": 1.0}
        )
        high_score, _ = transmission.score_debt_saturation(
            {"value": 8.0, "change": 0.5}, {"percent_change": 7.0}
        )

        self.assertEqual(low_score, 3.0)
        self.assertEqual(high_score, 25.0)

    def test_corporate_stress_responds_to_spread_level_and_widening(self):
        calm_score, _ = transmission.score_corporate_stress({"value": 3.0, "change": -0.2})
        stressed_score, _ = transmission.score_corporate_stress({"value": 8.0, "change": 1.0})

        self.assertEqual(calm_score, 2.0)
        self.assertEqual(stressed_score, 23.0)

    def test_predatory_extraction_has_non_linear_apr_redline(self):
        normal_score, _, _ = transmission.score_predatory_extraction(
            {"value": 17.0}, {"value": 700000.0}
        )
        redline_score, _, interest = transmission.score_predatory_extraction(
            {"value": 21.2}, {"value": 1352000.0}
        )

        self.assertLess(normal_score, 5.0)
        self.assertGreaterEqual(redline_score, 16.0)
        self.assertAlmostEqual(interest, 286.6)

    def test_breathing_room_accounts_for_price_squeeze_and_credit_dependence(self):
        safer_score, _ = transmission.score_breathing_room(
            {"value": 8.0}, {"value": 1.5}, {"value": 14.0}, {"value": 700000.0}, {"percent_change": 2.0}
        )
        squeezed_score, diagnosis = transmission.score_breathing_room(
            {"value": 4.1}, {"value": 2.85}, {"value": 21.19}, {"value": 1352414.0}, {"percent_change": 3.46}
        )

        self.assertLess(safer_score, 5.0)
        self.assertGreaterEqual(squeezed_score, 15.0)
        self.assertIn("price", diagnosis.lower())
        self.assertIn("revolving credit", diagnosis.lower())

    def test_qsr_deflator_series_is_declared(self):
        series = transmission.SERIES["food_away_from_home_cpi"]
        self.assertEqual(series["id"], "CUUR0000SEFV")
        self.assertIn("deflate", series["description"].lower())

    def test_active_phase_uses_furthest_material_phase(self):
        phases = [
            {"number": 1, "name": "one", "score": 17.0},
            {"number": 2, "name": "two", "score": 5.0},
            {"number": 3, "name": "three", "score": 13.0},
            {"number": 4, "name": "four", "score": 9.0},
        ]

        active = transmission.active_phase(phases)

        self.assertEqual(active["number"], 3)
        self.assertEqual(active["status"], "material signal")


if __name__ == "__main__":
    unittest.main()
