# models.py
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
        ("bike", "Bike"),
        ("keke", "Keke"),
        ("van", "Van"),
        ("truck", "Truck"),
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
    delivery_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def compute_base_price(self):
        # regional base prices (bike baseline)
        base_matrix = {
            "Igoli": {"Igoli": 1500, "Okuku": 2000, "Abakpa": 2000, "Abouchiche": 2500},
            "Okuku": {"Igoli": 2000, "Okuku": 1500, "Abakpa": 3000, "Abouchiche": 3500},
            "Abakpa": {"Igoli": 2000, "Okuku": 3000, "Abakpa": 1500, "Abouchiche": 3500},
            "Abouchiche": {"Igoli": 2500, "Okuku": 3500, "Abakpa": 3500, "Abouchiche": 1500},
        }
        return base_matrix.get(self.pickup_region, {}).get(self.delivery_region, 0)

    def save(self, *args, **kwargs):
        base_price = self.compute_base_price()
        vehicle_multipliers = {"bike": 1.0, "keke": 1.5, "van": 4.0, "truck": 8.0}
        multiplier = vehicle_multipliers.get(self.preferred_vehicle, 1)
        self.delivery_amount = base_price * multiplier
        super().save(*args, **kwargs)


class OrderLocation(models.Model):
    order = models.OneToOneField(
        "Order",  # ✅ use string reference to the class name
        on_delete=models.CASCADE,
        related_name="location",
        null=True
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

# reviews
class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} – {self.rating}★"