from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from clients.models import Client


class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = "CLIENT"
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            Client.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone or "",
                gender="M",
                date_of_birth="2000-01-01",
                address="À compléter",
                profession="À compléter",
                identity_number="À compléter",
            )

        return user