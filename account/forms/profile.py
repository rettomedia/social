from network.models import CustomUser
from django.contrib.auth.forms import UserChangeForm


class ProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('avatar','username','email','region','bio','location')