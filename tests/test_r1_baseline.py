import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd

from data.snapshot import DataSnapshot
from research.r1_baseline import (
    COST_SCENARIOS_BPS,
    run_r1_development,
    run_r1_breadth_gate_development,
    run_r1_medium_term_development,
    run_r1_risk_off_development,
    run_r1_spy_regime_development,
    run_r1_top2_development,
    run_r1_volatility_adjusted_development,
    run_r2_leave_one_out_development,
)


def make_snapshot(adjusted=True):
    dates = pd.bdate_range("2015-01-01", "2023-02-01")
    prices = {}
    for offset, symbol in enumerate(("AMD", "TSLA", "AMZN", "AAPL", "SPXL", "SPY")):
        close = pd.Series(range(len(dates)), dtype=float) * (0.01 + offset * 0.001) + 100 + offset
        prices[symbol] = pd.DataFrame({"date": dates, "open": close, "close": close})
    return DataSnapshot(
        "synthetic-r1", datetime(2023, 2, 2), prices,
        universe=list(prices), source_name="unit-test",
        metadata={"adjusted": adjusted},
    )


class R1BaselineTests(unittest.TestCase):
    def test_development_runner_seals_oos_and_runs_cost_scenarios(self):
        results = run_r1_development(make_snapshot())

        self.assertEqual(tuple(results), COST_SCENARIOS_BPS)
        for bps, result in results.items():
            self.assertLessEqual(result["close_df"].index.max(), pd.Timestamp("2022-12-31"))
            self.assertEqual(result["research_report"]["region"], "DEVELOPMENT_ONLY")
            self.assertTrue(result["research_report"]["final_oos_sealed"])
            self.assertNotIn("SPXL", result["research_report"]["universe"])
            self.assertEqual(result["research_report"]["slippage_bps"], bps)
            self.assertEqual(result["benchmarks"]["primary"], "SPY")
            self.assertIn("secondary_return", result["benchmarks"])
            self.assertIn("sharpe", result["benchmarks"]["primary_metrics"])
            self.assertIn("mdd", result["benchmarks"]["secondary_metrics"])

    def test_spxl_is_only_in_explicit_robustness_run(self):
        result = run_r1_development(make_snapshot(), include_spxl=True)[10]
        self.assertIn("SPXL", result["research_report"]["universe"])

    def test_unadjusted_snapshot_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "adjusted"):
            run_r1_development(make_snapshot(adjusted=False))

    def test_risk_off_experiment_and_tsla_diagnostic_are_separate(self):
        with patch("research.r1_baseline.COST_SCENARIOS_BPS", (10,)):
            primary = run_r1_risk_off_development(make_snapshot())[10]
            diagnostic = run_r1_risk_off_development(
                make_snapshot(), exclude_tsla=True
            )[10]

        self.assertEqual(primary["research_report"]["experiment_id"], "R1-002")
        self.assertEqual(primary["research_report"]["absolute_momentum_lookback"], 126)
        self.assertIn("TSLA", primary["research_report"]["universe"])
        self.assertNotIn("TSLA", diagnostic["research_report"]["universe"])
        self.assertEqual(diagnostic["research_report"]["diagnostic"], "TSLA_EXCLUDED")

    def test_top2_experiment_is_separate_and_reports_concentration(self):
        with patch("research.r1_baseline.COST_SCENARIOS_BPS", (10,)):
            result = run_r1_top2_development(make_snapshot())[10]

        self.assertEqual(result["research_report"]["experiment_id"], "R1-003")
        self.assertEqual(result["research_report"]["top_n"], 2)
        self.assertEqual(result["research_report"]["absolute_momentum_lookback"], 126)
        self.assertEqual(result["concentration"]["basis"],
                         "TRADE_LEDGER_REALIZED_PNL")
        self.assertIn("max_absolute_realized_pnl_share", result["concentration"])

    def test_medium_term_experiment_changes_only_registered_score_weight(self):
        with patch("research.r1_baseline.COST_SCENARIOS_BPS", (10,)):
            baseline = run_r1_risk_off_development(make_snapshot())[10]
            candidate = run_r1_medium_term_development(make_snapshot())[10]

        self.assertEqual(candidate["research_report"]["experiment_id"], "R1-004")
        self.assertEqual(candidate["research_report"]["relative_momentum_weights"],
                         [0.0, 1.0, 1.0])
        self.assertEqual(candidate["research_report"]["top_n"], 1)
        self.assertEqual(candidate["research_report"]["absolute_momentum_lookback"], 126)
        self.assertEqual(baseline["research_report"]["relative_momentum_weights"],
                         [1.0, 1.0, 1.0])

    def test_bounded_batch_runners_preserve_registered_parameters(self):
        snapshot = make_snapshot()
        with patch("research.r1_baseline.COST_SCENARIOS_BPS", (10,)):
            volatility = run_r1_volatility_adjusted_development(snapshot)[10]
            breadth = run_r1_breadth_gate_development(snapshot)[10]
            regime = run_r1_spy_regime_development(snapshot)[10]

        self.assertEqual(volatility["research_report"]["experiment_id"], "R1-005")
        self.assertEqual(volatility["research_report"]["score_volatility_lookback"], 63)
        self.assertEqual(breadth["research_report"]["experiment_id"], "R1-006")
        self.assertEqual(breadth["research_report"]["minimum_positive_breadth"], 2)
        self.assertEqual(regime["research_report"]["experiment_id"], "R1-007")
        self.assertEqual(regime["research_report"]["market_regime_lookback"], 126)
        for result in (volatility, breadth, regime):
            self.assertTrue(result["research_report"]["final_oos_sealed"])
            self.assertEqual(result["research_report"]["top_n"], 1)
            self.assertEqual(result["research_report"]["absolute_momentum_lookback"], 126)

    def test_r2_leave_one_out_runs_every_exclusion_as_audit_only(self):
        with patch("research.r1_baseline.COST_SCENARIOS_BPS", (10,)):
            audit = run_r2_leave_one_out_development(make_snapshot())

        self.assertEqual(set(audit["leave_one_out"]),
                         {"AMD", "TSLA", "AMZN", "AAPL"})
        self.assertEqual(audit["reference"][10]["research_report"]["experiment_id"],
                         "R1-002")
        for excluded, scenarios in audit["leave_one_out"].items():
            result = scenarios[10]
            report = result["research_report"]
            self.assertEqual(report["experiment_id"], "R2-001")
            self.assertEqual(report["excluded_symbol"], excluded)
            self.assertTrue(report["audit_only"])
            self.assertTrue(report["final_oos_sealed"])
            self.assertNotIn(excluded, report["universe"])
            self.assertEqual(len(report["universe"]), 3)


if __name__ == "__main__":
    unittest.main()
