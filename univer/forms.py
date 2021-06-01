from django import forms
from univer.models import Post, Kaf

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class KafForm(forms.ModelForm):
    class Meta:
        model = Kaf
        fields = ('course', 'num')
