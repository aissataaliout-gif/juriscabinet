from django import forms
from .models import Lawyer


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = [
            "first_name",
            "last_name",
            "specialization",
            "phone",
            "email",
            "bar_number",
            "photo",
        ]