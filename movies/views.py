import json

from django.views import View
from django.http import JsonResponse

from movies.models import Movie


class MovieView(View): 
    def get(self,request): 

        country_name = request.GET.get("country")
        genre1       = request.GET.get("genre1")
        genre2       = request.GET.get("genre2")
        rating       = request.GET.get("rating")
        LIMIT        = 25
        OFFSET       = 0

        movies = Movie.objects.all().filter(country__name__isnull = False).order_by('-release_date')
        
        if country_name == "한국":
            movies = Movie.objects.filter(country__name="한국").order_by('-release_date')
        
        if country_name == "외국":
            movies = Movie.objects.exclude(country__name="한국").filter(country__name__isnull = False).distinct().order_by('-release_date')
   
        if genre1 and genre2:
            movies = Movie.objects.filter(genre__name=genre1 and genre2, genre__name__isnull = False).order_by('-release_date').distinct()

        if rating:
            movies =  Movie.objects.order_by('-average_rating').filter(country__name__isnull = False)
        
        movie_list = [{
            "country_name"   : [country.name for country in movie.country.all()], 
            "movie_name"     : movie.title,
            "released_date"  : movie.release_date,
            "average_rating" : movie.average_rating,
            "poster_image"   : movie.poster_image
        } for movie in movies ][OFFSET : LIMIT]

        return JsonResponse({"MOVIE_LIST" : movie_list}, status=200)