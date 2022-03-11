from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('wordofmouth/', include('wordofmouth.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('googlelogin.urls')),
    path('accounts/', include('allauth.urls')),
    # path('', include('main.urls')),
]