"""
REFERENCES
  Title: Django Google Authentication using django-allauth
  Author: Muhd Rahiman
  Date: 3/14/2022
  URL: https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8

"""

from django.urls import include, path

from . import views
from .views import LikeView, RateView, AddCommentView

urlpatterns = [
    path('', views.create_recipe_view, name="create_recipe_view"),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('recipe_list', views.RecipeList.as_view(), name='recipe_list'),
    path('accounts/', include('allauth.urls')),
    path('user/<int:pk>/', views.UserDetails.as_view(), name='user_details'),
    path('like/<int:pk>/', LikeView, name='like_recipe'),
    path('rate/<recipe_id>/', RateView, name='rate_recipe'),
    path('recipe/<int:pk>/edit', views.edit_recipe_view, name='edit'),
    path('recipe/<int:pk>/edit_recipe', views.edit_recipe, name='edit_recipe'),
    path('user_recipe_list', views.UserRecipeList.as_view(), name='user_recipe_list'),
    path('favorites', views.FavoriteRecipeList.as_view(), name='favorite_recipe_list'),
    path('recipe/<int:pk>/comment', AddCommentView.as_view(), name='add_comment'),
    path('delete_item/<recipe_id>/', views.deleteItem, name='delete'),
    # path('recipe/<int:pk>/fork', views.ForkView.as_view(), name='fork'),
    path('recipe/<int:pk>/fork', views.fork_recipe_view, name='fork'),
    path('recipe/<int:pk>/forklist', views.ForkRecipeList.as_view(), name='fork_recipe_list'),
]


handler404 = views.error_404