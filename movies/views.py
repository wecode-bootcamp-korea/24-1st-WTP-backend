import json

from django.db.models import Q, Avg
from django.views import View
from django.http import JsonResponse

from movies.models import Movie, MovieParticipant, Rating


class MovieView(View): 
    def get(self,request): 
        country_name = request.GET.get("country")
        genre1       = request.GET.get("genre1")
        genre2       = request.GET.get("genre2")
        rating       = request.GET.get("rating","")
        KOREAN_MOVIE = "한국"
        FOREIGN_MOVIE = "외국"
        LIMIT        = 25
        OFFSET       = 0

        q = Q()
        
        if country_name == KOREAN_MOVIE:
            q.add(Q(country__name=KOREAN_MOVIE), q.AND)

        if country_name == FOREIGN_MOVIE:
            q.add(~Q(country__name=KOREAN_MOVIE), q.AND)

        if genre1 or genre2:
            q.add(Q(genre__name=genre1)|Q(genre__name=genre2), q.AND)
        
        movies = Movie.objects.filter(q).order_by('-release_date').distinct()
        
        if rating:
            movies =  Movie.objects.order_by('-average_rating')

        movie_list = [{
            "country_name"   : [country.name for country in movie.country.all()], 
            "movie_name"     : movie.title,
            "released_date"  : movie.release_date,
            "average_rating" : movie.average_rating,
            "poster_image"   : movie.poster_image
        } for movie in movies ][OFFSET : LIMIT]

        return JsonResponse({"MOVIE_LIST" : movie_list}, status=200)

class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            if not Movie.objects.filter(id = movie_id).exists():
                return JsonResponse({'MESSAGE':'Movie Not Exists'}, status = 404)

            movie = Movie.objects.get(id = movie_id)

            movie_details = {
                'title'          : movie.title,
                'release_date'   : movie.release_date,
                'genre'          : [genre.name for genre in movie.genre.all()],
                'country'        : [country.name for country in movie.country.all()],
                'poster_image'   : movie.poster_image,
                'trailer'        : movie.trailer,
                'image_url'      : [image.image_url for image in movie.image_set.all()],
                'participants'   : [
                    {
                        'name'  : participants.participant.name,
                        'role'  : participants.role,
                        'image' : participants.participant.image_url 
                    } for participants in MovieParticipant.objects.filter(movie = movie_id)
                ],
                'description'    : movie.description,
                'rating_users'   : movie.rating_set.count(),
                'average_rating' : round(Rating.objects.filter(movie_id = movie).aggregate(Avg('rate'))['rate__avg'], 1)
            }

            return JsonResponse({'movie_info': movie_details}, status = 200)

        except KeyError:
            JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)