from django import forms
from .models import SubscribeModel


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = SubscribeModel
        fields = ['email',]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control",
                                            "placeholder": "Введите email"})
        }
        labels = {
            "email": "",
        }
