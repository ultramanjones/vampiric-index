"""Validation for the household-circulation v2 scorecard."""
import json
import unittest
from pathlib import Path

import build_circulation_v2 as v2

ROOT = Path(__file__).parent


class HouseholdCirculationV2Tests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        self.definition = self.payload["metadata"]["scorecards"][v2.SCORECARD_KEY]

    def test_v2_is_active_and_its_public_labels_live_in_metadata(self):
        self.assertEqual(self.payload["metadata"]["active_scorecard"], v2.SCORECARD_KEY)
        self.assertEqual(self.definition["module_order"], v2.ORDER)
        for key in v2.ORDER:
            self.assertTrue(self.definition["modules"][key]["label"])

    def test_complete_scores_are_bounded_and_reproducible(self):
        complete = 0
        for country in self.payload["countries"]:
            card = country["scorecards"][v2.SCORECARD_KEY]
            if card["status"] == "unavailable":
                self.assertTrue(card["missing_modules"])
                self.assertNotIn("hvi_score", card)
                continue
            complete += 1
            self.assertEqual(card["status"], "complete")
            self.assertEqual(set(card["modules"]), set(v2.ORDER))
            self.assertTrue(all(0 <= value <= v2.MODULE_MAX for value in card["modules"].values()))
            self.assertEqual(card["hvi_score"], round(sum(card["modules"].values()), 1))
            self.assertEqual(card["grade"], v2.grade(card["hvi_score"]))
            self.assertEqual(set(card["observed_readings"]), set(v2.ORDER))
        self.assertGreater(complete, 100)

    def test_legacy_scorecard_is_preserved_separately(self):
        for country in self.payload["countries"]:
            legacy = country["scorecards"][v2.LEGACY_KEY]
            self.assertEqual(legacy["status"], "legacy")
            self.assertEqual(legacy["modules"], country["pillars"])
            self.assertEqual(legacy["hvi_score"], country["hvi_score"])


if __name__ == "__main__":
    unittest.main()
