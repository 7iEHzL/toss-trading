from backtest.accounting import build_backtest_result
from backtest.portfolio import Portfolio


def run_signal_backtest(df, initial_cash=10000000, cost_model=None, benchmark=None):
    required = {"date", "open", "close", "buy_signal", "sell_signal"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("backtest data must not be empty")

    portfolio = Portfolio(initial_cash, cost_model)
    equity_curve = []
    for i in range(len(df)):
        today = df.iloc[i]
        if i > 0:
            signal = df.iloc[i - 1]
            metadata = {
                "index": len(equity_curve),
                "date": today["date"],
                "signal_date": signal["date"],
            }
            if signal["buy_signal"] and portfolio.quantity("ASSET") == 0:
                quantity = portfolio.cost_model.max_affordable_quantity(
                    portfolio.cash, float(today["open"])
                )
                portfolio.buy("ASSET", quantity, today["open"], **metadata)
            elif signal["sell_signal"] and portfolio.quantity("ASSET") > 0:
                portfolio.liquidate("ASSET", today["open"], **metadata)
        equity_curve.append(portfolio.equity({"ASSET": today["close"]}))

    return build_backtest_result(
        portfolio, equity_curve, df["date"], initial_cash,
        {"ASSET": df.iloc[-1]["close"]}, benchmark,
    )
