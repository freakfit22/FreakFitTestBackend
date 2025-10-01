from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Customer(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(Group, related_name="customer_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customer_permissions", blank=True)

    def __str__(self):
        return self.username


class UserDetail(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # 👈 new field


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Offer model

class Offer(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount in percentage
    duration = models.IntegerField(default=30, help_text="Duration of the offer in days")  # Default 30 days
    description = models.TextField()
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title