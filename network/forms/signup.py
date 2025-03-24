from django.contrib.auth.forms import UserCreationForm
from network.models import CustomUser
from django import forms
import re
from django_recaptcha.fields import ReCaptchaField

class SignupForm(UserCreationForm):
    agree = forms.BooleanField(required=False)
    captcha = ReCaptchaField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','captcha')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain English letters, numbers and underscores.")
        return username
