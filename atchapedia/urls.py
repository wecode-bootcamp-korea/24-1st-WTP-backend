from django.urls import path, include
<<<<<<< HEAD

from users.views import Login


urlpatterns = [
    path('users', include('users.urls')),
    path('details', include('movies.urls')),
    
=======

urlpatterns = [
    path('users', include('users.urls')),
    path("movies", include("movies.urls"))
>>>>>>> main
]

