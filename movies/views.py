import json
from json.decoder           import JSONDecodeError
from decimal                import *

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Avg
from django.core.exceptions import ValidationError

from users.utils            import login_decorator
from movies.models          import Movie, MovieParticipant
from movies.models          import Movie, MovieParticipant, Rating, MovieGenre


class MovieView(View): 
    def get(self,request): 
        country_name  = request.GET.get("country")
        genre1        = request.GET.get("genre1")
        genre2        = request.GET.get("genre2")
        rating        = request.GET.get("rating","")
        KOREAN_MOVIE  = "한국"
        FOREIGN_MOVIE = "외국"
        LIMIT         = 25
        OFFSET        = 0

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
            "movie_id"       : movie.id,
            "released_date"  : movie.release_date,
            "average_rating" : movie.average_rating,
            "poster_image"   : movie.poster_image
        } for movie in movies ][OFFSET : LIMIT]

        return JsonResponse({"MOVIE_LIST" : movie_list}, status=200)


class RateView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:
            data = json.loads(request.body)
            
            rate = data['rate']

            Rating.objects.update_or_create(
                user_id  = request.user.id,
                movie_id = movie_id,
                defaults = {'rate' : rate}
            )

            mv_rate  = Rating.objects.filter(movie_id=movie_id)
            avg_rate = mv_rate.aggregate(avg_rate=Avg('rate'))
            
            Movie.objects.filter(id=movie_id).update(average_rating=avg_rate['avg_rate'])

            return JsonResponse({
                "message" : "SUCCESS"
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID FORMAT"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "NO DATA"}, status=400)
        
        except ValidationError:
            return JsonResponse({"message" : "TYPE DOESNT MATCH"}, status=400)
    
    @login_decorator
    def get(self, request, movie_id):
        
        if Rating.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
                rate = Rating.objects.get(user_id=request.user.id, movie_id = movie_id).rate
        else:
            rate = 0.0

        return JsonResponse({"user_rate" : rate}, status=200)


class GenreMovieView(View):
    def get(self, request):  
        OFFSET = 0
        LIMIT  = 16
        q      = Q()

        try:
            movie_id = request.GET.get('id', None)
            
            if not movie_id:
                return JsonResponse({"message" : "NO QUERY STRING"}, status=404)  
            
            if not MovieGenre.objects.filter(movie_id=movie_id).exists():
                return JsonResponse({"message" : "QUERY DOES NOT MATCH"}, status=404)

            genres = MovieGenre.objects.filter(movie_id=movie_id)

            related = []

            for genre in genres:
                q |= Q(genre__id = genre.genre_id)
            
            movie = MovieGenre.objects.select_related('movie').filter(q).exclude(movie_id=movie_id)
            
            related = [{
                "movie_id" : mv.movie.id,
                "title"    : mv.movie.title,
                "avg"      : mv.movie.average_rating,
                "poster"   : mv.movie.poster_image,    
            }for mv in movie]
            
            related_movies = list({rel['title']: rel for rel in related}.values())
            
            return JsonResponse({
                "message" : "SUCCESS",
                "related_movies" : related_movies[OFFSET:LIMIT],
            },status=200)
        
        except KeyError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)


class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            if not Movie.objects.filter(id=movie_id).exists():
                return JsonResponse({'MESSAGE' : 'Movie Not Exists'}, status = 404)

            movie = Movie.objects.get(id=movie_id)

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
                    } for participants in MovieParticipant.objects.filter(movie=movie_id)
                ],
                'description'    : movie.description,
                'rating_users'   : movie.rating_set.count(),
                'average_rating' : round(Rating.objects.filter(movie_id=movie).aggregate(Avg('rate'))['rate__avg'], 1)
            }

            return JsonResponse({'movie_info' : movie_details}, status = 200)

        except KeyError:
            JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)


class CommentView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:    
            data    = json.loads(request.body)
            user_id = request.user.id
            rating  = Rating.objects.get(user_id=user_id,movie_id=movie_id)

            if not rating:
                return JsonResponse({"MESSAGE" : "ENTER_RATING_FIRST"}, status=404)

            rating.comment = (data["comment"])
            rating.save()

            return JsonResponse({"MESSAGE" : "CREATE"}, status=200)
        except ValueError:
                return JsonResponse({"MESSAGE" : "VALUE_ERROR"}, status=404)
        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=404)

    def get(self, request, movie_id):
        comment_list = [{
            "user_name"   : rating.user.name, 
            "comment"     : rating.comment, 
            "user_rating" : rating.rate 
        }for rating in Rating.objects.filter(movie_id=movie_id).order_by('-id')]

        return JsonResponse({"MESSAGE" :comment_list}, status=200)
