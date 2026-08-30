import unittest

import pandas as pd

from backtest.costs import ExecutionCostModel
from backtest.rotation_engine import run_rotation_backtest
from research.attribution import (
    analyze_exposure_normalized_returns,
    analyze_overnight_concentration,
    attribute_rotation_result,
)


class ResearchAttributionTests(unittest.TestCase):
    def test_daily_attribution_reconciles_equity_with_costs(self):
        data = {
            "AAA": pd.DataFrame({
                "date": pd.date_range("2026-01-05", periods=4),
                "open": [100.0, 105.0, 120.0, 110.0],
                "close": [100.0, 110.0, 130.0, 115.0],
            })
        }
        result = run_rotation_backtest(
            data, initial_cash=1000,
            lookback_1m=1, lookback_3m=1, lookback_6m=1,
            rebalance_interval=5,
            cost_model=ExecutionCostModel(commission_rate=0.0005, slippage_bps=10),
        )

        attribution = attribute_rotation_result(result)

        self.assertLess(attribution["max_daily_reconciliation_error"], 1e-6)
        self.assertLess(abs(attribution["total_reconciliation_error"]), 1e-6)
        self.assertEqual(attribution["by_symbol"]["AAA"]["holding_days"], 2)
        self.assertGreater(attribution["by_symbol"]["AAA"]["execution_cost"], 0)
        self.assertAlmostEqual(
            attribution["by_symbol"]["AAA"]["net"],
            result["final_value"] - result["initial_cash"],
        )

    def test_distributed_overnight_classification(self):
        attribution = {"daily": [
            {
                "date": pd.Timestamp("2020-01-01") + pd.Timedelta(days=index),
                "contributions": {"AAA": {"overnight": 1.0}},
            }
            for index in range(40)
        ]}

        result = analyze_overnight_concentration(
            attribution, "AAA", "2020-01-01", "2020-12-31"
        )

        self.assertEqual(result["classification"], "DISTRIBUTED")
        self.assertAlmostEqual(result["top_5_positive_share"], 0.125)

    def test_extreme_overnight_classification(self):
        amounts = [100.0] + [1.0] * 39
        attribution = {"daily": [
            {
                "date": pd.Timestamp("2020-01-01") + pd.Timedelta(days=index),
                "contributions": {"AAA": {"overnight": amount}},
            }
            for index, amount in enumerate(amounts)
        ]}

        result = analyze_overnight_concentration(
            attribution, "AAA", "2020-01-01", "2020-12-31"
        )

        self.assertEqual(result["classification"], "EXTREME_GAP_DRIVEN")
        self.assertGreater(result["top_1_positive_share"], 0.20)

    def test_exposure_normalized_analysis_separates_return_and_scale(self):
        dates = pd.date_range("2020-01-01", periods=3)
        result = {
            "open_df": pd.DataFrame({
                "TSLA": [100.0, 102.0, 102.0],
                "OTHER": [100.0, 100.0, 99.0],
            }, index=dates),
            "close_df": pd.DataFrame({
                "TSLA": [100.0, 102.0, 102.0],
                "OTHER": [100.0, 100.0, 99.0],
            }, index=dates),
        }
        attribution = {"daily": [
            {"date": dates[0], "closing_positions": {"TSLA": 20}},
            {"date": dates[1], "closing_positions": {"OTHER": 10}},
            {"date": dates[2], "closing_positions": {}},
        ]}

        analysis = analyze_exposure_normalized_returns(
            result, attribution, "TSLA", dates[0], dates[-1]
        )

        self.assertEqual(analysis["classification"], "BOTH")
        self.assertTrue(analysis["return_edge"])
        self.assertTrue(analysis["capital_scaling"])


if __name__ == "__main__":
    unittest.main()
