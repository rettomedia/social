from django.contrib.auth.forms import UserCreationForm
from network.models import CustomUser
from django import forms
import re

class SignupForm(UserCreationForm):
    agree = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain English letters, numbers and underscores.")
        return username
