import unittest

import pandas as pd

from backtest.trend_allocation import run_independent_trend_backtest


class R5TrendTests(unittest.TestCase):
    def test_month_end_signal_executes_at_next_open(self):
        dates = pd.bdate_range("2019-01-01", "2020-03-31")
        close = pd.Series(range(len(dates)), dtype=float) / 10 + 50
        data = {"AAA": pd.DataFrame({"date": dates, "open": close, "close": close})}
        result = run_independent_trend_backtest(data, evaluation_start="2020-03-01")
        self.assertTrue(result["trades"])
        first = result["trades"][0]
        self.assertGreater(pd.Timestamp(first["date"]), pd.Timestamp(first["signal_date"]))

    def test_negative_trend_stays_in_cash(self):
        dates = pd.bdate_range("2019-01-01", "2020-03-31")
        close = pd.Series(range(len(dates), 0, -1), dtype=float) + 50
        data = {"AAA": pd.DataFrame({"date": dates, "open": close, "close": close})}
        result = run_independent_trend_backtest(data, evaluation_start="2020-03-01")
        self.assertEqual(result["trades"], [])
        self.assertEqual(result["final_value"], result["initial_cash"])


if __name__ == "__main__":
    unittest.main()
