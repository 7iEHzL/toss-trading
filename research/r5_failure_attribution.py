"""Bounded descriptive attribution for R5 temporal instability."""

from collections import defaultdict

import pandas as pd


ASSET_GROUPS = {
    "equity": ("SPY", "EFA", "EEM"),
    "bonds_credit": ("IEF", "TLT", "LQD"),
    "real_assets": ("IYR", "GLD", "DBC"),
}


def analyze_r5_period(data, result_bundle, evaluation_start, period_end,
                      named_windows):
    candidate = result_bundle["candidate"]
    signals = analyze_monthly_signals(data, evaluation_start, period_end)
    primary = candidate[10]
    by_symbol = result_bundle["diagnostics"]["by_symbol"]
    groups = {
        group: sum(by_symbol.get(symbol, 0.0) for symbol in symbols)
        for group, symbols in ASSET_GROUPS.items()
    }
    absolute_groups = sum(abs(value) for value in groups.values())
    group_shares = {key: abs(value) / absolute_groups if absolute_groups else 0.0
                    for key, value in groups.items()}
    return {
        "signal": signals,
        "allocation": {
            "candidate_minus_no_trend_total_return": (
                primary["performance"]["total_return"]
                - result_bundle["inverse_volatility"][10]["performance"]["total_return"]
            ),
            "candidate_minus_no_trend_sharpe": (
                primary["performance"]["sharpe"]
                - result_bundle["inverse_volatility"][10]["performance"]["sharpe"]
            ),
            "candidate_minus_equal_trend_total_return": (
                primary["performance"]["total_return"]
                - result_bundle["equal_weight_trend"][10]["performance"]["total_return"]
            ),
            "candidate_minus_equal_trend_sharpe": (
                primary["performance"]["sharpe"]
                - result_bundle["equal_weight_trend"][10]["performance"]["sharpe"]
            ),
        },
        "turnover_whipsaw": {
            "transitions": signals["transitions"],
            "false_entries": signals["false_entries"],
            "false_exits": signals["false_exits"],
            "false_transition_rate": signals["false_transition_rate"],
            "turnover_10bps": primary["performance"]["turnover"],
            "trade_count_10bps": len(primary["trades"]),
        },
        "asset_contribution": {
            "by_symbol": by_symbol,
            "by_group": groups,
            "absolute_group_shares": group_shares,
            "max_asset_share": result_bundle["diagnostics"]["max_asset_contribution_share"],
        },
        "period_contribution": {
            "two_year_blocks": result_bundle["diagnostics"]["block_returns"],
            "named_windows": _window_contributions(primary, named_windows),
        },
        "cost": {
            "total_return_0bps": candidate[0]["performance"]["total_return"],
            "total_return_10bps": primary["performance"]["total_return"],
            "total_return_20bps": candidate[20]["performance"]["total_return"],
            "return_drag_0_to_10bps": (
                candidate[0]["performance"]["total_return"]
                - primary["performance"]["total_return"]
            ),
            "slippage_dollars_10bps": primary["total_slippage_cost"],
        },
    }


def analyze_monthly_signals(data, evaluation_start, period_end):
    open_df, close_df = _aligned(data)
    month_ends = list(close_df.groupby(close_df.index.to_period("M")).tail(1).index)
    observations, signs_by_symbol = [], defaultdict(list)
    for index, signal_date in enumerate(month_ends[:-1]):
        execution_dates = open_df.index[open_df.index > signal_date]
        next_signal = month_ends[index + 1]
        next_execution_dates = open_df.index[open_df.index > next_signal]
        if execution_dates.empty or next_execution_dates.empty:
            continue
        execution_date, exit_date = execution_dates[0], next_execution_dates[0]
        if execution_date < pd.Timestamp(evaluation_start) or execution_date > pd.Timestamp(period_end):
            continue
        history = close_df.index[close_df.index <= signal_date - pd.DateOffset(years=1)]
        if history.empty:
            continue
        prior_date = history[-1]
        trailing = close_df.loc[signal_date] / close_df.loc[prior_date] - 1
        payoff = open_df.loc[exit_date] / open_df.loc[execution_date] - 1
        for symbol in close_df.columns:
            sign = 1 if trailing[symbol] > 0 else -1
            hit = payoff[symbol] > 0 if sign > 0 else payoff[symbol] < 0
            row = {"signal_date": signal_date, "execution_date": execution_date,
                   "exit_date": exit_date, "symbol": symbol, "sign": sign,
                   "trailing_return": float(trailing[symbol]),
                   "subsequent_return": float(payoff[symbol]), "hit": bool(hit)}
            observations.append(row)
            signs_by_symbol[symbol].append(row)

    positive = [row for row in observations if row["sign"] > 0]
    negative = [row for row in observations if row["sign"] < 0]
    transitions = false_entries = false_exits = 0
    for rows in signs_by_symbol.values():
        for previous, current in zip(rows, rows[1:]):
            if current["sign"] == previous["sign"]:
                continue
            transitions += 1
            if current["sign"] > 0 and current["subsequent_return"] <= 0:
                false_entries += 1
            if current["sign"] < 0 and current["subsequent_return"] >= 0:
                false_exits += 1
    return {
        "observations": len(observations),
        "positive_observations": len(positive), "negative_observations": len(negative),
        "positive_mean_payoff": _mean(positive, "subsequent_return"),
        "negative_mean_payoff": _mean(negative, "subsequent_return"),
        "positive_hit_rate": _mean(positive, "hit"),
        "negative_hit_rate": _mean(negative, "hit"),
        "overall_hit_rate": _mean(observations, "hit"),
        "transitions": transitions, "false_entries": false_entries,
        "false_exits": false_exits,
        "false_transition_rate": ((false_entries + false_exits) / transitions
                                  if transitions else 0.0),
        "persistence_rate": 1 - transitions / max(len(observations) - len(signs_by_symbol), 1),
    }


def _window_contributions(result, named_windows):
    dates = result["close_df"].index[-len(result["equity_curve"]):]
    equity = pd.Series(result["equity_curve"], index=dates)
    changes = equity.diff().fillna(equity.iloc[0] - result["initial_cash"])
    output = {}
    for name, start, end in named_windows:
        mask = (changes.index >= pd.Timestamp(start)) & (changes.index <= pd.Timestamp(end))
        output[name] = float(changes.loc[mask].sum())
    covered = pd.Series(False, index=changes.index)
    for _, start, end in named_windows:
        covered |= (changes.index >= pd.Timestamp(start)) & (changes.index <= pd.Timestamp(end))
    output["outside_named_windows"] = float(changes.loc[~covered].sum())
    return output


def _aligned(data):
    opens, closes = {}, {}
    for symbol, frame in data.items():
        indexed = frame.copy()
        indexed["date"] = pd.to_datetime(indexed["date"])
        indexed = indexed.set_index("date").sort_index()
        opens[symbol], closes[symbol] = indexed["open"], indexed["close"]
    return pd.DataFrame(opens).dropna(), pd.DataFrame(closes).dropna()


def _mean(rows, key):
    return sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0
