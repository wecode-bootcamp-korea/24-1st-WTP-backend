from django.urls import path, include

from users.views import Login


urlpatterns = [
    path('users', include('users.urls')),
]

