import requests

from config.settings import ENABLE_REAL_ORDER

BASE_URL = "https://openapi.tossinvest.com"


class LiveOrderSafetyError(RuntimeError):
    pass


def _require_live_order_permission(live_order_confirmed):
    if ENABLE_REAL_ORDER is not True:
        raise LiveOrderSafetyError("Live trading이 비활성화되어 있습니다.")

    if live_order_confirmed is not True:
        raise LiveOrderSafetyError(
            "해당 주문에 대한 명시적 사용자 확인이 필요합니다."
        )


def buy_stock(
    access_token,
    account_seq,
    symbol,
    quantity,
    price=None,
    *,
    live_order_confirmed=False
):
    """
    주식 매수 함수

    시장가 매수:
        buy_stock(token, 1, "005930", 1, live_order_confirmed=True)

    지정가 매수:
        buy_stock(token, 1, "005930", 1, 82000, live_order_confirmed=True)
    """

    _require_live_order_permission(live_order_confirmed)

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
    price=None,
    *,
    live_order_confirmed=False
):
    """
    주식 매도 함수

    시장가 매도:
        sell_stock(token, 1, "005930", 1, live_order_confirmed=True)

    지정가 매도:
        sell_stock(token, 1, "005930", 1, 82000, live_order_confirmed=True)
    """

    _require_live_order_permission(live_order_confirmed)

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
