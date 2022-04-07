from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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


class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'wordofmouth/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data()

        post_id = get_object_or_404(Recipe, id=self.kwargs['pk'])
        total_likes = post_id.total_likes()

        liked = False
        if post_id.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["liked"] = liked
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
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']
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

# https://medium.com/@mohammedabuiriban/how-to-use-google-cloud-storage-with-django-application-ff698f5a740f


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


def LikeView(request, pk):
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    liked = False
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        liked = False
    else:
        recipe.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))