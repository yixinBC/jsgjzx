from django.urls import path

from . import views

app_name = 'canteen'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('class', views.class_login, name='class'),
    path('welcome', views.welcome, name='welcome')
]
