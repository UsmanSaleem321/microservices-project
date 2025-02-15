import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utility import *


class AccountsAPIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token"):
            return None  
        token = auth_header.split(" ")[1]
        user_data = validate_token_with_accounts_api(token)  
        return (user_data, token)


class CartServiceAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if not request.user["is_seller"]:
            return super().authenticate(request)
        service_token = request.headers.get("service_token")
        if not service_token:
            raise AuthenticationFailed("No service token found.")
        if validate_servicet_token(service_token):
            return super().authenticate(request)
        
