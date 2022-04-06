from django.contrib import admin
from .models import Recipe, Upload

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Upload)