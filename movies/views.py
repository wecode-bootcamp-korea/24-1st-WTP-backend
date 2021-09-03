import json

from django.views import View
from django.http import JsonResponse, request

from movies.models import Movie

class MovieView(View): 
    def get(self,request): 

        country_name = request.GET.get("country")
        LIMIT        = int(request.GET.get("limit"))
        OFFSET       = int(request.GET.get("offset"))
        movie_list   = []

        if not country_name == "한국" and not country_name == "외국":
            return JsonResponse({"MESSAGE" : "COUNTRY_DOSE_NOT_EXIST"}, status=400)

        if country_name == "한국":
            movies = Movie.objects.filter(country__name="한국").order_by('-id')
        
        elif country_name == "외국":
            movies = Movie.objects.all().exclude(country__name="한국").order_by('-id')
            
        for i in range(OFFSET, LIMIT):
            movie_list.append({
                "country_name"   : movies[i].country.name, 
                "movie_name"     : movies[i].title,
                "released_date"  : movies[i].release_date,
                "average_rating" : movies[i].average_rating,
                "poster_image"   : movies[i].poster_image
            })
            
        return JsonResponse({"MOVIE_LIST" : movie_list}, status=200)