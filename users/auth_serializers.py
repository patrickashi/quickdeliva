from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login = attrs.get("username")   # we’ll still receive it under the "username" field
        password = attrs.get("password")
        user = None

        if login and password:
            # Try login by username
            user = authenticate(username=login, password=password)

            # Try login by email
            if user is None and "@" in login:
                try:
                    user_obj = User.objects.get(email__iexact=login)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data = super().validate({"username": user.username, "password": password})
        data["email"] = user.email
        return data