import requests
from rest_framework.exceptions import AuthenticationFailed
import jwt
sercret_key = "skaakd@jafhakjf432hiufh324"


def validate_token_with_accounts_api(token):
     
    ACCOUNTS_API_URL = "http://127.0.0.1:8000/token_verify/"  
    headers = {"Authorization": f"Token {token}"}   
    response = requests.get(ACCOUNTS_API_URL, headers=headers)
    if response.status_code != 200:
        raise AuthenticationFailed("Invalid or expired token.")
    return response.json()

def validate_servicet_token(service_token):
    payload = jwt.decode(service_token, sercret_key, algorithms=["HS256"])
    if payload["service"] != "order-service":
        raise AuthenticationFailed("Invalid service token.")
    return True
    