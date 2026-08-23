from django import forms
from .models import Message
from accounts.models import User


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            "receiver",
            "subject",
            "content",
        ]

        widgets = {
            "receiver": forms.Select(
                attrs={"class": "form-select"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:

            if user.role == "CLIENT":
                self.fields["receiver"].queryset = User.objects.filter(
                    role="LAWYER",
                    is_active=True
                )

            elif user.role == "LAWYER":
                self.fields["receiver"].queryset = User.objects.filter(
                    role="CLIENT",
                    is_active=True
                )

            else:
                self.fields["receiver"].queryset = User.objects.none()