import pandas as pd

def add_momentum_strategy(df, lookback=20):
    df["momentum"] = df["close"] / df["close"].shift(lookback) - 1

    df["buy_signal"] = df["momentum"] > 0
    df["sell_signal"] = df["momentum"] < 0

    return df