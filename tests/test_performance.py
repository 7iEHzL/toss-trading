import unittest

import pandas as pd

from backtest.performance import calculate_performance


class PerformanceTests(unittest.TestCase):
    def test_standard_metrics_and_benchmark(self):
        dates = pd.to_datetime(["2025-01-01", "2025-07-02", "2026-01-01"])
        metrics = calculate_performance(
            [100.0, 80.0, 121.0], dates, 100.0,
            trades=[{"notional": 50.0}, {"notional": 55.0}],
            benchmark=pd.Series([100.0, 105.0, 110.0], index=dates),
        )

        self.assertAlmostEqual(metrics["total_return"], 0.21)
        self.assertAlmostEqual(metrics["cagr"], 0.21, places=3)
        self.assertAlmostEqual(metrics["mdd"], -0.20)
        self.assertAlmostEqual(metrics["calmar"], 1.05, places=2)
        self.assertAlmostEqual(metrics["benchmark_return"], 0.10)
        self.assertAlmostEqual(metrics["excess_return"], 0.11)
        self.assertGreater(metrics["turnover"], 0)


if __name__ == "__main__":
    unittest.main()
