import unittest

import pandas as pd

from data.sources.pit_membership import PitIndexMembershipSource


class FakePitIndex:
    @staticmethod
    def info(index):
        return {"index": index, "source": "fake"}

    @staticmethod
    def get_constituents(as_of, index):
        return pd.DataFrame({"ticker": [f"T{i:03d}" for i in range(500)]})

    @staticmethod
    def get_constituents_history(start, end, index):
        frame = FakePitIndex.get_constituents(start, index)
        frame["as_of"] = start
        return frame


class PitMembershipTests(unittest.TestCase):
    def test_normalizes_point_in_time_membership(self):
        result = PitIndexMembershipSource(FakePitIndex).constituents("2020-01-02")
        self.assertEqual(len(result), 500)
        self.assertEqual(result["as_of"].nunique(), 1)
        self.assertTrue(result["membership_source"].eq("pitindex").all())

    def test_rejects_final_oos_request(self):
        with self.assertRaisesRegex(ValueError, "Final OOS"):
            PitIndexMembershipSource(FakePitIndex).constituents("2023-01-01")


if __name__ == "__main__":
    unittest.main()
