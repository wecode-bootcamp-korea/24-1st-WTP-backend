from django.urls import path

from movies.views import MovieView, RatingView, CommentView

urlpatterns = [
    path("",MovieView.as_view()),
]