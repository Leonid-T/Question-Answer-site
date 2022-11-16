from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('question/<int:pk>', views.QuestionView.as_view(), name='question'),
    path('ask/', views.QuestionAdd.as_view(), name='ask'),
    path('popular/', views.PopularView.as_view(), name='popular'),
    path('new/', views.NewView.as_view(), name='new'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('search', views.SearchView.as_view(), name='search'),
]
