from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from .models import Question, Answer, LikeDislike

app_name = 'qa'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('question/<int:pk>', views.QuestionView.as_view(), name='question'),
    path('ask', views.QuestionAdd.as_view(), name='ask'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('search', views.SearchView.as_view(), name='search'),
    path('delete_answer', views.AnswerDelete.as_view(), name='delete_answer'),
    path('delete_question', views.QuestionDelete.as_view(), name='delete_question'),
    path('question/<int:pk>/load_answers', views.LoadAnswers.as_view(), name='load_answers'),
    path('contacts', views.ContactsView.as_view(), name='contacts'),
    path('question/<int:pk>/like', views.VoteView.as_view(model=Question, vote_type=LikeDislike.LIKE),
         name='like_question'),
    path('question/<int:pk>/dislike', views.VoteView.as_view(model=Question, vote_type=LikeDislike.DISLIKE),
         name='dislike_question'),
    path('answer/<int:pk>/like', views.VoteView.as_view(model=Answer, vote_type=LikeDislike.LIKE),
         name='like_answer'),
    path('answer/<int:pk>/dislike', views.VoteView.as_view(model=Answer, vote_type=LikeDislike.DISLIKE),
         name='dislike_answer'),
]
