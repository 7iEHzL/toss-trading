from collections import defaultdict
import math

import pandas as pd


PERIODS = (
    ("2015-2016", pd.Timestamp("2015-01-01"), pd.Timestamp("2016-12-31")),
    ("2017-2018", pd.Timestamp("2017-01-01"), pd.Timestamp("2018-12-31")),
    ("2019-2020", pd.Timestamp("2019-01-01"), pd.Timestamp("2020-12-31")),
    ("2021-2022", pd.Timestamp("2021-01-01"), pd.Timestamp("2022-12-31")),
)


def attribute_rotation_result(result):
    """Reconcile a rotation result into exact daily symbol-level P&L sources."""
    close_df = result["close_df"]
    open_df = result["open_df"]
    equity = list(result["equity_curve"])
    dates = close_df.index[-len(equity):]
    trades_by_date = defaultdict(list)
    for trade in result["trades"]:
        trades_by_date[pd.Timestamp(trade["date"])].append(trade)

    positions = defaultdict(int)
    daily_rows = []
    holding_days = defaultdict(int)
    prior_equity = float(result["initial_cash"])
    previous_date = None

    for equity_index, date in enumerate(dates):
        quantities_before = dict(positions)
        overnight = defaultdict(float)
        if previous_date is not None:
            for symbol, quantity in quantities_before.items():
                overnight[symbol] = quantity * (
                    float(open_df.loc[date, symbol])
                    - float(close_df.loc[previous_date, symbol])
                )

        costs = defaultdict(float)
        for trade in trades_by_date[date]:
            symbol = trade["symbol"]
            quantity = int(trade["qty"])
            if trade["action"] == "BUY":
                positions[symbol] += quantity
            elif trade["action"] == "SELL":
                positions[symbol] -= quantity
                if positions[symbol] == 0:
                    del positions[symbol]
            else:
                raise ValueError(f"unsupported trade action: {trade['action']}")
            costs[symbol] += float(trade["commission"]) + float(trade["slippage_cost"])

        intraday = defaultdict(float)
        for symbol, quantity in positions.items():
            intraday[symbol] = quantity * (
                float(close_df.loc[date, symbol])
                - float(open_df.loc[date, symbol])
            )
            holding_days[symbol] += 1

        symbols = set(overnight) | set(intraday) | set(costs)
        contributions = {}
        for symbol in symbols:
            contributions[symbol] = {
                "overnight": overnight[symbol],
                "intraday": intraday[symbol],
                "execution_cost": costs[symbol],
                "net": overnight[symbol] + intraday[symbol] - costs[symbol],
            }

        equity_change = float(equity[equity_index]) - prior_equity
        attributed_change = sum(item["net"] for item in contributions.values())
        daily_rows.append({
            "date": date,
            "equity_change": equity_change,
            "attributed_change": attributed_change,
            "reconciliation_error": equity_change - attributed_change,
            "contributions": contributions,
            "closing_positions": dict(positions),
        })
        prior_equity = float(equity[equity_index])
        previous_date = date

    by_symbol = _aggregate_by_symbol(daily_rows)
    total_holding_days = sum(holding_days.values())
    for symbol, values in by_symbol.items():
        values["holding_days"] = holding_days[symbol]
        values["holding_day_share"] = (
            holding_days[symbol] / total_holding_days if total_holding_days else 0.0
        )

    absolute_net_total = sum(abs(values["net"]) for values in by_symbol.values())
    gross_path_total = sum(values["gross_absolute_daily_net"] for values in by_symbol.values())
    total_net = sum(values["net"] for values in by_symbol.values())
    for values in by_symbol.values():
        values["absolute_net_share"] = (
            abs(values["net"]) / absolute_net_total if absolute_net_total else 0.0
        )
        values["gross_path_share"] = (
            values["gross_absolute_daily_net"] / gross_path_total
            if gross_path_total else 0.0
        )
        values["net_profit_ratio"] = values["net"] / total_net if total_net else 0.0

    sell_trades = [trade for trade in result["trades"] if trade["action"] == "SELL"]
    absolute_realized_total = sum(abs(trade["realized_pnl"]) for trade in sell_trades)
    largest_trade = max(sell_trades, key=lambda trade: abs(trade["realized_pnl"]), default=None)

    max_error = max(
        (abs(row["reconciliation_error"]) for row in daily_rows), default=0.0
    )
    total_error = sum(row["reconciliation_error"] for row in daily_rows)
    if max_error > 1e-6 or abs(total_error) > 1e-4:
        raise ValueError("daily P&L attribution does not reconcile to equity")

    return {
        "daily": daily_rows,
        "by_symbol": by_symbol,
        "by_period": _aggregate_by_period(daily_rows),
        "max_daily_reconciliation_error": max_error,
        "total_reconciliation_error": total_error,
        "largest_absolute_realized_trade": largest_trade,
        "largest_trade_absolute_realized_share": (
            abs(largest_trade["realized_pnl"]) / absolute_realized_total
            if largest_trade is not None and absolute_realized_total else 0.0
        ),
        "top_absolute_realized_trades": sorted(
            sell_trades, key=lambda trade: abs(trade["realized_pnl"]), reverse=True
        )[:5],
    }


def analyze_overnight_concentration(attribution, symbol, start, end):
    """Classify whether positive overnight P&L is diffuse or gap-concentrated."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    observations = []
    for row in attribution["daily"]:
        if not start <= row["date"] <= end:
            continue
        contribution = row["contributions"].get(symbol)
        if contribution is not None and contribution["overnight"] != 0:
            observations.append({
                "date": row["date"],
                "overnight": contribution["overnight"],
            })

    positive = sorted(
        (item for item in observations if item["overnight"] > 0),
        key=lambda item: item["overnight"], reverse=True,
    )
    negative = sorted(
        (item for item in observations if item["overnight"] < 0),
        key=lambda item: item["overnight"],
    )
    positive_total = sum(item["overnight"] for item in positive)
    positive_shares = [
        item["overnight"] / positive_total for item in positive
    ] if positive_total else []

    def top_share(count):
        return sum(positive_shares[:count])

    top_1_share, top_5_share = top_share(1), top_share(5)
    if top_1_share >= 0.20 or top_5_share >= 0.50:
        classification = "EXTREME_GAP_DRIVEN"
    elif top_5_share < 0.30 and len(positive) >= 30:
        classification = "DISTRIBUTED"
    else:
        classification = "MIXED"

    values = [item["overnight"] for item in observations]
    ordered_values = sorted(values)
    midpoint = len(ordered_values) // 2
    if not ordered_values:
        median = 0.0
    elif len(ordered_values) % 2:
        median = ordered_values[midpoint]
    else:
        median = (ordered_values[midpoint - 1] + ordered_values[midpoint]) / 2

    return {
        "symbol": symbol,
        "start": start,
        "end": end,
        "classification": classification,
        "observation_days": len(observations),
        "positive_days": len(positive),
        "negative_days": len(negative),
        "positive_total": positive_total,
        "negative_total": sum(item["overnight"] for item in negative),
        "net_total": sum(values),
        "mean": sum(values) / len(values) if values else 0.0,
        "median": median,
        "top_1_positive_share": top_1_share,
        "top_5_positive_share": top_5_share,
        "top_10_positive_share": top_share(10),
        "positive_hhi": sum(share ** 2 for share in positive_shares),
        "largest_positive": positive[0] if positive else None,
        "largest_negative": negative[0] if negative else None,
        "top_positive_days": positive[:10],
    }


def analyze_exposure_normalized_returns(result, attribution, focus_symbol,
                                        start, end):
    """Separate per-dollar returns from capital scaling for held positions."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    open_df, close_df = result["open_df"], result["close_df"]
    daily = attribution["daily"]
    overnight_observations, intraday_observations = [], []

    for index, row in enumerate(daily):
        date = row["date"]
        if index > 0:
            previous_row = daily[index - 1]
            previous_date = previous_row["date"]
            for symbol, quantity in previous_row["closing_positions"].items():
                prior_close = float(close_df.loc[previous_date, symbol])
                today_open = float(open_df.loc[date, symbol])
                notional = quantity * prior_close
                daily_return = today_open / prior_close - 1
                overnight_observations.append({
                    "date": date, "symbol": symbol, "return": daily_return,
                    "notional": notional, "dollar_pnl": notional * daily_return,
                })
        for symbol, quantity in row["closing_positions"].items():
            today_open = float(open_df.loc[date, symbol])
            today_close = float(close_df.loc[date, symbol])
            notional = quantity * today_open
            daily_return = today_close / today_open - 1
            intraday_observations.append({
                "date": date, "symbol": symbol, "return": daily_return,
                "notional": notional, "dollar_pnl": notional * daily_return,
            })

    primary_overnight = [
        item for item in overnight_observations if start <= item["date"] <= end
    ]
    focus = [item for item in primary_overnight if item["symbol"] == focus_symbol]
    others = [item for item in primary_overnight if item["symbol"] != focus_symbol]
    focus_summary, others_summary = _return_observation_summary(focus), _return_observation_summary(others)
    comparable = bool(focus and others)
    return_edge = comparable and (
        focus_summary["mean_return"] - others_summary["mean_return"] >= 0.001
        and focus_summary["positive_hit_rate"]
        - others_summary["positive_hit_rate"] >= 0.05
    )
    capital_scaling = comparable and (
        focus_summary["average_notional"]
        >= 1.5 * others_summary["average_notional"]
    )
    if return_edge and capital_scaling:
        classification = "BOTH"
    elif return_edge:
        classification = "RETURN_EDGE"
    elif capital_scaling:
        classification = "CAPITAL_SCALING"
    else:
        classification = "INCONCLUSIVE"

    symbols = list(close_df.columns)
    by_symbol = {
        symbol: {
            "overnight": _return_observation_summary([
                item for item in overnight_observations if item["symbol"] == symbol
            ]),
            "intraday": _return_observation_summary([
                item for item in intraday_observations if item["symbol"] == symbol
            ]),
        }
        for symbol in symbols
    }
    focus_by_period = {}
    for label, period_start, period_end in PERIODS:
        focus_by_period[label] = _return_observation_summary([
            item for item in overnight_observations
            if item["symbol"] == focus_symbol
            and period_start <= item["date"] <= period_end
        ])

    return {
        "classification": classification,
        "focus_symbol": focus_symbol,
        "start": start,
        "end": end,
        "focus_overnight": focus_summary,
        "pooled_others_overnight": others_summary,
        "return_edge": return_edge,
        "capital_scaling": capital_scaling,
        "by_symbol": by_symbol,
        "focus_by_period": focus_by_period,
    }


def _return_observation_summary(observations):
    if not observations:
        return {
            "observations": 0, "mean_return": 0.0, "median_return": 0.0,
            "return_volatility": 0.0, "positive_hit_rate": 0.0,
            "average_notional": 0.0, "median_notional": 0.0,
            "exposure_weighted_return": 0.0, "total_dollar_pnl": 0.0,
        }
    returns = sorted(item["return"] for item in observations)
    notionals = sorted(item["notional"] for item in observations)
    mean_return = sum(returns) / len(returns)
    return {
        "observations": len(observations),
        "mean_return": mean_return,
        "median_return": _median(returns),
        "return_volatility": math.sqrt(
            sum((value - mean_return) ** 2 for value in returns) / len(returns)
        ),
        "positive_hit_rate": sum(value > 0 for value in returns) / len(returns),
        "average_notional": sum(notionals) / len(notionals),
        "median_notional": _median(notionals),
        "exposure_weighted_return": (
            sum(item["dollar_pnl"] for item in observations) / sum(notionals)
        ),
        "total_dollar_pnl": sum(item["dollar_pnl"] for item in observations),
    }


def _median(ordered_values):
    midpoint = len(ordered_values) // 2
    if len(ordered_values) % 2:
        return ordered_values[midpoint]
    return (ordered_values[midpoint - 1] + ordered_values[midpoint]) / 2


def _aggregate_by_symbol(daily_rows):
    result = {}
    for row in daily_rows:
        for symbol, item in row["contributions"].items():
            target = result.setdefault(symbol, {
                "overnight": 0.0,
                "intraday": 0.0,
                "execution_cost": 0.0,
                "net": 0.0,
                "gross_absolute_daily_net": 0.0,
            })
            for key in ("overnight", "intraday", "execution_cost", "net"):
                target[key] += item[key]
            target["gross_absolute_daily_net"] += abs(item["net"])
    return result


def _aggregate_by_period(daily_rows):
    result = {label: {} for label, _, _ in PERIODS}
    for row in daily_rows:
        for label, start, end in PERIODS:
            if start <= row["date"] <= end:
                for symbol, item in row["contributions"].items():
                    result[label][symbol] = result[label].get(symbol, 0.0) + item["net"]
                break
    return result
