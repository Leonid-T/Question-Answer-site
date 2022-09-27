from django import forms
from django.contrib.auth.models import User

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
    text = forms.CharField(widget=forms.Textarea, required=True)
    question = None
    author = None

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.question = self.question
        answer.author = self.author
        answer.save()
        return answer


def create_user(form):
    user = User()
    user.username = form.cleaned_data['username']
    user.set_password(form.cleaned_data['password1'])
    user.save()
    return user
