from django.urls  import path
from django.views import View

from movies.views import *

urlpatterns = [
    path('/movies/<int=movie_id>',)
]