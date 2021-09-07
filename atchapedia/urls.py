from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('details', include('movies.urls')),
    path("movies", include("movies.urls")),
]    

