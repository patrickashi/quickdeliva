from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "pickup_address",
        "delivery_address",
        "preferred_vehicle",
        "status",
        "created_at",
    )
    search_fields = ("pickup_address", "delivery_address", "preferred_vehicle", "user__email", "user__username")
    list_filter = ("status", "preferred_vehicle")

admin.site.register(Order, OrderAdmin)