import pandas as pd

from backtest.performance import calculate_performance
from backtest.portfolio import Portfolio


def run_rotation_backtest(
    data_dict, initial_cash=10000000, lookback_1m=21, lookback_3m=63,
    lookback_6m=126, weight_1m=1.0, weight_3m=1.0, weight_6m=1.0,
    rebalance_interval=5, cost_model=None, benchmark=None,
    absolute_momentum_lookback=None, top_n=1,
    score_volatility_lookback=None, breadth_momentum_lookback=None,
    minimum_positive_breadth=None, market_regime=None,
    market_regime_lookback=None,
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
    if score_volatility_lookback is not None:
        if score_volatility_lookback <= 1:
            raise ValueError("score_volatility_lookback must exceed one")
        volatility = close_df.pct_change().rolling(score_volatility_lookback).std()
        score_df = score_df.divide(volatility.where(volatility > 0))
    if absolute_momentum_lookback is not None and absolute_momentum_lookback <= 0:
        raise ValueError("absolute_momentum_lookback must be positive")
    if (breadth_momentum_lookback is None) != (minimum_positive_breadth is None):
        raise ValueError("breadth lookback and threshold must be provided together")
    if breadth_momentum_lookback is not None:
        if breadth_momentum_lookback <= 0:
            raise ValueError("breadth_momentum_lookback must be positive")
        if (isinstance(minimum_positive_breadth, bool)
                or not isinstance(minimum_positive_breadth, int)
                or not 1 <= minimum_positive_breadth <= len(close_df.columns)):
            raise ValueError("minimum_positive_breadth must fit the universe")
    if (market_regime is None) != (market_regime_lookback is None):
        raise ValueError("market regime series and lookback must be provided together")
    regime = None
    if market_regime is not None:
        if market_regime_lookback <= 0:
            raise ValueError("market_regime_lookback must be positive")
        regime = pd.Series(market_regime, copy=True)
        regime.index = pd.to_datetime(regime.index)
        regime = regime.sort_index().reindex(close_df.index)
        if regime.isna().any():
            raise ValueError("market regime series must cover all trading dates")
    if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer")
    if top_n > len(close_df.columns):
        raise ValueError("top_n must not exceed the universe size")
    start_index = max(
        lookback_1m, lookback_3m, lookback_6m,
        absolute_momentum_lookback or 0,
        score_volatility_lookback or 0,
        breadth_momentum_lookback or 0,
        market_regime_lookback or 0,
    )
    if len(close_df) <= start_index:
        raise ValueError(f"insufficient data: need {start_index + 1}, got {len(close_df)}")

    portfolio = Portfolio(initial_cash, cost_model)
    equity_curve, holding_history, rebalance_logs = [], [], []
    pending_rebalance = None
    for i in range(start_index, len(close_df)):
        today, close_prices, open_prices = close_df.index[i], close_df.iloc[i], open_df.iloc[i]
        scores = score_df.iloc[i]
        if pending_rebalance is not None:
            target_weights = pending_rebalance["target_weights"]
            current_symbols = set(portfolio.holdings)
            target_symbols = set(target_weights)
            if top_n > 1 or current_symbols != target_symbols:
                portfolio.rebalance(
                    target_weights, open_prices, index=len(equity_curve), date=today,
                    signal_date=pending_rebalance["signal_date"],
                    score=pending_rebalance["winner_score"],
                )
            pending_rebalance = None
        if (i - start_index) % rebalance_interval == 0:
            ranked = scores.dropna().sort_values(ascending=False)
            selected_winners = list(ranked.index[:top_n])
            winner_score = ranked.iloc[0] if not ranked.empty else float("nan")
            target_weights = {}
            absolute_momenta = {}
            if absolute_momentum_lookback is not None:
                for symbol in selected_winners:
                    absolute_momenta[symbol] = (
                        close_prices[symbol]
                        / close_df.iloc[i - absolute_momentum_lookback][symbol]
                        - 1
                    )
            for symbol in selected_winners:
                if (absolute_momentum_lookback is None
                        or absolute_momenta[symbol] > 0):
                    target_weights[symbol] = 1.0 / top_n
            positive_breadth = None
            breadth_gate = False
            if breadth_momentum_lookback is not None:
                breadth_returns = (
                    close_prices / close_df.iloc[i - breadth_momentum_lookback] - 1
                )
                positive_breadth = int((breadth_returns > 0).sum())
                breadth_gate = positive_breadth < minimum_positive_breadth
            market_regime_momentum = None
            market_regime_gate = False
            if regime is not None:
                market_regime_momentum = (
                    regime.iloc[i] / regime.iloc[i - market_regime_lookback] - 1
                )
                market_regime_gate = market_regime_momentum <= 0
            if breadth_gate or market_regime_gate:
                target_weights = {}
            risk_off = (
                len(target_weights) < len(selected_winners)
                or breadth_gate or market_regime_gate
            )
            current_symbols = set(portfolio.holdings)
            execution_date = close_df.index[i + 1] if i + 1 < len(close_df) else None
            selected_winner = selected_winners[0] if selected_winners else None
            target_winner = (
                selected_winner if top_n == 1 and selected_winner in target_weights
                else None
            )
            absolute_momentum = absolute_momenta.get(selected_winner)
            rebalance_logs.append({
                "index": len(equity_curve), "date": today,
                "execution_date": execution_date, "winner": selected_winner,
                "target_winner": target_winner,
                "selected_winners": selected_winners,
                "target_weights": dict(target_weights),
                "absolute_momentum": absolute_momentum,
                "absolute_momenta": absolute_momenta,
                "risk_off": risk_off,
                "positive_breadth": positive_breadth,
                "breadth_gate": breadth_gate,
                "market_regime_momentum": market_regime_momentum,
                "market_regime_gate": market_regime_gate,
                "winner_score": winner_score,
                "holding": next(iter(portfolio.holdings), None),
                "holdings": sorted(current_symbols),
                "changed": current_symbols != set(target_weights),
                "scores": scores.to_dict(),
            })
            if not pd.isna(winner_score) and execution_date is not None:
                pending_rebalance = {
                    "target_weights": target_weights,
                    "selected_winners": selected_winners,
                    "winner_score": winner_score,
                    "signal_date": today,
                }
        equity_curve.append(portfolio.equity(close_prices))
        holdings = tuple(sorted(portfolio.holdings))
        holding_history.append(
            next(iter(portfolio.holdings), None) if top_n == 1 else holdings
        )

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
