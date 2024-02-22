from django import forms
from network.models import CustomUser


class ProfileForm(forms.ModelForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('avatar','username','email','bio','location')