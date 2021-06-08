from django.contrib import admin

# Register your models here.
from .models import Activity, Picture
admin.site.register(Activity)
admin.site.register(Picture)
