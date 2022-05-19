import requests
SUPERSET_URL = "https://superset.startuptrend.in"
SUPERSET_LOGIN = "/api/v1/security/login"
GUEST_TOK_GENERATE  = "/api/v1/security/guest_token/"
GUEST_TOK_REFRESH   = "/api/v1/security/refresh"

def get_access_token():
    url = SUPERSET_URL + SUPERSET_LOGIN
    body = {
        "username": "embeddadmin",
        "password": "abcd1234",
        "provider": "db",
        "refresh": True,
    }
    response = requests.post(url=url, json=body)
    tokens = response.json()
    print(tokens)
    return tokens["access_token"], tokens["refresh_token"]
try:
    access_token, refresh_token = get_access_token()
except:
    print("Please change AUTH Type to LDAP")

def refresh_access_token():
    url = SUPERSET_URL + GUEST_TOK_REFRESH
    headers = {"Authorization": f'Bearer {refresh_token}'}
    response = requests.post(url=url, headers=headers)
    token = response.json()
    return token["access_token"]

def get_guest_tokens(body):
    global access_token, refresh_access_token
    url = SUPERSET_URL + GUEST_TOK_GENERATE
    headers = {"Authorization": f'Bearer {access_token}'}
    response = requests.post(url=url, json=body, headers=headers)
    token = response.json()

    if token.get("msg") == "Token has expired":
        access_token, refresh_access_token = get_access_token()
        # refresh_access_token()

    url = SUPERSET_URL + GUEST_TOK_GENERATE
    headers = {"Authorization": f'Bearer {access_token}'}
    response = requests.post(url=url, json=body, headers=headers)
    token = response.json()
    return token

if __name__=="__main__":

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
    guest_tok = get_guest_tokens(body)
    print("Guest token:")
    print(guest_tok)
                    