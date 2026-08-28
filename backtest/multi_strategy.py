from backtest.engine import run_signal_backtest

from strategy.moving_average import add_moving_average
from strategy.rsi import add_rsi_strategy
from strategy.volatility_breakout import add_volatility_breakout_strategy
from strategy.momentum import add_momentum_strategy


def compare_strategies(df, initial_cash=10000000):
    strategies = {
        "Moving Average": add_moving_average,
        "RSI": add_rsi_strategy,
        "Volatility Breakout": add_volatility_breakout_strategy,
        "Momentum": add_momentum_strategy
    }

    results = []

    for name, strategy_func in strategies.items():
        test_df = df.copy()
        test_df = strategy_func(test_df)

        result = run_signal_backtest(
            test_df,
            initial_cash=initial_cash
        )

        results.append({
            "strategy": name,
            "final_value": result["final_value"],
            "return_pct": result["return_pct"],
            "mdd": result["mdd"],
            "win_rate": result["win_rate"],
            "trades": len(result["trades"])
        })

    return results