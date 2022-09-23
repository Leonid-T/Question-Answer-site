from django.http import HttpResponse
from django.views import generic

from .models import Question, Answer


def test(request):
    return HttpResponse('OK')


class IndexView(generic.ListView):
    template_name = 'index.html'
    paginate_by = 10
    model = Question


class PopularView(generic.ListView):
    template_name = 'popular.html'
    paginate_by = 10
    model = Question

    def get_queryset(self):
        return Question.objects.popular()[:]


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'question.html'
