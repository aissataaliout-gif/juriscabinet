from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('LAWYER', 'Avocat'),
        ('CLIENT', 'Client'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CLIENT'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"

class ContactMessage(models.Model):
        name = models.CharField(max_length=150)
        email = models.EmailField()
        phone = models.CharField(max_length=20, blank=True)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.name} — {self.created_at.strftime('%d/%m/%Y')}"