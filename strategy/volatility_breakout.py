import pandas as pd

def add_volatility_breakout_strategy(df, k=0.5):
    df["range"] = df["high"].shift(1) - df["low"].shift(1)
    df["target_price"] = df["open"] + df["range"] * k

    df["buy_signal"] = df["close"] > df["target_price"]

    # 단순화: 다음 날 종가 매도
    df["sell_signal"] = df["buy_signal"].shift(1).fillna(False).astype(bool)

    return df