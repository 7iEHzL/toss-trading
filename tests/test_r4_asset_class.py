import unittest
from datetime import datetime

import pandas as pd

from data.r4_development_snapshot import R4A_UNIVERSE
from data.snapshot import DataSnapshot
from research.r4_asset_class import run_r4a_001


class R4AssetClassTests(unittest.TestCase):
    def test_runner_preserves_frozen_strategy_and_oos_seal(self):
        dates = pd.bdate_range("2014-07-01", "2023-03-01")
        prices = {}
        for offset, ticker in enumerate(R4A_UNIVERSE):
            close = pd.Series(range(len(dates)), dtype=float) * (0.01 + offset / 10000) + 50
            prices[ticker] = pd.DataFrame({"date": dates, "open": close, "close": close})
        snapshot = DataSnapshot(
            "synthetic-r4a", datetime(2023, 3, 2), prices,
            universe=R4A_UNIVERSE, metadata={"adjusted": True},
        )
        results = run_r4a_001(snapshot)
        for bps, result in results.items():
            report = result["research_report"]
            self.assertEqual(report["experiment_id"], "R4A-001")
            self.assertEqual(report["absolute_momentum_lookback"], 126)
            self.assertEqual(report["top_n"], 1)
            self.assertEqual(report["relative_momentum_weights"], [1.0, 1.0, 1.0])
            self.assertEqual(report["slippage_bps"], bps)
            self.assertTrue(report["final_oos_sealed"])
            self.assertGreaterEqual(result["close_df"].index[126],
                                    pd.Timestamp("2015-01-01"))
            self.assertLess(result["close_df"].index.max(), pd.Timestamp("2023-01-01"))


if __name__ == "__main__":
    unittest.main()
