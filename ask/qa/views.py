from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Question
from .forms import AskForm, AnswerForm, SignupForm, AuthForm


class IndexView(generic.ListView):
    template_name = 'index.html'
    paginate_by = 10
    model = Question

    def get_queryset(self):
        return Question.objects.all()


class PopularView(generic.ListView):
    template_name = 'popular.html'
    paginate_by = 10
    model = Question

    def get_queryset(self):
        return Question.objects.popular()


class NewView(generic.ListView):
    template_name = 'new.html'
    paginate_by = 10
    model = Question

    def get_queryset(self):
        return Question.objects.new()


class QuestionView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = AnswerForm()
        return render(request, 'question.html', {
            'question': question,
            'form': form,
        })

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        if request.user.is_authenticated:
            form = AnswerForm(request.POST)
            form.question = question
            form.author = request.user
            if form.is_valid():
                post = form.save()
                return HttpResponseRedirect(reverse('qa:question', args=(post.question_id, )))
            else:
                return HttpResponseRedirect(reverse('qa:login'))


def question_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AskForm(request.POST)
            form.author = request.user
            if form.is_valid():
                post = form.save()
                return HttpResponseRedirect(reverse('qa:question', args=(post.pk, )))
        else:
            form = AskForm()
        return render(request, 'ask.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('qa:login'))


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('qa:index'))
        return render(request, 'signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = reverse('qa:index')
            else:
                url = reverse('qa:signup')
            return HttpResponseRedirect(url)


class SearchView(View):
    def get(self, request):
        results = ''
        query_search = request.GET.get('search')
        if query_search:
            results = Question.objects.filter(Q(title__icontains=query_search) | Q(text__icontains=query_search))
        paginate_by = 10
        paginator = Paginator(results, paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'search.html', {
            'count': paginator.count,
            'page_obj': page_obj,
        })
