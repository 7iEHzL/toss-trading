import pandas as pd


def rank_series(series, higher_is_better=True):
    if higher_is_better:
        return series.rank(pct=True)
    return series.rank(pct=True, ascending=False)


def run_multifactor_rotation_backtest_v2(
    data_dict,
    fundamental_data,
    initial_cash=10000000,
    momentum_lookback=63,
    absolute_momentum_lookback=126,
    volume_lookback=20,
    ma_window=200,
    rebalance_interval=5,
    top_n=2,
    weight_momentum=0.40,
    weight_quality=0.25,
    weight_value=0.25,
    weight_volume=0.10
):
    close_df = pd.DataFrame()
    volume_df = pd.DataFrame()

    for ticker, df in data_dict.items():
        temp = df.copy()
        temp["date"] = pd.to_datetime(temp["date"])
        temp = temp.sort_values("date")
        temp = temp.set_index("date")

        close_df[ticker] = temp["close"]
        volume_df[ticker] = temp["volume"]

    close_df = close_df.dropna()
    volume_df = volume_df.loc[close_df.index]

    tickers = list(close_df.columns)

    ma_df = close_df.rolling(ma_window).mean()

    cash = initial_cash
    holdings = {}
    trades = []
    equity_curve = []
    rebalance_logs = []

    start_index = max(
        momentum_lookback,
        absolute_momentum_lookback,
        volume_lookback * 2,
        ma_window
    )

    if len(close_df) <= start_index:
        raise ValueError(
            f"데이터가 부족합니다. 필요 최소 데이터: {start_index + 1}, 현재 데이터: {len(close_df)}"
        )

    for i in range(start_index, len(close_df)):
        today = close_df.index[i]
        prices = close_df.iloc[i]

        current_equity = cash
        for ticker, qty in holdings.items():
            current_equity += qty * prices[ticker]

        is_rebalance_day = (i - start_index) % rebalance_interval == 0

        if is_rebalance_day:
            momentum = close_df.iloc[i] / close_df.iloc[i - momentum_lookback] - 1
            absolute_momentum = close_df.iloc[i] / close_df.iloc[i - absolute_momentum_lookback] - 1

            recent_volume = volume_df.iloc[i - volume_lookback:i].mean()
            past_volume = volume_df.iloc[i - volume_lookback * 2:i - volume_lookback].mean()
            volume_raw = recent_volume / past_volume - 1

            roe = pd.Series({
                ticker: fundamental_data[ticker]["roe"]
                for ticker in tickers
            })

            pbr = pd.Series({
                ticker: fundamental_data[ticker]["pbr"]
                for ticker in tickers
            })

            momentum_rank = rank_series(momentum, True)
            volume_rank = rank_series(volume_raw, True)
            quality_rank = rank_series(roe, True)
            value_rank = rank_series(pbr, False)

            total_score = (
                weight_momentum * momentum_rank
                + weight_quality * quality_rank
                + weight_value * value_rank
                + weight_volume * volume_rank
            )

            candidates = []

            rejected = {}

            for ticker in tickers:
                reasons = []

                if absolute_momentum[ticker] <= 0:
                    reasons.append("absolute_momentum<=0")

                if prices[ticker] <= ma_df.iloc[i][ticker]:
                    reasons.append("close<=MA200")

                if len(reasons) == 0:
                    candidates.append(ticker)
                else:
                    rejected[ticker] = reasons

            if len(candidates) > 0:
                winners = (
                    total_score.loc[candidates]
                    .sort_values(ascending=False)
                    .head(top_n)
                    .index
                    .tolist()
                )
            else:
                winners = []

            rebalance_logs.append({
                "index": len(equity_curve),
                "date": today,
                "winners": winners,
                "candidates": candidates,
                "rejected": rejected,
                "scores": total_score.to_dict()
            })

            for ticker, qty in list(holdings.items()):
                if ticker not in winners:
                    sell_price = prices[ticker]
                    cash += qty * sell_price

                    trades.append({
                        "index": len(equity_curve),
                        "date": today,
                        "action": "SELL",
                        "symbol": ticker,
                        "price": sell_price,
                        "qty": qty,
                        "cash": cash
                    })

                    del holdings[ticker]

            if len(winners) > 0:
                total_equity = cash
                for ticker, qty in holdings.items():
                    total_equity += qty * prices[ticker]

                target_value = total_equity / len(winners)

                for ticker in winners:
                    current_value = 0
                    if ticker in holdings:
                        current_value = holdings[ticker] * prices[ticker]

                    diff_value = target_value - current_value

                    if diff_value > prices[ticker]:
                        buy_price = prices[ticker]
                        qty = diff_value // buy_price

                        if qty > 0:
                            cost = qty * buy_price
                            cash -= cost
                            holdings[ticker] = holdings.get(ticker, 0) + qty

                            trades.append({
                                "index": len(equity_curve),
                                "date": today,
                                "action": "BUY",
                                "symbol": ticker,
                                "price": buy_price,
                                "qty": qty,
                                "cash": cash,
                                "score": total_score[ticker]
                            })

        current_equity = cash
        for ticker, qty in holdings.items():
            current_equity += qty * prices[ticker]

        equity_curve.append(current_equity)

    final_value = equity_curve[-1]
    return_pct = (final_value - initial_cash) / initial_cash * 100

    peak = equity_curve[0]
    mdd = 0
    mdd_peak_index = 0
    mdd_trough_index = 0
    temp_peak_index = 0

    for i, equity in enumerate(equity_curve):
        if equity > peak:
            peak = equity
            temp_peak_index = i

        drawdown = (equity - peak) / peak

        if drawdown < mdd:
            mdd = drawdown
            mdd_peak_index = temp_peak_index
            mdd_trough_index = i

    wins = 0
    losses = 0

    buys = {}

    for trade in trades:
        symbol = trade["symbol"]

        if trade["action"] == "BUY":
            buys[symbol] = trade

        elif trade["action"] == "SELL" and symbol in buys:
            buy = buys[symbol]

            if trade["price"] > buy["price"]:
                wins += 1
            else:
                losses += 1

            del buys[symbol]

    total_closed = wins + losses
    win_rate = wins / total_closed * 100 if total_closed > 0 else 0

    return {
        "initial_cash": initial_cash,
        "final_value": final_value,
        "return_pct": return_pct,
        "mdd": mdd * 100,
        "mdd_peak_index": mdd_peak_index,
        "mdd_trough_index": mdd_trough_index,
        "trades": trades,
        "equity_curve": equity_curve,
        "rebalance_logs": rebalance_logs,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
    }