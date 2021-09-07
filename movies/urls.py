from django.urls import path

from movies.views import MovieView

urlpatterns = [
    path("",MovieView.as_view()),
]