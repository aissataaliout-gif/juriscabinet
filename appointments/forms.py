from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "dossier",
            "title",
            "appointment_date",
            "location",
            "notes",
        ]

        widgets = {
            "appointment_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }