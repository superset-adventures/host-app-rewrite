import requests

SUPERSET_URL = "https://superset.startuptrend.in"
SUPERSET_LOGIN = "/api/v1/security/login"
GUEST_TOK_GENERATE  = "/api/v1/security/guest_token/"
GUEST_TOK_REFRESH   = "/api/v1/security/refresh"

url = SUPERSET_URL + SUPERSET_LOGIN
body = {
    "username": "embeddadmin",
    "password": "abcd1234",
    "provider": "db",
    "refresh": True,
}
response = requests.post(url=url, json=body)
tokens = response.json()
access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]
print("*"*50)
print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")
print("*"*50)

url = SUPERSET_URL + GUEST_TOK_GENERATE
headers = {"Authorization": f'Bearer {access_token}'}
body = {
            "resources": [
                {
                    "id": "10",
                    "type": "dashboard"
                }
            ],
            "rls": [
            ],
            "user": {
                "first_name": "appuser",
                "last_name": "appuser",
                "username": "appuser"
            }
        }
response = requests.post(url=url, json=body, headers=headers)

token = response.json()
print("Guest Token:")
print(token)


