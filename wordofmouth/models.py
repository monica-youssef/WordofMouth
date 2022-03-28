from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=200, default="DEFAULT_IMAGE_URL")

    def __str__(self):
        return self.title