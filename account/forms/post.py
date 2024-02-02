from django import forms
from account.models import Post

class Creation(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content')