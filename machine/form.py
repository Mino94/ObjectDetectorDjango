from django import forms
# from .models import Post

class PostForm(forms.Form):
    image = forms.ImageField()

    