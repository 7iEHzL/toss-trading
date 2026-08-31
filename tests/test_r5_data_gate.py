import unittest

import pandas as pd

from data.r5_development_snapshot import (
    END_EXCLUSIVE, R5_UNIVERSE, R5YahooPriceSource, audit_r5_frames,
)


def frame(start="2006-02-03", end="2014-12-31"):
    dates = pd.bdate_range(start, end)
    close = pd.Series(range(len(dates)), dtype=float) / 100 + 50
    return pd.DataFrame({
        "date": dates, "open": close, "high": close + 1,
        "low": close - 1, "close": close, "volume": 1000,
    })


class FakeYFinance:
    __version__ = "fake"

    @staticmethod
    def download(*args, **kwargs):
        source = frame().set_index("date")
        source.index.name = "Date"
        return source.rename(columns=str.title)


class R5DataGateTests(unittest.TestCase):
    def test_complete_frames_pass(self):
        audit = audit_r5_frames({ticker: frame() for ticker in R5_UNIVERSE})
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["minimum_coverage"], 1.0)

    def test_first_post_inception_trading_day_is_valid(self):
        prices = {ticker: frame() for ticker in R5_UNIVERSE}
        prices["DBC"] = prices["DBC"].iloc[1:].reset_index(drop=True)
        audit = audit_r5_frames(prices)
        self.assertTrue(audit["passed"])
        self.assertGreaterEqual(audit["minimum_coverage"], 0.95)

    def test_missing_or_sparse_frame_fails(self):
        prices = {ticker: frame() for ticker in R5_UNIVERSE}
        prices["DBC"] = prices["DBC"].iloc[200:].reset_index(drop=True)
        self.assertFalse(audit_r5_frames(prices)["passed"])
        prices.pop("GLD")
        self.assertFalse(audit_r5_frames(prices)["passed"])

    def test_source_refuses_post_2014_request(self):
        source = R5YahooPriceSource(FakeYFinance)
        with self.assertRaisesRegex(ValueError, "sealed"):
            source.download("SPY", end_exclusive="2015-01-02")

    def test_mock_download_stays_before_boundary(self):
        result = R5YahooPriceSource(FakeYFinance).download("SPY")
        self.assertLess(result["date"].max(), pd.Timestamp(END_EXCLUSIVE))


if __name__ == "__main__":
    unittest.main()
