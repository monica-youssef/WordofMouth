from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeview, name="homeview"),
    path('wordofmouth/create', views.create, name='create'),
    path('wordofmouth/detail', views.detail, name='detail'),
]