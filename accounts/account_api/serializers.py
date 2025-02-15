from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

# Get the custom user model
CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_seller']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'is_seller']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Remove password from validated data
        password = validated_data.pop('password')
        
        # Create the user instance
        user = CustomUser(**validated_data)
        
        # Hash the password
        user.set_password(password)
        user.save()
        
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        data["user"] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})
        return data

