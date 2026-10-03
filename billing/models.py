from django.db import models
from dossiers.models import Dossier


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("PAID", "Payée"),
        ("OVERDUE", "Impayée"),
    ]

    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Facture #{self.id} - {self.dossier}"