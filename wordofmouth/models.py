from django.db import models
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

from django.contrib.auth.models import User


# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=200)

    # changed these for forking
    ingredients = models.CharField(max_length=500)
    instructions = models.CharField(max_length=500)
    parent = models.CharField(max_length=500)

    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='author')  # author, changed to cascade
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=200)

    # like feature
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.CharField(choices= LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.recipe)



# https://medium.com/@mohammedabuiriban/how-to-use-google-cloud-storage-with-django-application-ff698f5a740f
class Upload(models.Model):
    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = '/images/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload!")

    def __str__(self):
        return self.title
