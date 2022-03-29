from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    added_by = models.ForeignKey(User ,null=True, blank=True, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.title

