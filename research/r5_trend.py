"""Frozen R5-001 runner and pre-registered diagnostics."""

import pandas as pd

from backtest.performance import calculate_performance
from backtest.trend_allocation import run_independent_trend_backtest
from data.r5_development_snapshot import EVALUATION_START, R5_UNIVERSE
from research.attribution import attribute_rotation_result


COSTS = (0, 5, 10, 20)
BLOCKS = ((2007, 2008), (2009, 2010), (2011, 2012), (2013, 2014))
STRESS_BLOCKS = ((2015, 2016), (2017, 2018), (2019, 2020), (2021, 2022))


def run_r5_001(snapshot, initial_cash=100000.0):
    _validate_snapshot(snapshot)
    data = {symbol: snapshot.prices[symbol] for symbol in R5_UNIVERSE}
    candidate = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, EVALUATION_START, True, True
    ) for bps in COSTS}
    inverse_vol = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, EVALUATION_START, False, True
    ) for bps in COSTS}
    equal_trend = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, EVALUATION_START, True, False
    ) for bps in COSTS}
    benchmarks = _buy_hold_benchmarks(data, candidate[10], initial_cash)
    for bps, result in candidate.items():
        result["research_report"].update({
            "experiment_id": "R5-001", "final_oos_sealed": True,
            "universe": list(R5_UNIVERSE), "trend_horizon": "12_CALENDAR_MONTHS",
            "ewma_decay": 60 / 61, "rebalance": "MONTH_END_NEXT_OPEN",
            "slippage_bps": bps, "data_provenance": snapshot.provenance(),
        })
    diagnostics = _diagnostics(candidate[10], BLOCKS)
    verdict = adjudicate_r5_001(candidate, inverse_vol, equal_trend, benchmarks, diagnostics)
    return {"candidate": candidate, "inverse_volatility": inverse_vol,
            "equal_weight_trend": equal_trend, "benchmarks": benchmarks,
            "diagnostics": diagnostics, "verdict": verdict}


def run_r5_002_contaminated_stress(r5_snapshot, r4_snapshot, initial_cash=100000.0):
    """Apply the frozen R5-001 rule to known 2015-2022 data; never clean OOS."""
    _validate_snapshot(r5_snapshot)
    if r4_snapshot.metadata.get("final_oos_downloaded") is not False:
        raise ValueError("R5 stress snapshot violates Final OOS seal")
    data = {}
    for symbol in R5_UNIVERSE:
        combined = pd.concat([r5_snapshot.prices[symbol], r4_snapshot.prices[symbol]])
        combined["date"] = pd.to_datetime(combined["date"])
        combined = combined[combined["date"] < pd.Timestamp("2023-01-01")]
        data[symbol] = combined.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    candidate = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, "2015-01-01", True, True
    ) for bps in COSTS}
    inverse_vol = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, "2015-01-01", False, True
    ) for bps in COSTS}
    equal_trend = {bps: run_independent_trend_backtest(
        data, initial_cash, bps, "2015-01-01", True, False
    ) for bps in COSTS}
    benchmarks = _buy_hold_benchmarks(data, candidate[10], initial_cash)
    diagnostics = _diagnostics(candidate[10], STRESS_BLOCKS)
    return {"candidate": candidate, "inverse_volatility": inverse_vol,
            "equal_weight_trend": equal_trend, "benchmarks": benchmarks,
            "diagnostics": diagnostics,
            "label": "RESEARCHER_CONTAMINATED_STRESS_DIAGNOSTIC",
            "final_oos_sealed": True}


def adjudicate_r5_001(candidate, inverse_vol, equal_trend, benchmarks, diagnostics):
    c, iv, et = (candidate[10]["performance"], inverse_vol[10]["performance"],
                 equal_trend[10]["performance"])
    checks = {
        "sharpe_improvement": c["sharpe"] - iv["sharpe"] >= 0.10,
        "calmar_improvement": c["calmar"] - iv["calmar"] >= 0.05,
        "positive_cagr_excess": c["cagr"] > iv["cagr"],
        "mdd_not_materially_worse": c["mdd"] >= et["mdd"] - 0.03,
        "positive_blocks": diagnostics["positive_blocks"] >= 3,
        "asset_concentration": diagnostics["max_asset_contribution_share"] < 0.50,
        "period_concentration": diagnostics["max_positive_block_share"] < 0.60,
        "cost_robust": (candidate[20]["performance"]["total_return"] > 0
                        and candidate[20]["performance"]["sharpe"]
                        > inverse_vol[20]["performance"]["sharpe"]),
    }
    if not checks["sharpe_improvement"] or not checks["positive_cagr_excess"]:
        verdict = "REJECT"
    elif sum(not checks[key] for key in (
            "positive_blocks", "asset_concentration", "period_concentration", "cost_robust")) >= 2:
        verdict = "REJECT"
    elif all(checks.values()):
        verdict = "ACCEPT"
    else:
        verdict = "INCONCLUSIVE"
    return {"verdict": verdict, "checks": checks}


def _validate_snapshot(snapshot):
    if snapshot.metadata.get("adjusted") is not True:
        raise ValueError("R5 requires adjusted prices")
    if snapshot.metadata.get("final_oos_downloaded") is not False:
        raise ValueError("R5 Final OOS seal violated")
    if not snapshot.metadata.get("audit", {}).get("passed"):
        raise ValueError("R5 data gate did not pass")


def _buy_hold_benchmarks(data, reference, initial_cash):
    dates = pd.DatetimeIndex(reference["close_df"].index[-len(reference["equity_curve"]):])
    close = pd.DataFrame({symbol: frame.set_index("date")["close"] for symbol, frame in data.items()})
    opens = pd.DataFrame({symbol: frame.set_index("date")["open"] for symbol, frame in data.items()})
    close.index = pd.to_datetime(close.index)
    opens.index = pd.to_datetime(opens.index)
    close = close.reindex(dates).dropna()
    initial_open = opens.reindex(dates).iloc[0]
    equal = (close / initial_open).mean(axis=1) * initial_cash
    spy = close["SPY"] / initial_open["SPY"] * initial_cash
    return {"equal_weight": calculate_performance(equal, equal.index, initial_cash),
            "spy": calculate_performance(spy, spy.index, initial_cash)}


def _diagnostics(result, period_blocks):
    attribution = attribute_rotation_result(result)
    by_symbol = {symbol: values["net"] for symbol, values in attribution["by_symbol"].items()}
    absolute = sum(abs(value) for value in by_symbol.values())
    max_asset = max((abs(value) / absolute for value in by_symbol.values()), default=0.0)
    equity = pd.Series(result["equity_curve"],
                       index=result["close_df"].index[-len(result["equity_curve"]):])
    block_returns, positive_contributions = {}, []
    for start, end in period_blocks:
        block = equity[(equity.index.year >= start) & (equity.index.year <= end)]
        value = float(block.iloc[-1] / block.iloc[0] - 1) if len(block) > 1 else 0.0
        block_returns[f"{start}-{end}"] = value
        contribution = float(block.iloc[-1] - block.iloc[0]) if len(block) > 1 else 0.0
        if contribution > 0:
            positive_contributions.append(contribution)
    total_positive = sum(positive_contributions)
    max_positive = max(positive_contributions, default=0.0) / total_positive if total_positive else 0.0
    return {"by_symbol": by_symbol, "max_asset_contribution_share": max_asset,
            "block_returns": block_returns,
            "positive_blocks": sum(value > 0 for value in block_returns.values()),
            "max_positive_block_share": max_positive,
            "attribution_reconciliation_error": attribution["total_reconciliation_error"]}
