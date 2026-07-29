from django.db import models
from clients.models import Client
from lawyers.models import Lawyer


class Dossier(models.Model):
    STATUS_CHOICES = [
        ("OUVERT", "Ouvert"),
        ("EN_COURS", "En cours"),
        ("FERME", "Fermé"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="dossiers"
    )

    lawyer = models.ForeignKey(
        Lawyer,
        on_delete=models.CASCADE,
        related_name="dossiers"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OUVERT"
    )

    opening_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title