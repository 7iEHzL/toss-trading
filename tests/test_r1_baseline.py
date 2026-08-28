import unittest
from datetime import datetime

import pandas as pd

from data.snapshot import DataSnapshot
from research.r1_baseline import COST_SCENARIOS_BPS, run_r1_development


def make_snapshot(adjusted=True):
    dates = pd.bdate_range("2015-01-01", "2023-02-01")
    prices = {}
    for offset, symbol in enumerate(("AMD", "TSLA", "AMZN", "AAPL", "SPXL", "SPY")):
        close = pd.Series(range(len(dates)), dtype=float) * (0.01 + offset * 0.001) + 100 + offset
        prices[symbol] = pd.DataFrame({"date": dates, "open": close, "close": close})
    return DataSnapshot(
        "synthetic-r1", datetime(2023, 2, 2), prices,
        universe=list(prices), source_name="unit-test",
        metadata={"adjusted": adjusted},
    )


class R1BaselineTests(unittest.TestCase):
    def test_development_runner_seals_oos_and_runs_cost_scenarios(self):
        results = run_r1_development(make_snapshot())

        self.assertEqual(tuple(results), COST_SCENARIOS_BPS)
        for bps, result in results.items():
            self.assertLessEqual(result["close_df"].index.max(), pd.Timestamp("2022-12-31"))
            self.assertEqual(result["research_report"]["region"], "DEVELOPMENT_ONLY")
            self.assertTrue(result["research_report"]["final_oos_sealed"])
            self.assertNotIn("SPXL", result["research_report"]["universe"])
            self.assertEqual(result["research_report"]["slippage_bps"], bps)
            self.assertEqual(result["benchmarks"]["primary"], "SPY")
            self.assertIn("secondary_return", result["benchmarks"])

    def test_spxl_is_only_in_explicit_robustness_run(self):
        result = run_r1_development(make_snapshot(), include_spxl=True)[10]
        self.assertIn("SPXL", result["research_report"]["universe"])

    def test_unadjusted_snapshot_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "adjusted"):
            run_r1_development(make_snapshot(adjusted=False))


if __name__ == "__main__":
    unittest.main()
