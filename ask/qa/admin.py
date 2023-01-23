from django.contrib import admin

from .models import Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 10


class QuestionAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author']
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
