import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime

sercret_key = "skaakd@jafhakjf432hiufh324"

def validate_token_with_accounts_api(token):
    ACCOUNTS_API_URL = "http://127.0.0.1:8000/token_verify/"  
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(ACCOUNTS_API_URL, headers=headers)
    if response.status_code != 200:
        raise AuthenticationFailed("Invalid or expired token.")
    return response.json() 

def generate_service_token():
    payload = {
        "service": "order-service",
        "iat": datetime.datetime.now(datetime.timezone.utc),  # Issued at
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),  # Expiry time
    }
    
    service_token = jwt.encode(payload, sercret_key, algorithm="HS256")
    return service_token

