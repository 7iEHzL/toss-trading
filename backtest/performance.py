import math

import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_performance(equity_curve, dates, initial_cash, trades=None,
                          benchmark=None, risk_free_rate=0.0):
    equity = pd.Series(list(equity_curve), index=pd.to_datetime(list(dates)), dtype=float)
    if equity.empty:
        raise ValueError("equity curve must not be empty")
    returns = equity.pct_change().dropna()
    total_return = equity.iloc[-1] / float(initial_cash) - 1

    elapsed_days = max((equity.index[-1] - equity.index[0]).days, 0)
    years = elapsed_days / 365.25
    cagr = (equity.iloc[-1] / float(initial_cash)) ** (1 / years) - 1 if years > 0 else 0.0

    running_peak = equity.cummax()
    drawdowns = equity / running_peak - 1
    mdd = float(drawdowns.min())
    trough_date = drawdowns.idxmin()
    peak_date = equity.loc[:trough_date].idxmax()

    annual_volatility = float(returns.std(ddof=1) * math.sqrt(TRADING_DAYS_PER_YEAR)) if len(returns) > 1 else 0.0
    excess = returns - risk_free_rate / TRADING_DAYS_PER_YEAR
    sharpe = _safe_ratio(excess.mean() * TRADING_DAYS_PER_YEAR, annual_volatility)
    downside = returns[returns < 0]
    downside_volatility = float(downside.std(ddof=1) * math.sqrt(TRADING_DAYS_PER_YEAR)) if len(downside) > 1 else 0.0
    sortino = _safe_ratio(excess.mean() * TRADING_DAYS_PER_YEAR, downside_volatility)
    calmar = _safe_ratio(cagr, abs(mdd))

    traded_notional = sum(float(trade.get("notional", 0.0)) for trade in (trades or []))
    average_equity = float(equity.mean())
    turnover = traded_notional / average_equity if average_equity else 0.0

    result = {
        "total_return": total_return,
        "cagr": cagr,
        "annual_volatility": annual_volatility,
        "sharpe": sharpe,
        "sortino": sortino,
        "calmar": calmar,
        "mdd": mdd,
        "mdd_peak_date": peak_date,
        "mdd_trough_date": trough_date,
        "turnover": turnover,
    }
    if benchmark is not None:
        benchmark_series = pd.Series(benchmark, dtype=float).reindex(equity.index).dropna()
        if benchmark_series.empty:
            raise ValueError("benchmark has no values aligned with the equity curve")
        result["benchmark_return"] = benchmark_series.iloc[-1] / benchmark_series.iloc[0] - 1
        result["excess_return"] = total_return - result["benchmark_return"]
    return result


def _safe_ratio(numerator, denominator):
    return float(numerator / denominator) if denominator and math.isfinite(denominator) else 0.0
