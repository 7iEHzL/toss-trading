import pandas as pd

from backtest.performance import calculate_performance


def execute_target_rebalance(portfolio, winners, open_prices, equity_index,
                             date, signal_date, scores, weights=None,
                             reason=None):
    if weights is None:
        weights = ({symbol: 1.0 / len(winners) for symbol in winners}
                   if winners else {})
    metadata = {
        "index": equity_index,
        "date": date,
        "signal_date": signal_date,
    }
    before = len(portfolio.trades)
    portfolio.rebalance(weights, open_prices, **metadata)
    for trade in portfolio.trades[before:]:
        if trade["symbol"] in scores:
            trade["score"] = scores[trade["symbol"]]
        if trade["symbol"] in weights:
            trade["weight"] = weights[trade["symbol"]]
        if reason is not None:
            trade["reason"] = reason


def build_backtest_result(portfolio, equity_curve, dates, initial_cash,
                          final_prices, benchmark=None, research_disclosure=None,
                          data_provenance=None, **extra):
    dates = pd.DatetimeIndex(dates)
    metrics = calculate_performance(equity_curve, dates, initial_cash, portfolio.trades, benchmark)
    summary = portfolio.summary(final_prices)
    disclosure = research_disclosure or {
        "research_mode": "STANDARD_RESEARCH_MODE",
        "fundamentals_point_in_time": None,
        "warnings": [],
    }
    metrics.update({
        "research_mode": disclosure["research_mode"],
        "fundamentals_point_in_time": disclosure["fundamentals_point_in_time"],
        "warnings": list(disclosure["warnings"]),
    })
    return {
        "initial_cash": initial_cash,
        "final_value": equity_curve[-1],
        "return_pct": metrics["total_return"] * 100,
        "mdd": metrics["mdd"] * 100,
        "mdd_peak_index": dates.get_loc(metrics["mdd_peak_date"]),
        "mdd_trough_index": dates.get_loc(metrics["mdd_trough_date"]),
        "trades": portfolio.trades,
        "equity_curve": equity_curve,
        "performance": metrics,
        "research_report": {
            **disclosure,
            "data_provenance": data_provenance,
        },
        **summary,
        **extra,
    }
