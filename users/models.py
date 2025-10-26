from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # ✅ keep username (from AbstractUser)
    email = models.EmailField(unique=True)

    USER_TYPES = (
        ("individual", "Individual"),
        ("business", "E-commerce/SME"),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = "username"     # ✅ Django still uses username internally
    REQUIRED_FIELDS = ["email"]     # ✅ only require email extra
    def __str__(self):
        return f"{self.username} ({self.email})"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} — {self.subject or 'No subject'}"