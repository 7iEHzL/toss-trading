import unittest

import pandas as pd

from backtest.rotation_engine import run_rotation_backtest


class RotationBacktestTimingTests(unittest.TestCase):
    def make_data(self):
        return {
            "AAA": pd.DataFrame(
                {
                    "date": pd.to_datetime(
                        ["2026-01-05", "2026-01-06", "2026-01-07"]
                    ),
                    "open": [100.0, 105.0, 120.0],
                    "close": [100.0, 110.0, 130.0],
                }
            )
        }

    def test_close_score_executes_at_next_open(self):
        result = run_rotation_backtest(
            self.make_data(),
            initial_cash=1000,
            lookback_1m=1,
            lookback_3m=1,
            lookback_6m=1,
            rebalance_interval=5,
        )

        self.assertEqual(len(result["trades"]), 1)
        trade = result["trades"][0]
        self.assertEqual(trade["signal_date"], pd.Timestamp("2026-01-06"))
        self.assertEqual(trade["date"], pd.Timestamp("2026-01-07"))
        self.assertEqual(trade["price"], 120.0)
        self.assertEqual(trade["qty"], 8)
        self.assertEqual(result["final_value"], 1080.0)

        log = result["rebalance_logs"][0]
        self.assertEqual(log["date"], pd.Timestamp("2026-01-06"))
        self.assertEqual(log["execution_date"], pd.Timestamp("2026-01-07"))

    def test_last_bar_rebalance_has_no_execution(self):
        result = run_rotation_backtest(
            self.make_data(),
            initial_cash=1000,
            lookback_1m=1,
            lookback_3m=1,
            lookback_6m=1,
            rebalance_interval=1,
        )

        self.assertEqual(len(result["trades"]), 1)
        self.assertIsNone(result["rebalance_logs"][-1]["execution_date"])

    def test_missing_open_column_is_rejected(self):
        data = self.make_data()
        data["AAA"] = data["AAA"].drop(columns=["open"])

        with self.assertRaisesRegex(ValueError, "open"):
            run_rotation_backtest(data)


if __name__ == "__main__":
    unittest.main()
