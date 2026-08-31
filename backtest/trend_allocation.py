"""Long/cash independent trend with optional inverse-volatility allocation."""

import math

import pandas as pd

from backtest.accounting import build_backtest_result, execute_target_rebalance
from backtest.costs import ExecutionCostModel
from backtest.portfolio import Portfolio


def run_independent_trend_backtest(data, initial_cash=100000.0, slippage_bps=10,
                                   evaluation_start="2007-03-01",
                                   use_trend=True, inverse_volatility=True,
                                   ewma_decay=60 / 61):
    if not 0 < ewma_decay < 1:
        raise ValueError("ewma_decay must be between zero and one")
    open_df, close_df = _aligned_prices(data)
    returns = close_df.pct_change()
    volatility = returns.ewm(alpha=1 - ewma_decay, adjust=False).std(bias=True)
    month_end = set(close_df.groupby(close_df.index.to_period("M")).tail(1).index)
    portfolio = Portfolio(initial_cash, ExecutionCostModel(slippage_bps=slippage_bps))
    pending = None
    equity_curve, dates, rebalance_logs = [], [], []

    for index, date in enumerate(close_df.index):
        if pending is not None:
            execute_target_rebalance(
                portfolio, list(pending["weights"]), open_df.loc[date].to_dict(),
                len(equity_curve), date, pending["signal_date"], pending["scores"],
                weights=pending["weights"], reason="MONTHLY_TREND_REBALANCE",
            )
            pending = None

        if date >= pd.Timestamp(evaluation_start):
            equity_curve.append(portfolio.equity(close_df.loc[date].to_dict()))
            dates.append(date)

        if (date not in month_end or index + 1 >= len(close_df)
                or close_df.index[index + 1] < pd.Timestamp(evaluation_start)):
            continue
        target_date = date - pd.DateOffset(years=1)
        history = close_df.index[close_df.index <= target_date]
        if history.empty or volatility.loc[date].isna().any():
            continue
        prior_date = history[-1]
        trailing = close_df.loc[date] / close_df.loc[prior_date] - 1
        active = list(trailing[trailing > 0].index) if use_trend else list(close_df.columns)
        if inverse_volatility:
            raw = {symbol: 1 / float(volatility.loc[date, symbol]) for symbol in active
                   if math.isfinite(float(volatility.loc[date, symbol]))
                   and float(volatility.loc[date, symbol]) > 0}
        else:
            raw = {symbol: 1.0 for symbol in active}
        total = sum(raw.values())
        weights = {symbol: value / total for symbol, value in raw.items()} if total else {}
        pending = {
            "signal_date": date, "weights": weights,
            "scores": {symbol: float(trailing[symbol]) for symbol in close_df.columns},
        }
        rebalance_logs.append({
            "signal_date": date, "execution_date": close_df.index[index + 1],
            "active_assets": active, "weights": weights,
        })

    if not equity_curve:
        raise ValueError("no R5 evaluation observations")
    return build_backtest_result(
        portfolio, equity_curve, dates, initial_cash,
        close_df.loc[dates[-1]].to_dict(), open_df=open_df, close_df=close_df,
        rebalance_logs=rebalance_logs,
        research_disclosure={"research_mode": "STANDARD_RESEARCH_MODE",
                             "fundamentals_point_in_time": None, "warnings": []},
    )


def _aligned_prices(data):
    opens, closes = {}, {}
    for symbol, frame in data.items():
        required = {"date", "open", "close"}
        if missing := required.difference(frame.columns):
            raise ValueError(f"{symbol} missing columns: {', '.join(sorted(missing))}")
        indexed = frame.copy()
        indexed["date"] = pd.to_datetime(indexed["date"])
        indexed = indexed.set_index("date").sort_index()
        opens[symbol] = indexed["open"].astype(float)
        closes[symbol] = indexed["close"].astype(float)
    return pd.DataFrame(opens).dropna(), pd.DataFrame(closes).dropna()
