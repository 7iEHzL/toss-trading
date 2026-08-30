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

    def test_absolute_momentum_risk_off_sells_at_next_open(self):
        data = {
            "AAA": pd.DataFrame({
                "date": pd.date_range("2026-01-05", periods=5),
                "open": [100.0, 110.0, 120.0, 90.0, 70.0],
                "close": [100.0, 110.0, 120.0, 90.0, 80.0],
            })
        }
        result = run_rotation_backtest(
            data, initial_cash=1000,
            lookback_1m=1, lookback_3m=1, lookback_6m=1,
            rebalance_interval=1, absolute_momentum_lookback=1,
        )

        sell = next(trade for trade in result["trades"] if trade["action"] == "SELL")
        self.assertEqual(sell["signal_date"], pd.Timestamp("2026-01-08"))
        self.assertEqual(sell["date"], pd.Timestamp("2026-01-09"))
        self.assertEqual(sell["reference_price"], 70.0)
        risk_off_log = next(log for log in result["rebalance_logs"] if log["risk_off"])
        self.assertEqual(risk_off_log["winner"], "AAA")
        self.assertIsNone(risk_off_log["target_winner"])

    def test_invalid_absolute_momentum_lookback_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            run_rotation_backtest(
                self.make_data(), lookback_1m=1, lookback_3m=1,
                lookback_6m=1, absolute_momentum_lookback=0,
            )

    def test_top2_executes_equal_weight_at_next_open(self):
        dates = pd.date_range("2026-01-05", periods=3)
        data = {
            "AAA": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 120.0, 120.0],
            }),
            "BBB": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 110.0, 110.0],
            }),
            "CCC": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 90.0, 90.0],
            }),
        }
        result = run_rotation_backtest(
            data, initial_cash=1000, lookback_1m=1, lookback_3m=1,
            lookback_6m=1, rebalance_interval=5, top_n=2,
        )

        self.assertEqual(result["holdings"], {"AAA": 5, "BBB": 5})
        self.assertEqual(result["rebalance_logs"][0]["selected_winners"],
                         ["AAA", "BBB"])
        self.assertEqual(result["rebalance_logs"][0]["target_weights"],
                         {"AAA": 0.5, "BBB": 0.5})
        self.assertEqual(result["trades"][0]["date"], dates[2])

    def test_top2_negative_absolute_momentum_slot_stays_cash(self):
        dates = pd.date_range("2026-01-05", periods=3)
        data = {
            "AAA": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 120.0, 120.0],
            }),
            "BBB": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 95.0, 95.0],
            }),
            "CCC": pd.DataFrame({
                "date": dates, "open": [100.0, 100.0, 100.0],
                "close": [100.0, 90.0, 90.0],
            }),
        }
        result = run_rotation_backtest(
            data, initial_cash=1000, lookback_1m=1, lookback_3m=1,
            lookback_6m=1, rebalance_interval=5,
            absolute_momentum_lookback=1, top_n=2,
        )

        self.assertEqual(result["holdings"], {"AAA": 5})
        self.assertEqual(result["cash"], 500.0)
        self.assertTrue(result["rebalance_logs"][0]["risk_off"])
        self.assertEqual(result["rebalance_logs"][0]["target_weights"],
                         {"AAA": 0.5})

    def test_invalid_top_n_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            run_rotation_backtest(self.make_data(), top_n=0)

    def test_volatility_adjustment_changes_only_ranking_scale(self):
        dates = pd.date_range("2026-01-05", periods=5)
        data = {
            "AAA": pd.DataFrame({
                "date": dates, "open": [100.0] * 5,
                "close": [100.0, 150.0, 100.0, 150.0, 150.0],
            }),
            "BBB": pd.DataFrame({
                "date": dates, "open": [100.0] * 5,
                "close": [100.0, 105.0, 110.0, 120.0, 120.0],
            }),
        }
        result = run_rotation_backtest(
            data, lookback_1m=1, lookback_3m=1, lookback_6m=1,
            rebalance_interval=1, score_volatility_lookback=2,
        )

        second_signal = result["rebalance_logs"][1]
        self.assertEqual(second_signal["winner"], "BBB")
        self.assertGreater(second_signal["scores"]["BBB"],
                           second_signal["scores"]["AAA"])

    def test_breadth_gate_moves_target_to_cash(self):
        dates = pd.date_range("2026-01-05", periods=3)
        data = {
            symbol: pd.DataFrame({
                "date": dates, "open": [100.0] * 3, "close": closes,
            })
            for symbol, closes in {
                "AAA": [100.0, 110.0, 110.0],
                "BBB": [100.0, 90.0, 90.0],
                "CCC": [100.0, 80.0, 80.0],
            }.items()
        }
        result = run_rotation_backtest(
            data, lookback_1m=1, lookback_3m=1, lookback_6m=1,
            absolute_momentum_lookback=1,
            breadth_momentum_lookback=1, minimum_positive_breadth=2,
        )

        self.assertEqual(result["trades"], [])
        self.assertTrue(result["rebalance_logs"][0]["breadth_gate"])
        self.assertEqual(result["rebalance_logs"][0]["positive_breadth"], 1)

    def test_market_regime_gate_moves_target_to_cash(self):
        dates = pd.date_range("2026-01-05", periods=3)
        data = {"AAA": pd.DataFrame({
            "date": dates, "open": [100.0] * 3,
            "close": [100.0, 110.0, 110.0],
        })}
        regime = pd.Series([100.0, 90.0, 90.0], index=dates)
        result = run_rotation_backtest(
            data, lookback_1m=1, lookback_3m=1, lookback_6m=1,
            absolute_momentum_lookback=1,
            market_regime=regime, market_regime_lookback=1,
        )

        self.assertEqual(result["trades"], [])
        self.assertTrue(result["rebalance_logs"][0]["market_regime_gate"])
        self.assertLess(result["rebalance_logs"][0]["market_regime_momentum"], 0)


if __name__ == "__main__":
    unittest.main()
