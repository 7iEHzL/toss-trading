"https://www.quantconnect.com/strategies/245/Tech-Momentum-Winner-Rotation 기반으로 만들었습니다"
import pandas as pd


def add_cross_sectional_momentum(
    data_dict,
    w1=1.0,
    w3=1.0,
    w6=1.0
):
    """
    data_dict

    {
        "AMD": df,
        "TSLA": df,
        ...
    }
    """

    scores = pd.DataFrame()

    for ticker, df in data_dict.items():

        score = (
            w1 * df["close"].pct_change(21)
            +
            w3 * df["close"].pct_change(63)
            +
            w6 * df["close"].pct_change(126)
        )

        scores[ticker] = score

    winner = scores.idxmax(axis=1)

    return winner, scores