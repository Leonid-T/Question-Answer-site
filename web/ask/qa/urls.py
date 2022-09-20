from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('login/', views.test, name='login'),
    path('signup/', views.test, name='signup'),
    path('question/123', views.test, name='question'),
    path('ask/', views.test, name='ask'),
    path('popular/', views.test, name='popular'),
    path('new/', views.test, name='new'),
]
