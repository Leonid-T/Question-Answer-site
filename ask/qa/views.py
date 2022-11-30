from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from .models import Question, Answer, LikeDislike
from .forms import AskForm, AnswerForm, SignupForm, AuthForm
from .serializer import serialize_answers, serialize_questions


class IndexView(View):
    sort_method = {
        'popular': lambda user: Question.objects.popular(),
        'new': lambda user: Question.objects.new(),
        'my_questions': lambda user: Question.objects.my_questions(user),
    }

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            page = request.GET.get('page')
            sort_option = request.GET.get('sort_option')
            questions = self.sort_method[sort_option](request.user)
            paginate_by = 10
            paginator = Paginator(questions, paginate_by)
            page_obj = paginator.get_page(page)
            content = serialize_questions(page_obj, request.user)
            return JsonResponse(content, status=200)
        else:
            return render(request, 'index.html')


class QuestionView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = AnswerForm()
        is_like_dislike = question.votes.is_like_dislike(request.user, question.id)
        is_like = 'active' if is_like_dislike == 1 else ''
        is_dislike = 'active' if is_like_dislike == -1 else ''
        return render(request, 'question.html', {
            'question': question,
            'rating': question.votes.rating(),
            'form': form,
            'url_like': reverse('qa:like_question', args=[question.id]),
            'url_dislike': reverse('qa:dislike_question', args=[question.id]),
            'is_like': is_like,
            'is_dislike': is_dislike,
        })

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated:
                content = form.save(question, user)
                return JsonResponse(content, status=200)
        return JsonResponse({'error': 'Validation error'}, status=400)


class QuestionAdd(View):
    def get(self, request):
        form = AskForm()
        return render(request, 'ask.html', {'form': form})

    def post(self, request):
        form = AskForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                question = Question.objects.create(**form.cleaned_data, author=request.user)
                return HttpResponseRedirect(reverse('qa:question', args=(question.pk, )))
            else:
                form.add_error('text', 'Оставлять вопросы могут только авторизованные пользователи')
        return render(request, 'ask.html', {'form': form})


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
                return JsonResponse({'url': reverse('qa:index')}, status=200)
        return JsonResponse({'error': form.errors}, status=400)


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return JsonResponse({'url': reverse('qa:index')}, status=200)
        form.add_error('password', 'Неправильное имя пользователя или пароль')
        return JsonResponse({'error': form.errors}, status=400)


class SearchView(View):
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            results = ''
            query_search = request.GET.get('search')
            if query_search:
                results = Question.objects.search(query_search)
            paginate_by = 10
            paginator = Paginator(results, paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            content = serialize_questions(page_obj, request.user)
            return JsonResponse(content, status=200)
        else:
            return render(request, 'search.html')


class AnswerDelete(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                Answer.objects.get(
                    question=request.POST.get('question_id'),
                    author=user,
                    id=request.POST.get('answer_id')
                ).delete()
                return JsonResponse({}, status=200)
            except (KeyError, Answer.DoesNotExist):
                return JsonResponse({'error': 'DoesNotExist'}, status=400)
        return JsonResponse({'error': 'Is not authenticated'}, status=400)


class QuestionDelete(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                Question.objects.get(author=user, id=request.POST.get('id')).delete()
                return JsonResponse({}, status=200)
            except (KeyError, Question.DoesNotExist):
                return JsonResponse({'error': 'DoesNotExist'}, status=400)
        return JsonResponse({'error': 'Is not authenticated'}, status=400)


class LoadAnswers(View):
    sort_method = {
        'new': lambda pk: get_object_or_404(Question, pk=pk).answers_new(),
        'popular': lambda pk: get_object_or_404(Question, pk=pk).answers_popular(),
    }

    def get(self, request, pk):
        sort_option = request.GET.get('sort_option')
        paginate_by = 10
        answers = self.sort_method[sort_option](pk)
        paginator = Paginator(answers, paginate_by)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        content = serialize_answers(page_obj, request.user)
        return JsonResponse(content, status=200)


class ContactsView(View):
    def get(self, request):
        return render(request, 'contacts.html')


class VoteView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        user = request.user
        if user.is_authenticated:
            obj = get_object_or_404(self.model, pk=pk)
            result = LikeDislike.objects.get_or_create_or_remove(obj, user, self.vote_type)
            rating = obj.update_rating()
            return JsonResponse({
                'id': obj.id,
                'result': result,
                'rating': rating,
            }, status=200)
        else:
            return JsonResponse({'error': 'Is not authenticated'}, status=400)
