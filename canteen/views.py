from django.shortcuts import render, redirect
from . import models


# Create your views here.
def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('has_login'):
            return func(request, *args, **kwargs)
        else:
            try:
                if models.Student.objects.get(stu_id=request.COOKIES.get('stu_id')
                                              ).password == request.COOKIES.get('password'):
                    request.session['has_login'] = True
                    return func(request, *args, **kwargs)
            except models.Student.DoesNotExist:
                return redirect('canteen:login')
            return redirect('canteen:login')

    return wrapper


def index(request):
    return render(request, 'canteen/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'canteen/login.html')
    elif request.method == 'POST':
        if request.session.get('has_login'):
            return redirect('canteen:welcome')
        stu_id = request.POST.get('stu_id')
        password = request.POST.get('password')
        try:
            if models.Student.objects.get(stu_id=stu_id).password == password:
                response = redirect('canteen:welcome')
                response.set_cookie('stu_id', stu_id, max_age=60 * 60 * 24 * 7)
                response.set_cookie('password', password, max_age=60 * 60 * 24 * 7)
                request.session['has_login'] = True
                return response
        except models.Student.DoesNotExist:
            return render(request, 'canteen/login.html', {'error_msg': '编号或密码错误，请重新输入！'})
        return render(request, 'canteen/login.html', {'error_msg': '编号或密码错误，请重新输入！'})


@login_required
def class_login(request):
    pass


@login_required
def welcome(request):
    student = models.Student.objects.get(stu_id=request.COOKIES.get('stu_id'))
    latest_meal = models.FoodForMeal.objects.filter(meal__gt=student.last_order).order_by('meal')
    return render(request, 'canteen/welcome.html',
                  {'student': student, 'food_list': latest_meal})


@login_required
def logout(request):
    request.session.flush()
    response = redirect('canteen:login')
    response.delete_cookie('stu_id')
    response.delete_cookie('password')
    return response
