import unittest

import pandas as pd

from backtest.multifactor_engine_v2 import run_multifactor_rotation_backtest_v2
from backtest.multifactor_engine_v3 import run_multifactor_rotation_backtest_v3


FUNDAMENTALS = {"AAA": {"roe": 0.1, "pbr": 1.0}}


class MultifactorV2TimingTests(unittest.TestCase):
    def test_close_score_executes_at_next_open(self):
        data = {
            "AAA": pd.DataFrame(
                {
                    "date": pd.date_range("2026-01-05", periods=4),
                    "open": [100.0, 105.0, 110.0, 120.0],
                    "close": [100.0, 105.0, 110.0, 130.0],
                    "volume": [100, 110, 120, 130],
                }
            )
        }

        result = run_multifactor_rotation_backtest_v2(
            data,
            FUNDAMENTALS,
            initial_cash=1000,
            momentum_lookback=2,
            absolute_momentum_lookback=2,
            volume_lookback=1,
            ma_window=2,
            rebalance_interval=5,
            top_n=1,
        )

        trade = result["trades"][0]
        self.assertEqual(trade["signal_date"], pd.Timestamp("2026-01-07"))
        self.assertEqual(trade["date"], pd.Timestamp("2026-01-08"))
        self.assertEqual(trade["price"], 120.0)
        self.assertEqual(trade["qty"], 8)
        self.assertEqual(result["final_value"], 1080.0)


class MultifactorV3TimingTests(unittest.TestCase):
    def test_close_score_executes_at_next_open_after_full_warmup(self):
        periods = 22
        closes = [100.0 + i for i in range(periods)]
        opens = closes.copy()
        opens[-1] = 150.0
        data = {
            "AAA": pd.DataFrame(
                {
                    "date": pd.date_range("2026-01-01", periods=periods),
                    "open": opens,
                    "close": closes,
                    "volume": [100 + i for i in range(periods)],
                }
            )
        }

        result = run_multifactor_rotation_backtest_v3(
            data,
            FUNDAMENTALS,
            initial_cash=1000,
            momentum_lookback=2,
            absolute_momentum_lookback=2,
            volume_lookback=1,
            ma_window=2,
            rebalance_interval=5,
            top_n=1,
        )

        trade = result["trades"][0]
        self.assertEqual(trade["signal_date"], pd.Timestamp("2026-01-21"))
        self.assertEqual(trade["date"], pd.Timestamp("2026-01-22"))
        self.assertEqual(trade["price"], 150.0)
        self.assertEqual(trade["qty"], 6)
        self.assertEqual(result["final_value"], 826.0)

        log = result["rebalance_logs"][0]
        self.assertEqual(log["execution_date"], pd.Timestamp("2026-01-22"))


if __name__ == "__main__":
    unittest.main()
