from django.db import models
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

from django.contrib.auth.models import User

from taggit.managers import TaggableManager

class UserRating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Recipe(models.Model):
    title = models.CharField(max_length=200)

    # changed these for forking
    ingredients = models.CharField(max_length=500)
    instructions = models.CharField(max_length=500)
    parent = models.CharField(max_length=500)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='author')  # author, changed to cascade
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=200)

    likes = models.ManyToManyField(User, related_name='recipe_posts')  # tutorial called it blog_posts
    ratings = models.ManyToManyField(UserRating, related_name='recipe_ratings')

    prep_time = models.IntegerField(default=0)
    prep_time_metric = models.CharField(max_length=200, default='minutes')
    prep_time_minutes_conversion = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    cook_time_metric = models.CharField(max_length=200, default='minutes')
    cook_time_minutes_conversion = models.IntegerField(default=0)
    servings = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tag, related_name='recipe_tags')
    r_tags = TaggableManager()

    def total_likes(self):
        return self.likes.count()

    def average_rating(self):
        # https://stackoverflow.com/questions/55325723/generate-average-for-ratings-in-django-models-and-return-with-other-model
        return self.ratings.all().aggregate(models.Avg('rating')).get('rating__avg', 0.00)

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.recipe.title, self.name)


# https://medium.com/@mohammedabuiriban/how-to-use-google-cloud-storage-with-django-application-ff698f5a740f
class Upload(models.Model):
    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = 'images/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload!")
            print("exception:", e)

    def __str__(self):
        return self.title
