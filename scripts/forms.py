from django import forms
from scripts.models import Script


class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['title','category','subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True
        self.fields['subject'].required = True