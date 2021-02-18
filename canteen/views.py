from django.shortcuts import render, redirect
from django.urls import reverse
from . import models


# Create your views here.
def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_login') or (
                models.Student.objects.get(stu_id=request.COOKIES.get('stu_id')
                                           ).password == request.COOKIES.get('password')):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('canteen:login'))
    return wrapper


def index(request):
    return render(request, 'canteen/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'canteen/login.html')
    elif request.method == 'POST':
        pass


def class_login(request):
    pass
