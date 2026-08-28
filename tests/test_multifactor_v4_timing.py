import unittest

import pandas as pd

from backtest.multifactor_engine_v4 import run_multifactor_rotation_backtest_v4
from backtest.multifactor_engine_v4_1 import run_multifactor_rotation_backtest_v4_1


FUNDAMENTALS = {"AAA": {"roe": 0.1, "pbr": 1.0}}


def make_trending_data(periods, final_open=None):
    closes = [100.0 + i for i in range(periods)]
    opens = closes.copy()
    if final_open is not None:
        opens[-1] = final_open

    return {
        "AAA": pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=periods),
                "open": opens,
                "high": [value + 1 for value in closes],
                "low": [value - 1 for value in closes],
                "close": closes,
                "volume": [100 + i for i in range(periods)],
            }
        )
    }


class MultifactorV41TimingTests(unittest.TestCase):
    def test_inverse_volatility_plan_executes_at_next_open(self):
        result = run_multifactor_rotation_backtest_v4_1(
            make_trending_data(22, final_open=150.0),
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
        self.assertEqual(trade["weight"], 1.0)


class MultifactorV4TimingTests(unittest.TestCase):
    def run_v4(self, data, rebalance_interval=100):
        return run_multifactor_rotation_backtest_v4(
            data,
            FUNDAMENTALS,
            initial_cash=1000,
            momentum_lookback=2,
            absolute_momentum_lookback=2,
            volume_lookback=1,
            ma_window=2,
            rebalance_interval=rebalance_interval,
            top_n=1,
            atr_window=2,
            atr_multiplier=0.5,
        )

    def test_rebalance_executes_at_next_open(self):
        result = self.run_v4(make_trending_data(22, final_open=150.0))

        trade = result["trades"][0]
        self.assertEqual(trade["reason"], "REBALANCE")
        self.assertEqual(trade["signal_date"], pd.Timestamp("2026-01-21"))
        self.assertEqual(trade["date"], pd.Timestamp("2026-01-22"))
        self.assertEqual(trade["price"], 150.0)

    def test_atr_stop_signal_executes_at_following_open(self):
        data = make_trending_data(24)
        frame = data["AAA"]
        frame.loc[21, ["open", "high", "low", "close"]] = [121.0, 131.0, 120.0, 130.0]
        frame.loc[22, ["open", "high", "low", "close"]] = [129.0, 100.0, 89.0, 90.0]
        frame.loc[23, ["open", "high", "low", "close"]] = [80.0, 91.0, 79.0, 85.0]

        result = self.run_v4(data)
        stop_trade = next(
            trade for trade in result["trades"]
            if trade["action"] == "SELL" and trade["reason"] == "ATR_STOP"
        )

        self.assertEqual(stop_trade["signal_date"], pd.Timestamp("2026-01-23"))
        self.assertEqual(stop_trade["date"], pd.Timestamp("2026-01-24"))
        self.assertEqual(stop_trade["price"], 80.0)


if __name__ == "__main__":
    unittest.main()
