import requests

BASE_URL = "https://openapi.tossinvest.com"


def get_current_price(access_token, symbol):

    url = f"{BASE_URL}/api/v1/prices"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "symbols": symbol
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print("현재가 조회 실패")
        print(response.text)
        return None

    data = response.json()

    return int(data["result"][0]["lastPrice"])