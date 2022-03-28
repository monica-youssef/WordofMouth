from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.create_recipe_view, name="create_recipe_view"),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('recipe_list', views.RecipeList.as_view(), name='recipe_list'),
    path('accounts/', include('allauth.urls')),
]