from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "receiver",
            "subject",
            "content",
        ]

        widgets = {
            "subject": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "receiver": forms.Select(
                attrs={"class": "form-select"}
            ),
        }