from rest_framework import serializers
from .models import User, Driver
from django.contrib.auth import get_user_model
from .models import ContactMessage

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "verification_code"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "user_type", "phone_number",
                  "gender", "state", "lga", "address", "business_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data["user_type"],
            phone_number=validated_data.get("phone_number"),
            gender=validated_data.get("gender"),
            state=validated_data.get("state"),
            lga=validated_data.get("lga"),
            address=validated_data.get("address"),
            business_name=validated_data.get("business_name"),
        )
        return user


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "created_at"]