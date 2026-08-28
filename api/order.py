import requests

BASE_URL = "https://openapi.tossinvest.com"


def buy_stock(
    access_token,
    account_seq,
    symbol,
    quantity,
    price=None
):
    """
    주식 매수 함수

    시장가 매수:
        buy_stock(token, 1, "005930", 1)

    지정가 매수:
        buy_stock(token, 1, "005930", 1, 82000)
    """

    url = f"{BASE_URL}/api/v1/orders"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": str(account_seq),
        "Content-Type": "application/json"
    }

    # 시장가 매수
    if price is None:
        body = {
            "symbol": symbol,
            "side": "BUY",
            "orderType": "MARKET",
            "quantity": str(quantity)
        }

    # 지정가 매수
    else:
        body = {
            "symbol": symbol,
            "side": "BUY",
            "orderType": "LIMIT",
            "quantity": str(quantity),
            "price": str(price)
        }

    print("\n===== 매수 주문 =====")
    print(body)

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    print("상태 코드:", response.status_code)

    try:
        result = response.json()
        print(result)
        return result

    except Exception:
        print(response.text)
        return None


def sell_stock(
    access_token,
    account_seq,
    symbol,
    quantity,
    price=None
):
    """
    주식 매도 함수

    시장가 매도:
        sell_stock(token, 1, "005930", 1)

    지정가 매도:
        sell_stock(token, 1, "005930", 1, 82000)
    """

    url = f"{BASE_URL}/api/v1/orders"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": str(account_seq),
        "Content-Type": "application/json"
    }

    # 시장가 매도
    if price is None:
        body = {
            "symbol": symbol,
            "side": "SELL",
            "orderType": "MARKET",
            "quantity": str(quantity)
        }

    # 지정가 매도
    else:
        body = {
            "symbol": symbol,
            "side": "SELL",
            "orderType": "LIMIT",
            "quantity": str(quantity),
            "price": str(price)
        }

    print("\n===== 매도 주문 =====")
    print(body)

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    print("상태 코드:", response.status_code)

    try:
        result = response.json()
        print(result)
        return result

    except Exception:
        print(response.text)
        return None

def get_order_status(
    access_token,
    account_seq,
    order_id
):
    """
    주문 상세 조회

    return:
        dict 또는 None
    """

    url = f"{BASE_URL}/api/v1/orders/{order_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": str(account_seq)
    }

    response = requests.get(
        url,
        headers=headers
    )

    print("\n===== 주문 조회 =====")
    print("상태 코드:", response.status_code)

    try:
        result = response.json()
        print(result)
        return result

    except Exception:
        print(response.text)
        return None
        
def is_order_filled(order_status):

    if not order_status:
        return False

    if "result" not in order_status:
        return False

    status = order_status["result"]["status"]

    return status == "FILLED"