from django.urls import path

from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.test, name='login'),
    path('signup/', views.test, name='signup'),
    path('question/<int:pk>', views.QuestionView.as_view(), name='question'),
    path('ask/', views.test, name='ask'),
    path('popular/', views.PopularView.as_view(), name='popular'),
    path('new/', views.test, name='new'),
]
