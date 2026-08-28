def run_signal_backtest(df, initial_cash=10000000):
    cash = initial_cash
    stock_qty = 0
    trades = []
    equity_curve = []

    for i in range(len(df)):
        today = df.iloc[i]

        if "buy_signal" not in df.columns or "sell_signal" not in df.columns:
            raise ValueError("buy_signal, sell_signal 컬럼이 필요합니다.")

        close_price = today["close"]

        if today["buy_signal"] and stock_qty == 0:
            stock_qty = cash // close_price

            if stock_qty > 0:
                invested = stock_qty * close_price
                cash -= invested

                trades.append({
                    "index": len(equity_curve),
                    "date": today["date"],
                    "action": "BUY",
                    "price": close_price,
                    "qty": stock_qty,
                    "cash": cash
                })

        elif today["sell_signal"] and stock_qty > 0:
            proceeds = stock_qty * close_price
            cash += proceeds

            trades.append({
                "index": len(equity_curve),
                "date": today["date"],
                "action": "SELL",
                "price": close_price,
                "qty": stock_qty,
                "cash": cash
            })

            stock_qty = 0

        equity = cash + stock_qty * close_price
        equity_curve.append(equity)

    final_value = equity_curve[-1]
    return_pct = (final_value - initial_cash) / initial_cash * 100

    peak = equity_curve[0]
    mdd = 0

    for equity in equity_curve:
        if equity > peak:
            peak = equity

        drawdown = (equity - peak) / peak
        if drawdown < mdd:
            mdd = drawdown

    wins = 0
    losses = 0

    for i in range(1, len(trades), 2):
        buy = trades[i - 1]
        sell = trades[i]

        if sell["price"] > buy["price"]:
            wins += 1
        else:
            losses += 1

    total_closed = wins + losses
    win_rate = wins / total_closed * 100 if total_closed > 0 else 0

    return {
        "initial_cash": initial_cash,
        "final_value": final_value,
        "return_pct": return_pct,
        "mdd": mdd * 100,
        "trades": trades,
        "equity_curve": equity_curve,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
    }