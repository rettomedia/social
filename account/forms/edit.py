from django import forms
from core.models import CustomUser

class EditProfile(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','bio','avatar')