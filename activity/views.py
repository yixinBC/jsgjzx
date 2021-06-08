from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    return render(request, 'activity/index.html', {'activities': Activity.objects.all()})


def detail(request, activity_id):
    return render(request, 'activity/detail.html', {'pictures': Picture.objects.filter(activity__id=activity_id)})
