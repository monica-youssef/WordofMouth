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


class RecipeList(generic.ListView):
    template_name = 'wordofmouth/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


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
        
        recipe = Recipe()
        recipe.title = request.POST['title']
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']
        recipe.image_url = image_url
        recipe.added_by = request.user
        
    except (KeyError):
        print("-----keyrror: ", errors)
        return render(request, 'wordofmouth/create_recipe_view.html', {
            'errors': errors
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


class EditView(generic.edit.UpdateView):
    model = Recipe
    fields = ['title', 'ingredients', 'instructions']
    template_name_suffix = '_update_view'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.id})


def edit_recipe_view(request):
    return render(request, 'wordofmouth/recipe_update_view.html', {})


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
