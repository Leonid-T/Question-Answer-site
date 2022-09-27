from django.urls import path

from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.test, name='signup'),
    path('question/<int:pk>', views.question_view, name='question'),
    path('ask/', views.question_add, name='ask'),
    path('popular/', views.PopularView.as_view(), name='popular'),
    path('new/', views.NewView.as_view(), name='new'),
]
