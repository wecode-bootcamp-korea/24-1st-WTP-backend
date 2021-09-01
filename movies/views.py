import json

from django.views import View
from django.http import JsonResponse, request

from movies.models import *
from users.models import User


class GetKoreanMovieList(View):
    def get(self,request):
        data = json.loads(request.body)
        
        movie_information = []
        korea              = Country.objects.get(name="한국")
        korea_movies       = korea.movie_set.all()
           
        for korea_movie in korea_movies:
            movie_information.append({
                "movie_name"     : korea_movie.title,
                "released_date"  : korea_movie.release_date,
                "average_rating" : korea_movie.average_rating,
                "poster_image"   : korea_movie.poster_image
            })

        result = movie_information[:data["movies_counts"]]    

        return JsonResponse({"RESULT" : result}, status=200)