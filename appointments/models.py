from django.db import models
from dossiers.models import Dossier


class Appointment(models.Model):
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    title = models.CharField(max_length=200)
    appointment_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title