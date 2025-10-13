from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Driver, User

class CustomUserAdmin(BaseUserAdmin):
    # Show these fields in admin list view
    list_display = ("id", "username", "email", "user_type", "is_verified", "is_staff")
    # Filters in the right side panel
    list_filter = ("is_verified", "is_staff", "user_type")
    # Fields to search for
    search_fields = ("email", "username", "phone_number", "business_name")

    fieldsets = BaseUserAdmin.fieldsets + (  # add custom fields to existing ones
        ("Additional Info", {
            "fields": (
                "user_type",
                "phone_number",
                "gender",
                "state",
                "lga",
                "address",
                "business_name",
                "is_verified",
                "verification_code",
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Driver)  # Register Driver model as well