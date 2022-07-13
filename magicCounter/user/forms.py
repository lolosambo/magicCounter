
from django import forms
from django.http import request
from user.models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:

        model = CustomUser
        fields = [
            "date_of_birth",
            "email"
        ]
        labels = {
            "date_of_birth": "Date de naissance",
            "email": "Adresse email",
        }
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            "email": forms.EmailInput(),
        }
