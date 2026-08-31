import pandas as pd

from backtest.costs import ExecutionCostModel
from backtest.performance import calculate_performance
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
    universe = SPXL_ROBUSTNESS_UNIVERSE if include_spxl else PRIMARY_UNIVERSE
    return _run_r1_development(
        snapshot, universe, initial_cash,
        experiment_id="R1-001", absolute_momentum_lookback=None,
        diagnostic="SPXL_INCLUDED" if include_spxl else None,
        top_n=1, relative_momentum_weights=(1.0, 1.0, 1.0),
    )


def run_r1_risk_off_development(snapshot, exclude_tsla=False,
                                initial_cash=100000.0):
    """Run pre-registered R1-002 without exposing final OOS."""
    universe = tuple(
        symbol for symbol in PRIMARY_UNIVERSE
        if not (exclude_tsla and symbol == "TSLA")
    )
    return _run_r1_development(
        snapshot, universe, initial_cash,
        experiment_id="R1-002", absolute_momentum_lookback=126,
        diagnostic="TSLA_EXCLUDED" if exclude_tsla else None,
        top_n=1, relative_momentum_weights=(1.0, 1.0, 1.0),
    )


def run_r4a_asset_class_development(snapshot, universe, initial_cash=100000.0):
    """Run frozen R1-002 on the separately frozen R4A asset-class universe."""
    results = _run_r1_development(
        snapshot, tuple(universe), initial_cash,
        experiment_id="R4A-001", absolute_momentum_lookback=126,
        diagnostic="FROZEN_ASSET_CLASS_UNIVERSE", top_n=1,
        relative_momentum_weights=(1.0, 1.0, 1.0),
        frame_preparer=_r4a_development_frame,
    )
    warning = (
        "R4A uses a pre-registered fixed ETF universe and is an asset-class "
        "replication, not stock-level PIT or survivorship-free replication."
    )
    for result in results.values():
        result["research_report"]["warnings"] = [warning]
    return results


def run_r1_top2_development(snapshot, initial_cash=100000.0):
    """Run pre-registered R1-003 in the development region only."""
    return _run_r1_development(
        snapshot, PRIMARY_UNIVERSE, initial_cash,
        experiment_id="R1-003", absolute_momentum_lookback=126,
        diagnostic=None, top_n=2,
        relative_momentum_weights=(1.0, 1.0, 1.0),
    )


def run_r1_medium_term_development(snapshot, initial_cash=100000.0):
    """Run pre-registered R1-004 in the development region only."""
    return _run_r1_development(
        snapshot, PRIMARY_UNIVERSE, initial_cash,
        experiment_id="R1-004", absolute_momentum_lookback=126,
        diagnostic=None, top_n=1,
        relative_momentum_weights=(0.0, 1.0, 1.0),
    )


def run_r1_volatility_adjusted_development(snapshot, initial_cash=100000.0):
    """Run pre-registered R1-005 in the development region only."""
    return _run_r1_development(
        snapshot, PRIMARY_UNIVERSE, initial_cash,
        experiment_id="R1-005", absolute_momentum_lookback=126,
        diagnostic=None, top_n=1,
        relative_momentum_weights=(1.0, 1.0, 1.0),
        score_volatility_lookback=63,
    )


def run_r1_breadth_gate_development(snapshot, initial_cash=100000.0):
    """Run pre-registered R1-006 in the development region only."""
    return _run_r1_development(
        snapshot, PRIMARY_UNIVERSE, initial_cash,
        experiment_id="R1-006", absolute_momentum_lookback=126,
        diagnostic=None, top_n=1,
        relative_momentum_weights=(1.0, 1.0, 1.0),
        breadth_momentum_lookback=126, minimum_positive_breadth=2,
    )


def run_r1_spy_regime_development(snapshot, initial_cash=100000.0):
    """Run pre-registered R1-007 in the development region only."""
    return _run_r1_development(
        snapshot, PRIMARY_UNIVERSE, initial_cash,
        experiment_id="R1-007", absolute_momentum_lookback=126,
        diagnostic=None, top_n=1,
        relative_momentum_weights=(1.0, 1.0, 1.0),
        market_regime_lookback=126,
    )


def run_r2_leave_one_out_development(snapshot, initial_cash=100000.0):
    """Audit frozen R1-002 dependence without selecting a new universe."""
    reference = run_r1_risk_off_development(
        snapshot, initial_cash=initial_cash
    )
    diagnostics = {}
    for excluded_symbol in PRIMARY_UNIVERSE:
        universe = tuple(
            symbol for symbol in PRIMARY_UNIVERSE if symbol != excluded_symbol
        )
        results = _run_r1_development(
            snapshot, universe, initial_cash,
            experiment_id="R2-001", absolute_momentum_lookback=126,
            diagnostic=f"{excluded_symbol}_EXCLUDED", top_n=1,
            relative_momentum_weights=(1.0, 1.0, 1.0),
        )
        for result in results.values():
            result["research_report"]["excluded_symbol"] = excluded_symbol
            result["research_report"]["audit_only"] = True
        diagnostics[excluded_symbol] = results
    return {"reference": reference, "leave_one_out": diagnostics}


def _run_r1_development(snapshot, universe, initial_cash, experiment_id,
                        absolute_momentum_lookback, diagnostic, top_n,
                        relative_momentum_weights,
                        score_volatility_lookback=None,
                        breadth_momentum_lookback=None,
                        minimum_positive_breadth=None,
                        market_regime_lookback=None, frame_preparer=None):
    if snapshot.metadata.get("adjusted") is not True:
        raise ValueError("R1 requires adjusted price data")

    required = set(universe) | {PRIMARY_BENCHMARK}
    missing = required.difference(snapshot.prices)
    if missing:
        raise ValueError(f"snapshot missing R1 symbols: {', '.join(sorted(missing))}")

    prepare = frame_preparer or _development_frame
    data = {symbol: prepare(snapshot.prices[symbol]) for symbol in universe}
    spy = _close_series(prepare(snapshot.prices[PRIMARY_BENCHMARK]))
    equal_weight = _equal_weight_benchmark(data)

    results = {}
    for slippage_bps in COST_SCENARIOS_BPS:
        result = run_rotation_backtest(
            data, initial_cash=initial_cash,
            lookback_1m=21, lookback_3m=63, lookback_6m=126,
            weight_1m=relative_momentum_weights[0],
            weight_3m=relative_momentum_weights[1],
            weight_6m=relative_momentum_weights[2],
            rebalance_interval=5,
            cost_model=ExecutionCostModel(slippage_bps=slippage_bps),
            benchmark=spy,
            absolute_momentum_lookback=absolute_momentum_lookback,
            top_n=top_n,
            score_volatility_lookback=score_volatility_lookback,
            breadth_momentum_lookback=breadth_momentum_lookback,
            minimum_positive_breadth=minimum_positive_breadth,
            market_regime=(spy if market_regime_lookback is not None else None),
            market_regime_lookback=market_regime_lookback,
        )
        result["concentration"] = _realized_pnl_concentration(result["trades"])
        evaluation_dates = result["close_df"].index[126:]
        primary = spy.reindex(evaluation_dates).dropna()
        secondary = equal_weight.reindex(evaluation_dates).dropna()
        primary_metrics = calculate_performance(
            primary / primary.iloc[0] * initial_cash,
            primary.index, initial_cash,
        )
        secondary_metrics = calculate_performance(
            secondary / secondary.iloc[0] * initial_cash,
            secondary.index, initial_cash,
        )
        secondary_return = secondary.iloc[-1] / secondary.iloc[0] - 1
        result["benchmarks"] = {
            "primary": PRIMARY_BENCHMARK,
            "primary_return": result["performance"]["benchmark_return"],
            "primary_metrics": primary_metrics,
            "secondary": "UNIVERSE_EQUAL_WEIGHT_BUY_AND_HOLD",
            "secondary_return": float(secondary_return),
            "secondary_metrics": secondary_metrics,
            "excess_vs_secondary": (
                result["performance"]["total_return"] - secondary_return
            ),
        }
        result["research_report"] = {
            "experiment_id": experiment_id,
            "region": "DEVELOPMENT_ONLY",
            "final_oos_sealed": True,
            "universe": list(universe),
            "diagnostic": diagnostic,
            "absolute_momentum_lookback": absolute_momentum_lookback,
            "top_n": top_n,
            "relative_momentum_weights": list(relative_momentum_weights),
            "score_volatility_lookback": score_volatility_lookback,
            "breadth_momentum_lookback": breadth_momentum_lookback,
            "minimum_positive_breadth": minimum_positive_breadth,
            "market_regime_lookback": market_regime_lookback,
            "slippage_bps": slippage_bps,
            "warnings": [EX_POST_UNIVERSE_WARNING],
            "data_provenance": snapshot.provenance(),
        }
        results[slippage_bps] = result
    return results


def _realized_pnl_concentration(trades):
    """Trade-ledger diagnostic; this is not full portfolio return attribution."""
    by_symbol = {}
    for trade in trades:
        if trade["action"] == "SELL":
            symbol = trade["symbol"]
            by_symbol[symbol] = by_symbol.get(symbol, 0.0) + trade["realized_pnl"]
    absolute_total = sum(abs(value) for value in by_symbol.values())
    if not by_symbol or absolute_total == 0:
        return {
            "realized_pnl_by_symbol": by_symbol,
            "dominant_symbol": None,
            "max_absolute_realized_pnl_share": 0.0,
            "basis": "TRADE_LEDGER_REALIZED_PNL",
        }
    dominant = max(by_symbol, key=lambda symbol: abs(by_symbol[symbol]))
    return {
        "realized_pnl_by_symbol": by_symbol,
        "dominant_symbol": dominant,
        "max_absolute_realized_pnl_share": (
            abs(by_symbol[dominant]) / absolute_total
        ),
        "basis": "TRADE_LEDGER_REALIZED_PNL",
    }


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


def _r4a_development_frame(frame):
    """Keep exactly 126 pre-2015 rows as warm-up for the R4A evaluation."""
    required = {"date", "open", "close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"R4A data missing columns: {', '.join(sorted(missing))}")
    result = frame.copy()
    result["date"] = pd.to_datetime(result["date"])
    result = result[result["date"] <= DEVELOPMENT_END].sort_values("date")
    warmup = result[result["date"] < DEVELOPMENT_START].tail(126)
    evaluation = result[result["date"] >= DEVELOPMENT_START]
    if len(warmup) < 126 or evaluation.empty:
        raise ValueError("R4A requires 126 pre-development warm-up rows")
    return pd.concat([warmup, evaluation], ignore_index=True)


def _close_series(frame):
    return frame.set_index("date")["close"].astype(float)


def _equal_weight_benchmark(data):
    closes = pd.concat(
        {symbol: _close_series(frame) for symbol, frame in data.items()}, axis=1
    ).dropna()
    normalized = closes.divide(closes.iloc[0])
    return normalized.mean(axis=1)
