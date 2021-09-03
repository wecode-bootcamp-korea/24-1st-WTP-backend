from django.urls  import path

from movies.views import MovieDetailView

urlpatterns = [
    path('/<int:movie_id>', MovieDetailView.as_view())
]