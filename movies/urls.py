from django.urls import path

from movies.views import MovieView, RatingView

urlpatterns = [
    path("movie",MovieView.as_view()),
    path("user/<int:user_id>",RatingView.as_view())
]