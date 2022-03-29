from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views import View
from django.middleware.csrf import get_token

from django.conf import settings
from .models import Recipe
from .models import Upload

def index(request):
    return render(request, 'index.html', {})


def create_recipe_view(request):
    return render(request, 'wordofmouth/create_recipe_view.html', {})


def detail(request):
    return render(request, 'wordofmouth/recipe_list.html', {})


class RecipeList(generic.ListView):
    template_name = 'wordofmouth/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'wordofmouth/detail.html'


class RecipeList(generic.ListView):
    template_name = 'wordofmouth/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


def create_recipe(request):
    try:
        recipe = Recipe()
        recipe.title = request.POST['title']
        recipe.text = request.POST['text']
        recipe.image_url = 'https://storage.cloud.google.com/a10-word-of-mouth/images/' + request.user.username + str(Recipe.objects.all().count() + 1) + '.jpeg'

        recipe.added_by = request.user
        recipe.id = Recipe.objects.all().count() + 1
    except (KeyError, recipe.DoesNotExist):
        return render(request, 'wordofmouth/recipe_list.html', {
            'error_message': "You didn't enter a title and text."
        })
    else:
        recipe.save()
        return HttpResponseRedirect('upload')


class UploadView(View):
    def get(self, request):
            html = """
                <form method="post" enctype="multipart/form-data">
                <input type='text' style='display:none;' value='%s' name='csrfmiddlewaretoken'/>
                <input type="file" name="image" accept="image/*">
                <button type="submit">Upload Image</button>
                </form>
            """ % (get_token(request))
            return HttpResponse(html)
    def post(self, request):
            image = request.FILES['image']
            # recipe = request.recipe
            public_uri = Upload.upload_image(image, request.user.username + str(Recipe.objects.all().count()) + '.jpeg')
            return HttpResponseRedirect('recipe_list')