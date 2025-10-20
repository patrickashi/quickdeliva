from django.db import models
from users.models import User

class Order(models.Model):
    REGION_CHOICES = (
        ("Igoli", "Igoli"),
        ("Okuku", "Okuku"),
        ("Abakpa", "Abakpa"),
        ("Abouchiche", "Abouchiche"),
    )
    VEHICLE_CHOICES = (
        ("bike", "Bike (₦1,500)"),
        ("keke", "Keke (₦2,500)"),
        ("van", "Van (schedule a call: 07074423164)"),
        ("truck", "Truck (schedule a call: 07074423164)"),
    )
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    pickup_region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True)
    delivery_region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    package_description = models.TextField()
    preferred_vehicle = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)  # new
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)