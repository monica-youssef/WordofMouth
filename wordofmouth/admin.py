from django.contrib import admin
from .models import Recipe, Upload, Comment

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Upload)
admin.site.register(Comment)