import requests
from config.settings import CLIENT_ID, CLIENT_SECRET

TOKEN_URL = "https://openapi.tossinvest.com/oauth2/token"


def get_access_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(
        TOKEN_URL,
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        return response.json()["access_token"]

    print("토큰 발급 실패")
    print("상태코드:", response.status_code)
    print("응답:", response.text)

    return None