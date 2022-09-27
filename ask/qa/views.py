from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404

from .models import Question
from .forms import AskForm, AnswerForm, LoginForm


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


class NewView(generic.ListView):
    template_name = 'new.html'
    paginate_by = 10
    model = Question

    def get_queryset(self):
        return Question.objects.new()[:]


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'question.html'


def question_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            post = form.save(question)
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()
    return render(request, 'question.html', {
        'question': question,
        'form': form,
    })


def question_add(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
