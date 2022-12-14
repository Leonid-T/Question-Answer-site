from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Answer
from .serializer import serialize_new_answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=225, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'title',
    }))
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'text',
    }))


class AnswerForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
    }))

    def save(self, question, user):
        text = self.cleaned_data.get('text')
        answer = Answer.objects.create(text=text, question=question, author=user)
        content = serialize_new_answer(answer, user)
        return content


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password'
    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'repeat_password'
    }))

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с данным именем уже существует')
        if password != repeat_password:
            self.add_error('password', '')
            self.add_error('repeat_password', 'Пароли не совпадают')
        if len(password) < 8:
            self.add_error('password', '')
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
        'id': 'username',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password'
    }))

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователя с данным именем не существует')
