from django.test import TestCase
from django.test.client import RequestFactory
from wordofmouth.models import Recipe
from . import views
from django.contrib.auth.models import User
# Create your tests here.



class TrivialTests2(TestCase):
    def test_trivial2(self):
        self.assertEqual(1, 1)

class recipeTestCase(TestCase):
    def test_model_recipe_create(self):
        my_user = User.objects.create(username='TestUser')
        recipe = Recipe.objects.create(title = "Gourmet Waffles", text = "Waffles", added_by = my_user)
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.title, "Gourmet Waffles")
        self.assertEqual(recipe.text, "Waffles")

class responseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_response_index(self):
        request = self.factory.get('wordofmouth/index/')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_response_homeview(self):
        request = self.factory.get('wordofmouth/')
        response = views.homeview(request)
        self.assertEqual(response.status_code, 200)

    def test_response_detail(self):
        request = self.factory.get('wordofmouth/recipe/1/')
        response = views.detail(request)
        print(response)
        self.assertEqual(response.status_code, 200)

class recipeIDTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.my_user = User.objects.create(username = 'TestUser')
    def test_5recipes(self):
        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Waffles', 'text': 'Waffles'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe1 = Recipe.objects.get(pk = 1)
        self.assertEqual(recipe1.id, 1)
        self.assertEqual(recipe1.title, "Gourmet Waffles")
        self.assertEqual(recipe1.text, "Waffles")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Pancakes', 'text': 'Pancakes'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe2 = Recipe.objects.get(pk = 2)
        self.assertEqual(recipe2.id, 2)
        self.assertEqual(recipe2.title, "Gourmet Pancakes")
        self.assertEqual(recipe2.text, "Pancakes")
        self.assertEqual(recipe2.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet French Toast', 'text': 'French Toast'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe3 = Recipe.objects.get(pk = 3)
        self.assertEqual(recipe3.id, 3)
        self.assertEqual(recipe3.title, "Gourmet French Toast")
        self.assertEqual(recipe3.text, "French Toast")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Scrambled Eggs', 'text': 'Scrambled Eggs'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe4 = Recipe.objects.get(pk = 4)
        self.assertEqual(recipe4.id, 4)
        self.assertEqual(recipe4.title, "Gourmet Scrambled Eggs")
        self.assertEqual(recipe4.text, "Scrambled Eggs")
        self.assertEqual(recipe1.added_by.username, "TestUser")

        request = self.factory.post('wordofmouth/create_recipe/', {'title': 'Gourmet Bacon', 'text': 'Bacon'})
        request.user = self.my_user
        views.create_recipe(request)
        recipe5 = Recipe.objects.get(pk = 5)
        self.assertEqual(recipe5.id, 5)
        self.assertEqual(recipe5.title, "Gourmet Bacon")
        self.assertEqual(recipe5.text, "Bacon")
        self.assertEqual(recipe1.added_by.username, "TestUser")
