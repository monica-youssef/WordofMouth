from django.test import TestCase
from wordofmouth.models import Recipe
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
