from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Recipe


def index(request):
    return render(request, 'index.html', {})


def homeview(request):
    return render(request, 'wordofmouth/wordofmouth.html', {})


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

    def get_context_data(self, *args, **kwargs):
        context= super(DetailView, self).get_context_data()
        post_id = get_object_or_404(Recipe, id=self.kwargs['pk'])
        total_likes = post_id.total_likes()
        context["total_likes"] = total_likes
        return context


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
        recipe.id = Recipe.objects.all().count() + 1
    except (KeyError, recipe.DoesNotExist):
        return render(request, 'wordofmouth/recipe_list.html', {
            'error_message': "You didn't enter a title and text."
        })
    else:
        recipe.save()
        return HttpResponseRedirect('recipe_list')


def LikeView(request, pk):
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    recipe.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))
