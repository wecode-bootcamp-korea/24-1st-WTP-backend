import json

from django.views import View
from django.http import JsonResponse, request

from movies.models import Country, Movie, Genre

class MovieView(View): 
    def get(self,request): 

        country_name = request.GET.get("country")
        genre1       = request.GET.get("genre1")
        genre2       = request.GET.get("genre2")
        rating       = request.GET.get("rating")
        LIMIT        = 25
        OFFSET       = 0

        if not country_name and not genre1 and not rating:
            return JsonResponse({"MESSAGE" : "PARAMETER_DOSE_NOT_EXIST"}, status=400)
        
        movies = Movie.objects.filter(country__name="한국").order_by('-id')[OFFSET : LIMIT]
        
        if country_name == "외국":
            movies = Movie.objects.exclude(country__name="한국").filter(country__name__isnull = False).distinct().order_by('-id')[OFFSET : LIMIT]
   
        if genre1 or genre2:
            movies = Movie.objects.filter(genre__name=genre1 or genre2, genre__name__isnull = False).order_by('-id').distinct()[OFFSET : LIMIT]

        if rating:
            movies =  Movie.objects.order_by('-average_rating').filter(country__name__isnull = False)[OFFSET : LIMIT]
        
        movie_list = [{
            "country_name"   : [country.name for country in movie.country.all()], 
            "movie_name"     : movie.title,
            "released_date"  : movie.release_date,
            "average_rating" : movie.average_rating,
            "poster_image"   : movie.poster_image
        } for movie in movies ]

        return JsonResponse({"MOVIE_LIST" : movie_list}, status=200)