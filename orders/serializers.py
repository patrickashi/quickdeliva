from rest_framework import serializers
from .models import Order
from .models import OrderLocation


class OrderSerializer(serializers.ModelSerializer):
    # Make user read-only → it will be set in `perform_create`
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user", "status", "created_at")  
        # ✅ these are managed by backend, not expected in frontend requests


class OrderStatsSerializer(serializers.Serializer):
    month = serializers.CharField()
    total = serializers.IntegerField()

class OrderLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLocation
        fields = ["latitude", "longitude", "updated_at"]