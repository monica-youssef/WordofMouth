from django.db import models
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title

#https://medium.com/@mohammedabuiriban/how-to-use-google-cloud-storage-with-django-application-ff698f5a740f
class Upload:
    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = '/images/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload!")