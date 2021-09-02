from django.urls import path

from movies.views import *

urlpatterns = [
    path("movie",MovieView.as_view())
]