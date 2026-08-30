import unittest

import pandas as pd

from data.r4_validator import audit_candidate, select_representatives
from data.sources.r4_yahoo_price_source import R4YahooPriceSource, normalize_r4_download
from research.r4_universe import build_r4_000_snapshot


class FakeYahoo:
    __version__ = "fake"

    def __init__(self, frame):
        self.frame = frame
        self.calls = []

    def download(self, ticker, **kwargs):
        self.calls.append((ticker, kwargs))
        return self.frame


class FakeR4Source:
    version = "fake"

    def __init__(self, frame, failed_ticker):
        self.frame = frame
        self.failed_ticker = failed_ticker

    def download(self, ticker):
        if ticker == self.failed_ticker:
            raise ValueError("no historical payload")
        return normalize_r4_download(self.frame)


class R4UniverseTests(unittest.TestCase):
    def raw_frame(self):
        dates = pd.bdate_range("2013-01-01", "2014-06-30")
        return pd.DataFrame({
            "Open": 100.0, "High": 102.0, "Low": 99.0, "Close": 101.0,
            "Adj Close": 50.5, "Volume": 100_000.0,
        }, index=pd.Index(dates, name="Date"))

    def test_source_is_hard_limited_to_r4_audit_interval(self):
        fake = FakeYahoo(self.raw_frame())
        source = R4YahooPriceSource(fake)
        frame = source.download("SPY")
        self.assertEqual(frame["date"].max(), pd.Timestamp("2014-06-30"))
        self.assertEqual(fake.calls[0][1]["end"], "2014-07-01")
        with self.assertRaises(ValueError):
            source.download("SPY", end_exclusive="2023-01-02")

    def test_adjusted_ohlc_and_raw_close_are_kept_separate(self):
        frame = normalize_r4_download(self.raw_frame())
        self.assertEqual(frame.loc[0, "close"], 50.5)
        self.assertEqual(frame.loc[0, "raw_close"], 101.0)
        self.assertEqual(frame.loc[0, "open"], 50.0)

    def test_liquidity_uses_raw_close_and_selection_rule(self):
        frame = normalize_r4_download(self.raw_frame())
        reference = frame["date"]
        low = audit_candidate({"category": "gold", "ticker": "AAA",
                               "inception_date": "2005-01-01", "exposure": "x",
                               "issuer_source": "x"}, frame, reference)
        high_frame = frame.copy()
        high_frame["volume"] *= 2
        high = audit_candidate({"category": "gold", "ticker": "BBB",
                                "inception_date": "2006-01-01", "exposure": "x",
                                "issuer_source": "x"}, high_frame, reference)
        selected = select_representatives(pd.DataFrame([low, high]))
        self.assertEqual(low["median_dollar_volume_2013"], 10_100_000.0)
        self.assertEqual(selected.loc[0, "ticker"], "BBB")

    def test_tie_breaks_by_inception_then_ticker(self):
        rows = pd.DataFrame([
            {"category": "gold", "ticker": "BBB", "inception_date": "2005-01-01",
             "median_dollar_volume_2013": 10_000_000.0, "eligible": True},
            {"category": "gold", "ticker": "AAA", "inception_date": "2005-01-01",
             "median_dollar_volume_2013": 10_000_000.0, "eligible": True},
            {"category": "gold", "ticker": "CCC", "inception_date": "2006-01-01",
             "median_dollar_volume_2013": 10_000_000.0, "eligible": True},
        ])
        self.assertEqual(select_representatives(rows).loc[0, "ticker"], "AAA")

    def test_failed_candidate_is_recorded_not_silently_dropped(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        tickers = ("SPY", "AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III")
        candidates = pd.DataFrame([
            {"category": f"category_{max(0, index - 1)}", "ticker": ticker,
             "inception_date": "2005-01-01", "exposure": "x", "issuer_source": "x"}
            for index, ticker in enumerate(tickers)
        ])
        with tempfile.TemporaryDirectory() as directory:
            candidate_path = Path(directory) / "candidates.csv"
            candidates.to_csv(candidate_path, index=False)
            with patch("research.r4_universe.CANDIDATE_PATH", candidate_path):
                audit, universe, _ = build_r4_000_snapshot(
                    Path(directory) / "snapshot", FakeR4Source(self.raw_frame(), "AAA")
                )
        failed = audit.loc[audit["ticker"] == "AAA"].iloc[0]
        self.assertFalse(failed["eligible"])
        self.assertIn("no historical payload", failed["download_error"])
        self.assertEqual(len(universe), 9)


if __name__ == "__main__":
    unittest.main()
