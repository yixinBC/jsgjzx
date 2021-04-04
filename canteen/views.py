import datetime
import json
import xlwt
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import *


# Create your views here.
def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('has_login'):
            return func(request, *args, **kwargs)
        else:
            try:
                if Student.objects.get(stu_id=request.COOKIES.get('stu_id')
                                       ).password == request.COOKIES.get('password'):
                    request.session['has_login'] = True
                    return func(request, *args, **kwargs)
            except Student.DoesNotExist:
                return redirect('canteen:login')
            return redirect('canteen:login')

    return wrapper


def get_next_menu(meal: Meal):
    if (meal_list := Meal.objects.filter(
            Q(date__gt=meal.date) | (Q(date=meal.date) & Q(index__gt=meal.index)))):
        next_meal = min(meal_list)
        return FoodForMeal.objects.filter(meal=next_meal)
    else:
        return


def index(request):
    return render(request, 'canteen/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'canteen/login.html')
    elif request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        password = request.POST.get('password')
        try:
            if Student.objects.get(stu_id=stu_id).password == password:
                response = redirect('canteen:welcome')
                response.set_cookie('stu_id', stu_id, max_age=60 * 60 * 24 * 7)
                response.set_cookie('password', password, max_age=60 * 60 * 24 * 7)
                request.session['has_login'] = True
                return response
        except Student.DoesNotExist:
            return render(request, 'canteen/login.html', {'error_msg': '编号或密码错误，请重新输入！'})
        return render(request, 'canteen/login.html', {'error_msg': '编号或密码错误，请重新输入！'})


@login_required
def class_login(request):
    pass


@login_required
def welcome(request):
    student = Student.objects.get(stu_id=request.COOKIES.get('stu_id'))
    #
    if student.last_order.date < (today := datetime.date.today()):
        student.last_order = Meal.objects.filter(date__lt=today).last()
        student.save(update_fields=['last_order'])
    #
    # TODO:make the code above a better approach
    return render(request, 'canteen/welcome.html',
                  {'student': student, 'food_list': get_next_menu(student.last_order), 'data': {}})


@require_POST
def askmeal(request):
    if request.content_type == "application/json":
        data = json.loads(request.body.decode())
        if 'student' in data.keys() and 'foodForMeal' in data.keys():
            try:
                student = Student.objects.get(pk=data.get('student'))
                food_for_meal = FoodForMeal.objects.get(pk=data.get('foodForMeal'))
                student.asked_meals.add(food_for_meal)
                student.last_order = food_for_meal.meal
                student.save(update_fields=['last_order'])
                food_for_meal.wanted = F('wanted') + 1
                food_for_meal.save(update_fields=['wanted'])
            except Exception as err:
                return render(request, 'canteen/text.html',
                              {'data': json.dumps({'error_message': str(err), 'success': False})})
            if food_list := get_next_menu(student.last_order):
                meal = food_list[0].meal
                return render(request, 'canteen/text.html',
                              {'food_list': food_list,
                               'data': json.dumps({
                                   'success': True,
                                   'hasContent': True,
                                   'date': str(meal.date),
                                   'description': meal.description,
                                   'meal_pk': meal.pk
                               })})
            else:
                return render(request, 'canteen/text.html',
                              {'food_list': food_list,
                               'data': json.dumps({
                                   'success': True,
                                   'hasContent': False
                               })})
        return render(request, 'canteen/text.html',
                      {'data': json.dumps({'success': False, 'error_message': 'bad_post'})})
    return render(request, 'canteen/text.html',
                  {'data': json.dumps({'success': False, 'error_message': 'bad_post'})})


@require_POST
def nextmeal(request):
    if request.content_type == "application/json":
        data = json.loads(request.body.decode())
        if 'student' in data.keys() and 'meal_pk' in data.keys():
            try:
                student = Student.objects.get(pk=data.get('student'))
                meal = Meal.objects.get(pk=data.get('meal_pk'))
                student.last_order = meal
                student.save(update_fields=['last_order'])
            except Exception as err:
                return render(request, 'canteen/text.html',
                              {'data': json.dumps({'error_message': str(err), 'success': False})})
            if food_list := get_next_menu(meal):
                next_meal = food_list[0].meal
                return render(request, 'canteen/text.html',
                              {'food_list': food_list,
                               'data': json.dumps({
                                   'success': True,
                                   'hasContent': True,
                                   'date': next_meal.date,
                                   'description': next_meal.description,
                                   'meal_pk': next_meal.pk
                               })})
            else:
                return render(request, 'canteen/text.html',
                              {'food_list': food_list,
                               'data': json.dumps({
                                   'success': True,
                                   'hasContent': False
                               })})
        return render(request, 'canteen/text.html',
                      {'data': json.dumps({'success': False, 'error_message': 'bad_post'})})
    return render(request, 'canteen/text.html',
                  {'data': json.dumps({'success': False, 'error_message': 'bad_post'})})


@login_required
def logout(request):
    request.session.flush()
    response = redirect('canteen:login')
    response.delete_cookie('stu_id')
    response.delete_cookie('password')
    return response


def export_excel(request, meal_pk):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=汇总数据.xls'
    wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet('sheet1')
    food_list = FoodForMeal.objects.filter(meal__pk=meal_pk)
    for i in range(len(food_list)):
        sheet.write(0, i, food_list[i].food.name)
        sheet.write(1, i, food_list[i].wanted)
    wb.save(response)
    return response


def result(request):
    meal_list = Meal.objects.all()
    return render(request, 'canteen/result.html', {'meal_list': meal_list})
