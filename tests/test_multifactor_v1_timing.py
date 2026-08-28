import unittest

import pandas as pd

from backtest.multifactor_engine import run_multifactor_rotation_backtest


class MultifactorV1TimingTests(unittest.TestCase):
    def make_data(self):
        return {
            "AAA": pd.DataFrame(
                {
                    "date": pd.to_datetime(
                        [
                            "2026-01-05",
                            "2026-01-06",
                            "2026-01-07",
                            "2026-01-08",
                        ]
                    ),
                    "open": [100.0, 105.0, 110.0, 120.0],
                    "close": [100.0, 105.0, 110.0, 130.0],
                    "volume": [100, 110, 120, 130],
                }
            )
        }

    def run_backtest(self, rebalance_interval=5):
        return run_multifactor_rotation_backtest(
            data_dict=self.make_data(),
            fundamental_data={"AAA": {"roe": 0.1, "pbr": 1.0}},
            initial_cash=1000,
            momentum_lookback=2,
            volume_lookback=1,
            rebalance_interval=rebalance_interval,
            top_n=1,
        )

    def test_close_score_executes_at_next_open(self):
        result = self.run_backtest()

        self.assertEqual(len(result["trades"]), 1)
        trade = result["trades"][0]
        self.assertEqual(trade["signal_date"], pd.Timestamp("2026-01-07"))
        self.assertEqual(trade["date"], pd.Timestamp("2026-01-08"))
        self.assertEqual(trade["price"], 120.0)
        self.assertEqual(trade["qty"], 8)
        self.assertEqual(result["final_value"], 1080.0)

        log = result["rebalance_logs"][0]
        self.assertEqual(log["execution_date"], pd.Timestamp("2026-01-08"))

    def test_last_bar_signal_has_no_execution(self):
        result = self.run_backtest(rebalance_interval=1)

        self.assertEqual(len(result["trades"]), 1)
        self.assertIsNone(result["rebalance_logs"][-1]["execution_date"])

    def test_missing_open_column_is_rejected(self):
        data = self.make_data()
        data["AAA"] = data["AAA"].drop(columns=["open"])

        with self.assertRaisesRegex(ValueError, "open"):
            run_multifactor_rotation_backtest(
                data,
                {"AAA": {"roe": 0.1, "pbr": 1.0}},
            )


if __name__ == "__main__":
    unittest.main()
