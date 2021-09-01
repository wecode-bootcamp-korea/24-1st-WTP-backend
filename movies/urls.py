from django.urls import path

from movies.views import *
#질문 하나의 url안에 여러기능들을 담아야하므로, view들을 하나로 합쳐야하는지?
urlpatterns = [
    path("main/korea_movies",GetKoreanMovieList.as_view())
]


