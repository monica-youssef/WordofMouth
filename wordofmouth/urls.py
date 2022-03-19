from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeview, name="homeview"),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('detail', views.detail, name='detail'),
    path('recipe_list', views.RecipeList.as_view(), name='recipe_list'),
]