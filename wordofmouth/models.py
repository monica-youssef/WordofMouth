from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    liked = models.ManyToManyField(User, default=None, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # everytime author is deleted the post they create is also deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()
