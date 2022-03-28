from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Recipe

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
        recipe.image_url = "hello world"

    except (KeyError, recipe.DoesNotExist):
        return render(request, 'wordofmouth/recipe_list.html', {
            'error_message': "You didn't enter a title and text."
        })
    else:
        recipe.save()
        return HttpResponseRedirect('recipe_list')