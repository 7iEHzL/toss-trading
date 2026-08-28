import requests
import pandas as pd

BASE_URL = "https://openapi.tossinvest.com"


def get_daily_candles(access_token, symbol, count=100):

    url = f"{BASE_URL}/api/v1/candles"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "symbol": symbol,
        "interval": "1d",
        "count": count
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print(response.text)
        return None

    data = response.json()

    candles = data["result"]["candles"]

    df = pd.DataFrame(candles)

    # 컬럼명 변경
    df.rename(columns={
        "timestamp": "date",
        "openPrice": "open",
        "highPrice": "high",
        "lowPrice": "low",
        "closePrice": "close",
        "volume": "volume"
    }, inplace=True)

    # 자료형 변환
    numeric_cols = ["open", "high", "low", "close", "volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    # 날짜 변환
    df["date"] = pd.to_datetime(df["date"])

    # 과거 → 현재 순 정렬
    df = df.sort_values("date")

    df.reset_index(drop=True, inplace=True)

    return df