from django import forms
from univer.models import Post, Kaf, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class KafForm(forms.ModelForm):
    class Meta:
        model = Kaf
        fields = ('course', 'num')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name = forms.CharField(max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)