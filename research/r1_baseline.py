import pandas as pd

from backtest.costs import ExecutionCostModel
from backtest.rotation_engine import run_rotation_backtest


PRIMARY_UNIVERSE = ("AMD", "TSLA", "AMZN", "AAPL")
SPXL_ROBUSTNESS_UNIVERSE = PRIMARY_UNIVERSE + ("SPXL",)
PRIMARY_BENCHMARK = "SPY"
DEVELOPMENT_START = pd.Timestamp("2015-01-01")
DEVELOPMENT_END = pd.Timestamp("2022-12-31")
FINAL_OOS_START = pd.Timestamp("2023-01-01")
FINAL_OOS_END = pd.Timestamp("2025-12-31")
COST_SCENARIOS_BPS = (0, 5, 10, 20)
EX_POST_UNIVERSE_WARNING = (
    "The R1 universe was selected ex post and may contain selection or "
    "survivorship bias."
)


def run_r1_development(snapshot, include_spxl=False, initial_cash=100000.0):
    """Run only the pre-registered development region; final OOS stays sealed."""
    if snapshot.metadata.get("adjusted") is not True:
        raise ValueError("R1 requires adjusted price data")

    universe = SPXL_ROBUSTNESS_UNIVERSE if include_spxl else PRIMARY_UNIVERSE
    required = set(universe) | {PRIMARY_BENCHMARK}
    missing = required.difference(snapshot.prices)
    if missing:
        raise ValueError(f"snapshot missing R1 symbols: {', '.join(sorted(missing))}")

    data = {symbol: _development_frame(snapshot.prices[symbol]) for symbol in universe}
    spy = _close_series(_development_frame(snapshot.prices[PRIMARY_BENCHMARK]))
    equal_weight = _equal_weight_benchmark(data)

    results = {}
    for slippage_bps in COST_SCENARIOS_BPS:
        result = run_rotation_backtest(
            data, initial_cash=initial_cash,
            lookback_1m=21, lookback_3m=63, lookback_6m=126,
            weight_1m=1.0, weight_3m=1.0, weight_6m=1.0,
            rebalance_interval=5,
            cost_model=ExecutionCostModel(slippage_bps=slippage_bps),
            benchmark=spy,
        )
        evaluation_dates = result["close_df"].index[126:]
        secondary = equal_weight.reindex(evaluation_dates).dropna()
        secondary_return = secondary.iloc[-1] / secondary.iloc[0] - 1
        result["benchmarks"] = {
            "primary": PRIMARY_BENCHMARK,
            "primary_return": result["performance"]["benchmark_return"],
            "secondary": "UNIVERSE_EQUAL_WEIGHT_BUY_AND_HOLD",
            "secondary_return": float(secondary_return),
            "excess_vs_secondary": (
                result["performance"]["total_return"] - secondary_return
            ),
        }
        result["research_report"] = {
            "experiment_id": "R1-001",
            "region": "DEVELOPMENT_ONLY",
            "final_oos_sealed": True,
            "universe": list(universe),
            "include_spxl": include_spxl,
            "slippage_bps": slippage_bps,
            "warnings": [EX_POST_UNIVERSE_WARNING],
            "data_provenance": snapshot.provenance(),
        }
        results[slippage_bps] = result
    return results


def _development_frame(frame):
    required = {"date", "open", "close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"R1 data missing columns: {', '.join(sorted(missing))}")
    result = frame.copy()
    result["date"] = pd.to_datetime(result["date"])
    mask = result["date"].between(DEVELOPMENT_START, DEVELOPMENT_END)
    result = result.loc[mask].sort_values("date").reset_index(drop=True)
    if result.empty:
        raise ValueError("snapshot has no R1 development observations")
    return result


def _close_series(frame):
    return frame.set_index("date")["close"].astype(float)


def _equal_weight_benchmark(data):
    closes = pd.concat(
        {symbol: _close_series(frame) for symbol, frame in data.items()}, axis=1
    ).dropna()
    normalized = closes.divide(closes.iloc[0])
    return normalized.mean(axis=1)
