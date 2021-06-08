from django.urls import path

from . import views

app_name = 'activity'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:activity_id>', views.detail, name='detail')
]
