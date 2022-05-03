from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .forms import CommentForm
from django.views import generic
from django.views import View
from django.middleware.csrf import get_token
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .models import Recipe, UserRating
from .models import Upload
from .models import Comment
from django.shortcuts import redirect
import re

from taggit.models import Tag

def index(request):
    all_recipes = Recipe.objects.all()
    random_recipes = Recipe.objects.order_by('?')[:3]
    context = {'all_recipes' : all_recipes, 'featured_recipes' : random_recipes}
    return render(request, 'index.html', context)


def create_recipe_view(request):
    common_tags = list(Recipe.r_tags.most_common()[:5])
    context = {'common_tags' : common_tags }
    return render(request, 'wordofmouth/create_recipe_view.html', context)


def detail(request):
    return render(request, 'wordofmouth/recipe_list.html', {})

def parse(tags):
    tags = tags.split(",")

    for i in range(len(tags)):
        tags[i] = tags[i].strip().lower()

    return tags

# https://stackoverflow.com/questions/63759451/how-to-check-that-a-comma-separated-string-in-python-contains-only-single-commas
def tags_valid(tags):
    pattern = re.compile(r"^(\w+)(,\s*\w+)*$")

    if pattern.match(tags) == None:
        return False
    else:
        return True


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

        rating = 0.0

        print("self.request.user.id: ", self.request.user.id)

        if not self.request.user.is_anonymous and post_id.ratings.filter(user=self.request.user).exists():
            rating = post_id.ratings.filter(user=self.request.user).first().rating

        context["rated"] = rating != 0.0
        context["rating"] = rating
        context["liked"] = liked
        context["total_likes"] = total_likes
        context["average_rating"] = post_id.average_rating()
        return context


def get_avg_rating(r):
    return r.average_rating() or -1.0

class RecipeList(generic.ListView):
    template_name = 'wordofmouth/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        recipes = Recipe.objects.all()
        
        if self.request.GET.get('query'):
            tags = parse(self.request.GET.get('query'))
            recipes_from_search = recipes.filter(title__icontains=self.request.GET.get('query'))
            recipes_from_tag = recipes.filter(r_tags__name__in=tags)
            combined = recipes_from_search | recipes_from_tag
            recipes = list(set(combined))
        elif self.request.GET.get('s'):
            recipes = recipes.filter(servings__exact=self.request.GET.get('s'))

        if self.request.GET.get('tag'):
            tags = parse(self.request.GET.get('tag'))
            recipes = recipes.filter(r_tags__name__in=tags)
        elif self.request.GET.get('a-z') == 'True':
            recipes = recipes.order_by('title')
        elif self.request.GET.get('by-rating') == 'True':
            recipes = sorted(recipes, key=lambda r: get_avg_rating(r), reverse=True)
        elif self.request.GET.get('pt') == 'True':
            recipes = sorted(recipes, key=lambda r: r.prep_time_minutes_conversion + r.cook_time_minutes_conversion, reverse=True)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class UserRecipeList(generic.ListView):
    template_name = 'wordofmouth/user_recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


def create_recipe(request):
    try:
        errors = []

        print("------request.post: ", request.POST)

        if (request.POST['title'] == ""):
            errors.append("1")
        if (request.POST['ingredients'] == ""):
            errors.append("2")
        if (request.POST['instructions'] == ""):
            errors.append("3")
        if (request.FILES['image'] == None):
            errors.append("4")

        r_tags = request.POST['r_tags']
        if (len(r_tags) > 0):
            if (not tags_valid(r_tags)):
                errors.append("5")
        
        if (request.POST['prep-time'] == "" or request.POST['cook-time'] == ""):
            errors.append("times-blank")
        else:
            if (not request.POST['prep-time'] or not request.POST['cook-time'].isdigit()):
                errors.append("times-invalid")
        
        if (len(errors) > 0): 
            raise KeyError

        timestamp = str(datetime.now()).replace(":", "").replace("-", "").replace(".", "")
        end_of_url = (request.user.username + str(timestamp) + '.jpeg').replace(" ", "")
        image_url = 'https://storage.cloud.google.com/a10-word-of-mouth/images/' + end_of_url
        image = request.FILES['image']

        public_uri = Upload.upload_image(image, end_of_url)

        if (public_uri == None):
            errors.append("4")
            raise KeyError
        
        recipe = Recipe.objects.create()
        recipe.title = request.POST['title']
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']
        recipe.image_url = image_url
        recipe.added_by = request.user

        recipe.prep_time = request.POST['prep-time']
        recipe.prep_time_metric = request.POST['prep-time-metric']
        
        recipe.cook_time = request.POST['cook-time']
        recipe.cook_time_metric = request.POST['cook-time-metric']
        
        recipe.servings = request.POST['servings']

        if (len(r_tags) > 0):
            for tag in parse(r_tags):
                recipe.r_tags.add(tag.strip().lower())

        recipe.prep_time_minutes_conversion = recipe.prep_time if recipe.prep_time_metric == "minutes" else (recipe.prep_time * 60)
        recipe.cook_time_minutes_conversion = recipe.cook_time if recipe.cook_time_metric == "minutes" else (recipe.cook_time * 60)
        
    except (KeyError):
        common_tags = list(Recipe.r_tags.most_common()[:5])
        entered_values = {
            'title': request.POST['title'],
            'ingredients': request.POST['ingredients'],
            'instructions': request.POST['instructions'],
            'prep_time': request.POST['prep-time'],
            'prep_time_metric': request.POST['prep-time-metric'],
            'cook_time': request.POST['cook-time'],
            'cook_time_metric': request.POST['cook-time-metric'],
            'servings': request.POST['servings'],
            'r_tags': request.POST['r_tags']
        }
        return render(request, 'wordofmouth/create_recipe_view.html', {
            'errors': errors,
            'common_tags': common_tags, 
            'entered_values': entered_values,
        })
    else:
        recipe.save()
        return HttpResponseRedirect('recipe_list')


# https://medium.com/@mohammedabuiriban/how-to-use-google-cloud-storage-with-django-application-ff698f5a740f
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "add_comment.html"
    success_url = reverse_lazy('recipe_list')
    def form_valid(self, form):
        form.instance.recipe_id = self.kwargs['pk']
        return super().form_valid(form)



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


def RateView(request, recipe_id):
    recipe = Recipe.objects.get(pk = recipe_id)

    rating = request.POST.get('rating')
    
    print("you clicked " + str(rating))
    userRating = UserRating()
    userRating.user = request.user
    userRating.rating = rating
    userRating.save()

    recipe.ratings.add(userRating)

    return HttpResponseRedirect(reverse('detail', args=[str(recipe_id)]))


def edit_recipe(request, pk):
    print("HELLOOOO WORLD")
    try:
        recipe = Recipe.objects.get(pk=pk)
        errors = []

        if (request.POST['updated_title'] == ""):
            errors.append("1")
        if (request.POST['updated_ingredients'] == ""):
            errors.append("2")
        if (request.POST['updated_instructions'] == ""):
            errors.append("3")
        if (request.POST['updated_prep-time'] == "" or request.POST['updated_cook-time'] == ""):
            errors.append("times-blank")
        
        r_tags = request.POST['updated_r_tags']
        if (len(r_tags) > 0):
            if (not tags_valid(r_tags)):
                errors.append("5")

        if (len(errors) > 0): 
            raise KeyError
        print("hello world we are here")
        #todo: FIX
        # if (request.FILES['updated_image'] == None):
        #     print("image not uploaded")
        # else:
        #     print("image uploaded")

        recipe.title = request.POST['updated_title']
        recipe.ingredients = request.POST['updated_ingredients']
        recipe.instructions = request.POST['updated_instructions']
        recipe.prep_time = request.POST['updated_prep-time']
        recipe.cook_time = request.POST['updated_cook-time']
        recipe.servings = request.POST['updated_servings']
        recipe.prep_time_metric = request.POST['updated_prep-time-metric']
        recipe.cook_time_metric = request.POST['updated_cook-time-metric']

        recipe.prep_time_minutes_conversion = recipe.prep_time if recipe.prep_time_metric == "minutes" else (recipe.prep_time * 60)
        recipe.cook_time_minutes_conversion = recipe.cook_time if recipe.cook_time_metric == "minutes" else (recipe.cook_time * 60)
        
    except (KeyError):
        print("error: " + str(errors))
        return render(request, 'wordofmouth/recipe_update_view.html', {
            'errors': errors,
            'recipe': recipe
        })
    else:
        recipe.save()
        return HttpResponseRedirect(reverse('detail', args=[str(pk)]))


def edit_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    context = { 'recipe': recipe }
    return render(request, 'wordofmouth/recipe_update_view.html', context)


class FavoriteRecipeList(generic.ListView):
    template_name = 'wordofmouth/favorite_recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        queryset = []
        for object in Recipe.objects.all():
            if object.likes.filter(id=self.request.user.id).exists():
                queryset.append(object)

        return queryset

# forking!


def fork_recipe_view(request, pk):
    original = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    copy = original
    copy.parent = original.pk
    copy.pk = None
    copy.title = "Fork of " + original.title
    copy.added_by = request.user
    copy.save()
    return HttpResponseRedirect(reverse('detail', args=[str(copy.pk)]))


class ForkRecipeList(generic.ListView):
    template_name = 'wordofmouth/fork_recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        queryset = []
        for thing in Recipe.objects.all():
            if thing.parent != 'new food' and thing.parent != '':
                if int(thing.parent) == int(self.kwargs.get('pk')):
                    queryset.append(thing)
        return queryset

def deleteItem(request, recipe_id):
    recipe = Recipe.objects.get(pk = recipe_id)
    recipe.delete()
    return redirect('user_recipe_list')
