from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name = 'liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # everytime author is deleted the post they create is also deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()

like_choices = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.CharField(choices= like_choices, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)