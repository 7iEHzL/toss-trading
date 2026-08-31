import unittest

import pandas as pd

from research.r5_failure_attribution import analyze_monthly_signals


class R5FailureAttributionTests(unittest.TestCase):
    def test_signal_payoff_is_measured_next_open_to_next_open(self):
        dates = pd.bdate_range("2018-01-01", "2020-04-03")
        price = pd.Series(range(len(dates)), dtype=float) + 100
        data = {"AAA": pd.DataFrame({"date": dates, "open": price, "close": price})}
        result = analyze_monthly_signals(data, "2019-03-01", "2020-03-31")
        self.assertGreater(result["observations"], 0)
        self.assertEqual(result["positive_hit_rate"], 1.0)
        self.assertEqual(result["transitions"], 0)

    def test_reversing_series_records_transitions(self):
        dates = pd.bdate_range("2017-01-01", "2020-04-03")
        values = [100 + (index if index < len(dates) // 2 else len(dates) - index)
                  for index in range(len(dates))]
        data = {"AAA": pd.DataFrame({"date": dates, "open": values, "close": values})}
        result = analyze_monthly_signals(data, "2018-03-01", "2020-03-31")
        self.assertGreater(result["transitions"], 0)


if __name__ == "__main__":
    unittest.main()
