import jwt
import datetime
import requests
from django.conf import settings
from .utility import validate_token_with_accounts_api
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

class AccountsAPIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token"):
            return None  
        token = auth_header.split(" ")[1]
        user_data = validate_token_with_accounts_api(token)  
        return (user_data, token)



