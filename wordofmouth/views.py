from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import Recipe

def index(request):
    return render(request, 'wordofmouth/index.html', {})


def homeview(request):
    return render(request, 'wordofmouth/wordofmouth.html', {})


def detail(request):
    return render(request, 'detail.html', {})


def create_recipe(request):
    try:
        recipe = Recipe()
        recipe.title = request.POST['title']
        recipe.text = request.POST['text']
        recipe.id = Recipe.objects.all().count() + 1
    except (KeyError, recipe.DoesNotExist):
        return render(request, 'detail.html', {
            'error_message': "You didn't enter a title and text."
        })
    else:
        recipe.save()
        return HttpResponseRedirect('detail')