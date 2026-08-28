import requests

BASE_URL = "https://openapi.tossinvest.com"


def get_balance(access_token, account_seq):
    url = f"{BASE_URL}/api/v1/holdings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": str(account_seq)
    }

    response = requests.get(url, headers=headers)

    print("상태 코드:", response.status_code)
    print(response.json())