from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Class, site="点菜系统")
admin.site.register(Meal, site="点菜系统")
admin.site.register(Food, site="点菜系统")
admin.site.register(FoodForMeal, site="点菜系统")
admin.site.register(Student, site="点菜系统")
admin.site.register(Comment, site="点菜系统")
admin.site.register(FoodForStudent, site="点菜系统")
