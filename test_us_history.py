"""Integrity checks for the U.S. no-interpolation history feed."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent


class USHistoryTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "us_history.json").read_text())
        self.series = {item["key"]: item for item in self.payload["series"]}

    def test_all_five_series_are_present_and_cited(self):
        expected = {"pay_reaching_households", "cost_of_staying_alive", "breathing_room_debt", "labor_leverage", "customer_cash"}
        self.assertEqual(set(self.series), expected)
        for item in self.series.values():
            self.assertTrue(item["url"].startswith("https://fred.stlouisfed.org/"))
            self.assertGreater(len(item["observations"]), 20)
            self.assertEqual(item["observations"], sorted(item["observations"]))

    def test_long_run_data_starts_no_later_than_1970_except_debt_service(self):
        for key, item in self.series.items():
            first = item["observations"][0][0]
            if key == "breathing_room_debt":
                self.assertEqual(first, "2005-01-01")
            else:
                self.assertLessEqual(first, "1970-01-01")


if __name__ == "__main__":
    unittest.main()
