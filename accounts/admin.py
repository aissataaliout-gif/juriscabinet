from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informations JurisCabinet",
            {
                "fields": (
                    "role",
                    "phone",
                    "profile_picture",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informations JurisCabinet",
            {
                "fields": (
                    "role",
                    "phone",
                    "profile_picture",
                )
            },
        ),
    )