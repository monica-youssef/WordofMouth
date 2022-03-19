from django.contrib import admin
from django.urls import include, path
from wordofmouth.views import index

urlpatterns = [
    path('', index, name="index"),
    path('wordofmouth/', include('wordofmouth.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    # path('', include('main.urls')),
]