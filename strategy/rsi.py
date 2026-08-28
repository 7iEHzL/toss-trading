import pandas as pd

def add_rsi_strategy(df, period=14):
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    df["buy_signal"] = df["rsi"] < 30
    df["sell_signal"] = df["rsi"] > 70

    return df