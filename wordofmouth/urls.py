from django.urls import path
from django.urls import include, path

from . import views
from .views import UploadView, LikeView

urlpatterns = [
    path('', views.create_recipe_view, name="create_recipe_view"),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('recipe_list', views.RecipeList.as_view(), name='recipe_list'),
    path('accounts/', include('allauth.urls')),
    path('upload', UploadView.as_view(), name='upload-image'),
    path('like/<int:pk>/', LikeView, name='like_recipe'),
    path('recipe/<int:pk>/edit', views.EditView.as_view(), name='edit'),
    path('user_recipe_list', views.UserRecipeList.as_view(), name='user_recipe_list'),
    path('favorites', views.FavoriteRecipeList.as_view(), name='favorite_recipe_list'),

    #forking
    # path('recipe/<int:pk>/fork', views.ForkView.as_view(), name='fork'),
    path('recipe/<int:pk>/fork', views.fork_recipe_view, name='fork'),

]