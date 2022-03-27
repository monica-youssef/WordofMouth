from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    likes = models.ManyToManyField(User, related_name='recipe_posts') #tutorial called it blog_posts

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title