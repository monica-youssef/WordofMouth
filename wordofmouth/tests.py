from django.test import TestCase
from django.test.client import RequestFactory
from wordofmouth.models import Recipe
from . import views
# Create your tests here.



class TrivialTests2(TestCase):
    def test_trivial2(self):
        self.assertEqual(1, 1)

class recipeTestCase(TestCase):
    def test_model_recipe_create(self):
        recipe = Recipe.objects.create(title = "Gourmet Waffles", text = "Waffles")
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
        request = self.factory.get('wordofmouth/recipe/1')
        response = views.detail(request)
        print(response)
        self.assertEqual(response.status_code, 200)


