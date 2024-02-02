from django.contrib.auth.forms import UserCreationForm
from core.models import CustomUser


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','password1','password2')