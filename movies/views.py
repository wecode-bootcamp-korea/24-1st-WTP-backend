import json

from django.db.models import Q
from django.views import View
from django.http import JsonResponse

from movies.models import Movie


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

            title          = movie.title
            release_date   = movie.release_date
            poster_image   = movie.poster_image
            trailer        = movie.trailer
            description    = movie.description

            image_url = [image.image_url for image in movie.image_set.all()]

            participants = []
            movie_participants = MovieParticipant.objects.filter(movie = movie_id)
            for movie_participant in movie_participants:
                participants.append(
                    {
                        'name' : movie_participant.participant.name,
                        'role' : movie_participant.role,
                        'image' : movie_participant.participant.image_url
                    }
                )

            rating_users  = [rating.user for rating in movie.rating_set.all()]
            rates         = [rating.rate for rating in movie.rating_set.all()]

            average_rating = sum(rates)/len(rating_users)

            movie_details = {
                'title'          : title,
                'release_date'   : release_date,
                'genre'          : [genre.name for genre in movie.genre.all()],
                'country'        : [country.name for country in movie.country.all()],
                'poster_image'   : poster_image,
                'trailer'        : trailer,
                'image_url'      : image_url,
                'description'    : description,
                'participants'   : participants,
                'average_rating' : average_rating,
                'rating_users'   : len(rating_users),
            }

            return JsonResponse({'movie_info': movie_details}, status = 200)

        except KeyError:
            JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
=======
