from django.db import models
from django.conf import settings


class Lawyer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lawyer_profile",
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    bar_number = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="lawyers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"