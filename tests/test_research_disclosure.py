import unittest
from datetime import datetime

import pandas as pd

from backtest.multifactor_engine import run_multifactor_rotation_backtest
from backtest.research import BIASED_RESEARCH_MODE
from data.snapshot import DataSnapshot


class ResearchDisclosureTests(unittest.TestCase):
    def test_static_fundamentals_are_marked_biased_in_report_and_metrics(self):
        frame = pd.DataFrame({
            "date": pd.date_range("2026-01-01", periods=4),
            "open": [100.0, 101.0, 102.0, 103.0],
            "close": [100.0, 101.0, 102.0, 103.0],
            "volume": [100, 101, 102, 103],
        })
        result = run_multifactor_rotation_backtest(
            {"AAA": frame}, {"AAA": {"roe": 0.1, "pbr": 1.0}},
            initial_cash=1000, momentum_lookback=2, volume_lookback=1,
            top_n=1,
        )

        for report in (result["research_report"], result["performance"]):
            self.assertEqual(report["research_mode"], BIASED_RESEARCH_MODE)
            self.assertFalse(report["fundamentals_point_in_time"])
            self.assertIn("not point-in-time", report["warnings"][0])

    def test_snapshot_exposes_storage_neutral_provenance(self):
        snapshot = DataSnapshot(
            snapshot_id="prices-2026-01-31-v1",
            as_of=datetime(2026, 1, 31, 12, 0),
            prices={"AAA": pd.DataFrame({"close": [100.0]})},
            universe=["AAA"], source_name="synthetic-test",
            metadata={"adjusted": True},
        )

        self.assertEqual(snapshot.provenance(), {
            "snapshot_id": "prices-2026-01-31-v1",
            "as_of": "2026-01-31T12:00:00",
            "source_name": "synthetic-test",
            "universe_size": 1,
            "metadata": {"adjusted": True},
        })


if __name__ == "__main__":
    unittest.main()
