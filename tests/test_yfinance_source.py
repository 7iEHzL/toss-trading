import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from data.yfinance_source import (
    R1_END_EXCLUSIVE,
    load_r1_development_snapshot,
    validate_price_frame,
)


def valid_frame():
    return pd.DataFrame({
        "date": pd.to_datetime(["2015-01-02", "2015-01-05"]),
        "open": [100.0, 101.0], "high": [102.0, 103.0],
        "low": [99.0, 100.0], "close": [101.0, 102.0],
        "volume": [1000, 1100],
    })


class YFinanceSourceValidationTests(unittest.TestCase):
    def test_valid_frame_passes(self):
        validate_price_frame(valid_frame(), "AAA")

    def test_tiny_adjustment_rounding_difference_is_allowed(self):
        frame = valid_frame()
        frame.loc[0, "high"] = frame.loc[0, "close"] - 1e-12
        validate_price_frame(frame, "AAA")

    def test_final_oos_date_is_rejected(self):
        frame = valid_frame()
        frame.loc[1, "date"] = pd.Timestamp(R1_END_EXCLUSIVE)
        with self.assertRaisesRegex(ValueError, "outside"):
            validate_price_frame(frame, "AAA")

    def test_bad_price_and_duplicate_date_are_rejected(self):
        bad_price = valid_frame()
        bad_price.loc[0, "open"] = 0
        with self.assertRaisesRegex(ValueError, "positive"):
            validate_price_frame(bad_price, "AAA")

        duplicate = valid_frame()
        duplicate.loc[1, "date"] = duplicate.loc[0, "date"]
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_price_frame(duplicate, "AAA")

    def test_manifest_refuses_final_oos_flag(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = {
                "requested_end_exclusive": R1_END_EXCLUSIVE,
                "final_oos_downloaded": True,
                "adjusted": True,
                "symbols": ["AMD", "TSLA", "AMZN", "AAPL", "SPXL", "SPY"],
            }
            Path(temp_dir, "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "final OOS"):
                load_r1_development_snapshot(temp_dir)


if __name__ == "__main__":
    unittest.main()
