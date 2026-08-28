import pandas as pd

from backtest.performance import calculate_performance
from backtest.portfolio import Portfolio


def run_rotation_backtest(
    data_dict, initial_cash=10000000, lookback_1m=21, lookback_3m=63,
    lookback_6m=126, weight_1m=1.0, weight_3m=1.0, weight_6m=1.0,
    rebalance_interval=5, cost_model=None, benchmark=None,
):
    if not data_dict:
        raise ValueError("stock data must not be empty")
    close_df, open_df = pd.DataFrame(), pd.DataFrame()
    for ticker, frame in data_dict.items():
        missing = {"date", "open", "close"}.difference(frame.columns)
        if missing:
            raise ValueError(f"{ticker} missing required columns: {', '.join(sorted(missing))}")
        temp = frame.copy()
        temp["date"] = pd.to_datetime(temp["date"])
        temp = temp.sort_values("date").set_index("date")
        close_df[ticker], open_df[ticker] = temp["close"], temp["open"]
    valid = close_df.notna().all(axis=1) & open_df.notna().all(axis=1)
    close_df, open_df = close_df.loc[valid], open_df.loc[valid]
    score_df = (weight_1m * close_df.pct_change(lookback_1m)
                + weight_3m * close_df.pct_change(lookback_3m)
                + weight_6m * close_df.pct_change(lookback_6m))
    start_index = max(lookback_1m, lookback_3m, lookback_6m)
    if len(close_df) <= start_index:
        raise ValueError(f"insufficient data: need {start_index + 1}, got {len(close_df)}")

    portfolio = Portfolio(initial_cash, cost_model)
    equity_curve, holding_history, rebalance_logs = [], [], []
    pending_rebalance = None
    for i in range(start_index, len(close_df)):
        today, close_prices, open_prices = close_df.index[i], close_df.iloc[i], open_df.iloc[i]
        scores = score_df.iloc[i]
        if pending_rebalance is not None:
            winner = pending_rebalance["winner"]
            if next(iter(portfolio.holdings), None) != winner:
                portfolio.rebalance(
                    {winner: 1.0}, open_prices, index=len(equity_curve), date=today,
                    signal_date=pending_rebalance["signal_date"],
                    score=pending_rebalance["winner_score"],
                )
            pending_rebalance = None
        if (i - start_index) % rebalance_interval == 0:
            winner, winner_score = scores.idxmax(), scores.max()
            current = next(iter(portfolio.holdings), None)
            execution_date = close_df.index[i + 1] if i + 1 < len(close_df) else None
            rebalance_logs.append({
                "index": len(equity_curve), "date": today,
                "execution_date": execution_date, "winner": winner,
                "winner_score": winner_score, "holding": current,
                "changed": current != winner, "scores": scores.to_dict(),
            })
            if not pd.isna(winner_score) and execution_date is not None:
                pending_rebalance = {"winner": winner, "winner_score": winner_score, "signal_date": today}
        equity_curve.append(portfolio.equity(close_prices))
        holding_history.append(next(iter(portfolio.holdings), None))

    dates = close_df.index[start_index:]
    metrics = calculate_performance(equity_curve, dates, initial_cash, portfolio.trades, benchmark)
    summary = portfolio.summary(close_df.iloc[-1])
    return {
        "initial_cash": initial_cash, "final_value": equity_curve[-1],
        "return_pct": metrics["total_return"] * 100, "mdd": metrics["mdd"] * 100,
        "mdd_peak_index": dates.get_loc(metrics["mdd_peak_date"]),
        "mdd_trough_index": dates.get_loc(metrics["mdd_trough_date"]),
        "trades": portfolio.trades, "equity_curve": equity_curve,
        "holding_history": holding_history, "score_df": score_df,
        "close_df": close_df, "open_df": open_df, "rebalance_logs": rebalance_logs,
        "performance": metrics, **summary,
    }
