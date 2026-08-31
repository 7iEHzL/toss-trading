import unittest

import pandas as pd

from data.r3_validator import (
    classify_audit, constituent_date_coverage, coverage_report,
    validate_price_frame_r3,
)
from data.sources.yahoo_price_source import YahooPriceSource


class FakeYahoo:
    __version__ = "fake"

    @staticmethod
    def download(*args, **kwargs):
        return pd.DataFrame()


def valid_raw():
    dates = pd.bdate_range("2014-07-01", periods=130, name="Date")
    return pd.DataFrame({
        "Open": 100.0, "High": 102.0, "Low": 99.0,
        "Close": 101.0, "Volume": 1000,
    }, index=dates)


class FakeBatchYahoo:
    __version__ = "fake"

    @staticmethod
    def download(tickers, **kwargs):
        if isinstance(tickers, str):
            return valid_raw()
        return pd.concat({ticker: valid_raw() for ticker in tickers}, axis=1)


class R3PriceCoverageTests(unittest.TestCase):

    def test_validator_tolerates_only_machine_precision_ohlc_noise(self):
        frame = pd.DataFrame({
            "date": pd.to_datetime(["2015-01-30"]),
            "open": [10.0], "high": [11.0], "low": [9.0 + 4e-15],
            "close": [9.0], "volume": [100.0],
        })
        validate_price_frame_r3(frame, "EEM")
        frame.loc[0, "low"] = 9.001
        with self.assertRaisesRegex(ValueError, "low is inconsistent"):
            validate_price_frame_r3(frame, "EEM")
    def test_no_final_oos_download_is_dispatched(self):
        with self.assertRaisesRegex(ValueError, "Final OOS"):
            YahooPriceSource(FakeYahoo).download("AAA", end_exclusive="2023-01-02")

    def test_missing_ticker_is_reported_and_blocks(self):
        membership = pd.DataFrame({
            "as_of": pd.Timestamp("2020-01-02"),
            "ticker": [f"T{i:03d}" for i in range(100)],
        })
        prices = {
            f"T{i:03d}": pd.DataFrame({"date": pd.to_datetime(["2020-01-02"])})
            for i in range(97)
        }
        mappings = {f"T{i:03d}": "exact" for i in range(97)}
        report = coverage_report(membership, prices, mappings)
        self.assertEqual(report["missing_count"], 3)
        self.assertFalse(report["price_gate_passed"])
        self.assertTrue(classify_audit(report, True).startswith("BLOCKED"))

    def test_constituent_date_coverage_uses_pit_states(self):
        membership = pd.DataFrame({
            "as_of": pd.to_datetime(["2020-01-02", "2020-01-02"]),
            "ticker": ["AAA", "BBB"],
        })
        prices = {
            "AAA": pd.DataFrame({"date": pd.to_datetime(["2020-01-02", "2020-01-03"])}),
            "BBB": pd.DataFrame({"date": pd.to_datetime(["2020-01-02"])}),
        }
        result = constituent_date_coverage(membership, prices)
        self.assertEqual(result["requested"], 4)
        self.assertEqual(result["available"], 3)
        self.assertEqual(result["coverage_ratio"], 0.75)


if __name__ == "__main__":
    unittest.main()
