from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=225, required=True)
    text = forms.CharField(widget=forms.Textarea, required=True)
    author = None

    def save(self):
        question = Question(**self.cleaned_data)
        question.author = self.author
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
    }))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'InputUsername',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'InputPassword'
    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'ReInputPassword'
    }))

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с данным именем уже существует')
        if password != repeat_password:
            self.add_error('repeat_password', 'Пароли не совпадают')
        if len(password) < 8:
            self.add_error('repeat_password', 'Пароль должен быть не менее 8 символов')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        user = authenticate(**self.cleaned_data)
        return user


class AuthForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'InputUsername',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'InputPassword'
    }))

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователя с данным именем не существует')
