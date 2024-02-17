from django.contrib.auth.forms import UserCreationForm
from network.models import CustomUser
from django import forms

class SignupForm(UserCreationForm):
    agree = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email','password1','password2')