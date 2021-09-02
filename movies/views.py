import json

from django.views import View
from django.http import JsonResponse, request

from movies.models import *
from users.models import User


class MovieView(View): 
    def get(self,request): 

        try:
            country_name = request.GET.get("country")
            limit        = int(request.GET.get("limit",25))
            offset       = int(request.GET.get("offset",0))
            movie_list   = []

            if not country_name == "한국" and not country_name == "외국":
                return JsonResponse({"MESSAGE" : "COUNTRY_DOSE_NOT_EXIST"}, status=400)

            if country_name == "한국":   
                movies = Movie.objects.filter(country__name=country_name).order_by('-id')[offset * limit: (offset+1) * limit]
               
                for movie in movies:
                    movie_list.append({
                        "movie_name"     : movie.title,
                        "released_date"  : movie.release_date,
                        "average_rating" : movie.average_rating,
                        "poster_image"   : movie.poster_image
                    })
                return JsonResponse({"KOREAN_MOVIES" : movie_list}, status=200)
            
            if country_name == "외국":
                countries = Country.objects.all().exclude(name="한국")
                
                for country in countries:
                    movies = Movie.objects.filter(country__name=country.name).order_by('-id')[offset * limit: (offset+1) * limit]
                    
                    for movie in movies:
                        movie_list.append({
                            "country_name"   : country.name,
                            "movie_name"     : movie.title,
                            "released_date"  : movie.release_date,
                            "average_rating" : movie.average_rating,
                            "poster_image"   : movie.poster_image
                        })
                return JsonResponse({"FOREIGN_MOVIES" : movie_list}, status=200)

        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)