from django import forms

from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=225)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = 1
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, question):
        answer = Answer(**self.cleaned_data)
        answer.question = question
        answer.author_id = 1
        answer.save()
        return answer


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
