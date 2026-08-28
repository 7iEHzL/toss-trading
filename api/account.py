import requests

BASE_URL = "https://openapi.tossinvest.com"


def get_accounts(access_token):
    url = f"{BASE_URL}/api/v1/accounts"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    print("상태 코드:", response.status_code)

    data = response.json()

    print(data)

    return data