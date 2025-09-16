from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Offer

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone_number", "address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "phone_number", "password1", "password2"),
        }),
    )

    list_display = ("username", "email", "phone_number", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'discount', 'duration', 'is_active', 'link')
    list_filter = ('is_active', 'duration')
    search_fields = ('title', 'description', 'link')
