import pandas as pd

def add_moving_average(df):
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()

    df["buy_signal"] = (
        (df["ma5"].shift(1) <= df["ma20"].shift(1)) &
        (df["ma5"] > df["ma20"])
    )

    df["sell_signal"] = (
        (df["ma5"].shift(1) >= df["ma20"].shift(1)) &
        (df["ma5"] < df["ma20"])
    )

    return df