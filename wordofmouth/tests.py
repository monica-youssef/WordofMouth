import django.test
from django.test import TestCase
from django.test.client import RequestFactory
from wordofmouth.models import Recipe
from . import views
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.



class TrivialTests2(TestCase):
    def test_trivial2(self):
        self.assertEqual(1, 1)

class recipeTestCase(TestCase):
    def test_model_recipe_create(self):
        my_user = User.objects.create(username='TestUser')
        recipe = Recipe.objects.create(title = "Gourmet Waffles", ingredients = "Waffles", instructions = "Make waffles", added_by = my_user)
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.title, "Gourmet Waffles")
        self.assertEqual(recipe.ingredients, "Waffles")
        self.assertEqual(recipe.instructions, "Make waffles")

class responseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_response_index(self):
        request = self.factory.get(reverse('index'))
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_response_detail(self):
        request = self.factory.get(reverse('detail', args=[1]))
        response = views.detail(request)
        self.assertEqual(response.status_code, 200)

    def test_response_list(self):
        request = self.factory.get(reverse('recipe_list'))
        response = views.detail(request)
        self.assertEqual(response.status_code, 200)

class recipeIDTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.my_user = User.objects.create(username = 'TestUser')
    def test_5recipes(self):
        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Waffles', 'ingredients': 'Waffles', 'instructions': 'Make waffles'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe1 = Recipe.objects.get(pk = 1)
        self.assertEqual(recipe1.id, 1)
        self.assertEqual(recipe1.title, "Gourmet Waffles")
        self.assertEqual(recipe1.ingredients, "Waffles")
        self.assertEqual(recipe1.instructions, "Make waffles")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Pancakes', 'ingredients': 'Pancakes', 'instructions': 'Make pancakes'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe2 = Recipe.objects.get(pk = 2)
        self.assertEqual(recipe2.id, 2)
        self.assertEqual(recipe2.title, "Gourmet Pancakes")
        self.assertEqual(recipe2.ingredients, "Pancakes")
        self.assertEqual(recipe2.instructions, "Make pancakes")
        self.assertEqual(recipe2.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet French Toast', 'ingredients': 'French Toast', 'instructions': 'Make french toast, but gourmet'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe3 = Recipe.objects.get(pk = 3)
        self.assertEqual(recipe3.id, 3)
        self.assertEqual(recipe3.title, "Gourmet French Toast")
        self.assertEqual(recipe3.ingredients, "French Toast")
        self.assertEqual(recipe3.instructions, "Make french toast, but gourmet")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Scrambled Eggs', 'ingredients': 'Scrambled Eggs', 'instructions': 'Make scrambled eggs'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe4 = Recipe.objects.get(pk = 4)
        self.assertEqual(recipe4.id, 4)
        self.assertEqual(recipe4.title, "Gourmet Scrambled Eggs")
        self.assertEqual(recipe4.ingredients, "Scrambled Eggs")
        self.assertEqual(recipe4.instructions, "Make scrambled eggs")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Bacon', 'ingredients': 'Bacon', 'instructions': 'Make bacon'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe5 = Recipe.objects.get(pk = 5)
        self.assertEqual(recipe5.id, 5)
        self.assertEqual(recipe5.title, "Gourmet Bacon")
        self.assertEqual(recipe5.ingredients, "Bacon")
        self.assertEqual(recipe5.instructions, "Make bacon")
        self.assertEqual(recipe1.added_by.username, "TestUser")


class LikeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.my_user = User.objects.create(username = 'TestUser')
        self.request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Waffles', 'ingredients': 'Waffles',
                                                                   'instructions': 'Make waffles'})
        self.request.user = self.my_user

        views.create_recipe(self.request)
        self.recipe = Recipe.objects.get(pk = 1)
    def test_myLikeTest(self):

        request = self.factory.post('wordofmouth/recipe/1', {'recipe_id': self.recipe.id})
        request.user = self.my_user
        views.LikeView(request, self.recipe.id)
        recipe = Recipe.objects.get(pk = 1)
        self.assertEqual(recipe.total_likes(), 1) #Test to like
        views.LikeView(request, self.recipe.id)
        self.assertEqual(recipe.total_likes(), 0) #Test to unlike
