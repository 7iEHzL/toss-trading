"""R4A-001 frozen asset-class replication and pre-registered adjudication."""

import pandas as pd

from data.r4_development_snapshot import R4A_UNIVERSE
from research.r1_baseline import run_r4a_asset_class_development


NON_EQUITY = {"IEF", "TLT", "LQD", "GLD", "DBC"}
BLOCKS = ((2015, 2016), (2017, 2018), (2019, 2020), (2021, 2022))


def run_r4a_001(snapshot, initial_cash=100000.0):
    return run_r4a_asset_class_development(snapshot, R4A_UNIVERSE, initial_cash)


def adjudicate_r4a_001(results):
    primary = results[10]
    performance = primary["performance"]
    benchmarks = primary["benchmarks"]
    spy = benchmarks["primary_metrics"]
    equal_weight = benchmarks["secondary_metrics"]
    concentration = primary["concentration"]["max_absolute_realized_pnl_share"]
    realized = primary["concentration"]["realized_pnl_by_symbol"]
    sold_assets = len(realized)
    non_equity_positive = any(realized.get(ticker, 0.0) > 0 for ticker in NON_EQUITY)
    block_returns = _block_returns(primary)
    positive_blocks = sum(value > 0 for value in block_returns.values())
    risk_adjusted_better = (
        performance["sharpe"] > max(spy["sharpe"], equal_weight["sharpe"])
        and performance["calmar"] > max(spy["calmar"], equal_weight["calmar"])
    )
    return_better = performance["total_return"] > benchmarks["secondary_return"]
    cost_consistent = all(
        result["performance"]["total_return"] > result["benchmarks"]["secondary_return"]
        for result in results.values()
    )
    accept = (risk_adjusted_better and return_better and concentration < 0.50
              and sold_assets >= 4 and non_equity_positive
              and positive_blocks >= 3 and cost_consistent)
    reject = ((not return_better and not risk_adjusted_better)
              or concentration >= 0.70 or positive_blocks <= 1)
    verdict = "ACCEPT" if accept else "REJECT" if reject else "INCONCLUSIVE"
    return {
        "verdict": verdict, "risk_adjusted_better_than_both": risk_adjusted_better,
        "return_better_than_equal_weight": return_better,
        "max_single_etf_pnl_share": concentration, "sold_assets": sold_assets,
        "non_equity_positive_pnl": non_equity_positive,
        "block_returns": block_returns, "positive_blocks": positive_blocks,
        "cost_direction_consistent": cost_consistent,
    }


def _block_returns(result):
    dates = pd.DatetimeIndex(result["close_df"].index[126:])
    equity = pd.Series(result["equity_curve"], index=dates)
    values = {}
    for start, end in BLOCKS:
        block = equity[(equity.index.year >= start) & (equity.index.year <= end)]
        values[f"{start}-{end}"] = float(block.iloc[-1] / block.iloc[0] - 1)
    return values
