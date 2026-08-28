import unittest

import pandas as pd

from backtest.costs import ExecutionCostModel
from backtest.multifactor_engine import run_multifactor_rotation_backtest
from backtest.multifactor_engine_v2 import run_multifactor_rotation_backtest_v2
from backtest.multifactor_engine_v3 import run_multifactor_rotation_backtest_v3
from backtest.multifactor_engine_v4 import run_multifactor_rotation_backtest_v4
from backtest.multifactor_engine_v4_1 import run_multifactor_rotation_backtest_v4_1
from backtest.rotation_engine import run_rotation_backtest


FUNDAMENTALS = {"AAA": {"roe": 0.1, "pbr": 1.0}}
COSTS = ExecutionCostModel(commission_rate=0.01, slippage_bps=100)


def data(periods, with_range=False):
    close = [100.0 + i for i in range(periods)]
    frame = {
        "date": pd.date_range("2026-01-01", periods=periods),
        "open": close.copy(), "close": close,
        "volume": [100 + i for i in range(periods)],
    }
    if with_range:
        frame["high"] = [price + 1 for price in close]
        frame["low"] = [price - 1 for price in close]
    return {"AAA": pd.DataFrame(frame)}


class CostModelIntegrationTests(unittest.TestCase):
    def assert_costed(self, result):
        buy = result["trades"][0]
        self.assertGreater(buy["price"], buy["reference_price"])
        self.assertGreater(buy["commission"], 0)
        self.assertGreater(buy["slippage_cost"], 0)
        self.assertGreater(result["total_commission"], 0)
        self.assertGreater(result["total_slippage_cost"], 0)
        self.assertIn("average_cost", result["positions"]["AAA"])
        self.assertIn("sharpe", result["performance"])

    def test_rotation_uses_common_cost_and_accounting(self):
        result = run_rotation_backtest(
            data(3), initial_cash=1000, lookback_1m=1, lookback_3m=1,
            lookback_6m=1, cost_model=COSTS,
        )
        self.assert_costed(result)

    def test_all_multifactor_versions_use_common_cost_and_accounting(self):
        calls = [
            (run_multifactor_rotation_backtest, data(4), {
                "momentum_lookback": 2, "volume_lookback": 1,
            }),
            (run_multifactor_rotation_backtest_v2, data(4), {
                "momentum_lookback": 2, "absolute_momentum_lookback": 2,
                "volume_lookback": 1, "ma_window": 2,
            }),
            (run_multifactor_rotation_backtest_v3, data(22), {
                "momentum_lookback": 2, "absolute_momentum_lookback": 2,
                "volume_lookback": 1, "ma_window": 2,
            }),
            (run_multifactor_rotation_backtest_v4, data(22, True), {
                "momentum_lookback": 2, "absolute_momentum_lookback": 2,
                "volume_lookback": 1, "ma_window": 2, "atr_window": 2,
            }),
            (run_multifactor_rotation_backtest_v4_1, data(22), {
                "momentum_lookback": 2, "absolute_momentum_lookback": 2,
                "volume_lookback": 1, "ma_window": 2,
            }),
        ]
        for function, dataset, parameters in calls:
            with self.subTest(engine=function.__name__):
                result = function(
                    dataset, FUNDAMENTALS, initial_cash=1000, top_n=1,
                    cost_model=COSTS, **parameters
                )
                self.assert_costed(result)


if __name__ == "__main__":
    unittest.main()
