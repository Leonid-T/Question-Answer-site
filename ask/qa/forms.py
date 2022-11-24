from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import template_localtime
from django.utils.html import escape

from crispy_forms.helper import FormHelper

from .models import Question, Answer


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

    # def __init__(self, *args, **kwargs):
    #     super(AnswerForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_show_labels = False

    def save(self, question, user):
        text = self.cleaned_data.get('text')
        answer = Answer.objects.create(text=text, question=question, author=user)
        content = {
            'text': escape(text),
            'added_at': localize(template_localtime(answer.added_at)),
            'author': escape(user.username),
            'answer_id': answer.id,
            'question_id': answer.question_id,
            'url_delete': reverse('qa:delete_answer'),
            'is_user': True,
        }
        return content


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
            self.add_error('password', '')
            self.add_error('repeat_password', 'Пароли не совпадают')
        if len(password) < 8:
            self.add_error('password', '')
            self.add_error('repeat_password', 'Пароль должен быть не менее 8 символов')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

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

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователя с данным именем не существует')


def serialize_answers(page_obj, user):
    answers = {}
    number = 0
    for answer in page_obj:
        is_user = user.username == answer.author.username
        answers[number] = {
            'text': escape(answer.text),
            'author': escape(answer.author.username),
            'question_id': answer.question_id,
            'added_at': localize(template_localtime(answer.added_at)),
            'answer_id': answer.id,
        }
        if is_user:
            answers[number]['url_delete'] = reverse('qa:delete_answer')
            answers[number]['is_user'] = is_user
        number += 1
    return {'has_page': page_obj.has_next(), 'answers': answers}
