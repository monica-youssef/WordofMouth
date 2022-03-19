from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import Recipe

def index(request):
    return HttpResponse("Hello, world. You're at the word of mouth index.")


def homeview(request):
    return render(request, 'wordofmouth.html', {})


def detail(request):
    return render(request, 'detail.html', {})


def create(request):
    try:
        recipe = Recipe()
        recipe.title = request.POST['title']
        recipe.text = request.POST['text']
        recipe.id = Recipe.objects.all().count() + 1
    except (KeyError, recipe.DoesNotExist):
        return render(request, 'wordofmouth/dtail.html', {
            'error_message': "You didn't enter a title and text."
        })
    else:
        recipe.save()
        return HttpResponseRedirect(reverse('wordofmouth:detail'))