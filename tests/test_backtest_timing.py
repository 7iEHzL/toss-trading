import unittest

import pandas as pd

from backtest.costs import ExecutionCostModel
from backtest.engine import run_signal_backtest


class SignalBacktestTimingTests(unittest.TestCase):
    def test_close_signal_executes_at_next_open(self):
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2026-01-05", "2026-01-06", "2026-01-07"]
                ),
                "open": [100.0, 120.0, 110.0],
                "close": [100.0, 130.0, 105.0],
                "buy_signal": [True, False, False],
                "sell_signal": [False, True, False],
            }
        )

        result = run_signal_backtest(df, initial_cash=1000)

        self.assertEqual(len(result["trades"]), 2)

        buy, sell = result["trades"]
        self.assertEqual(buy["signal_date"], df.loc[0, "date"])
        self.assertEqual(buy["date"], df.loc[1, "date"])
        self.assertEqual(buy["price"], 120.0)
        self.assertEqual(buy["qty"], 8)

        self.assertEqual(sell["signal_date"], df.loc[1, "date"])
        self.assertEqual(sell["date"], df.loc[2, "date"])
        self.assertEqual(sell["price"], 110.0)
        self.assertEqual(result["final_value"], 920.0)

    def test_last_bar_signal_is_not_executed_without_a_next_bar(self):
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2026-01-05", "2026-01-06"]),
                "open": [100.0, 101.0],
                "close": [100.0, 102.0],
                "buy_signal": [False, True],
                "sell_signal": [False, False],
            }
        )

        result = run_signal_backtest(df, initial_cash=1000)

        self.assertEqual(result["trades"], [])
        self.assertEqual(result["final_value"], 1000)

    def test_missing_open_column_is_rejected(self):
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2026-01-05"]),
                "close": [100.0],
                "buy_signal": [False],
                "sell_signal": [False],
            }
        )

        with self.assertRaisesRegex(ValueError, "open"):
            run_signal_backtest(df)

    def test_empty_data_is_rejected(self):
        df = pd.DataFrame(
            columns=["date", "open", "close", "buy_signal", "sell_signal"]
        )

        with self.assertRaisesRegex(ValueError, "empty"):
            run_signal_backtest(df)

    def test_commission_and_slippage_are_applied_to_cash(self):
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2026-01-05", "2026-01-06", "2026-01-07"]
                ),
                "open": [100.0, 120.0, 110.0],
                "close": [100.0, 130.0, 105.0],
                "buy_signal": [True, False, False],
                "sell_signal": [False, True, False],
            }
        )
        model = ExecutionCostModel(
            commission_rate=0.01,
            slippage_bps=100,
        )

        result = run_signal_backtest(df, initial_cash=1000, cost_model=model)

        buy, sell = result["trades"]
        self.assertAlmostEqual(buy["reference_price"], 120.0)
        self.assertAlmostEqual(buy["price"], 121.2)
        self.assertAlmostEqual(sell["reference_price"], 110.0)
        self.assertAlmostEqual(sell["price"], 108.9)
        self.assertAlmostEqual(result["total_commission"], 18.408)
        self.assertAlmostEqual(result["total_slippage_cost"], 18.4)
        self.assertAlmostEqual(result["final_value"], 883.192)

    def test_invalid_cost_parameters_are_rejected(self):
        for kwargs in (
            {"commission_rate": -0.01},
            {"slippage_bps": -1},
            {"commission_rate": float("nan")},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    ExecutionCostModel(**kwargs)


if __name__ == "__main__":
    unittest.main()
