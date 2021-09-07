import json

from django.db.models import Q
from django.views import View
from django.http import JsonResponse

from movies.models import Movie, Rating
from users.models import User
from users.utils import login_decorator


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

class CommentView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:    
            data = json.loads(request.body)
            user = User.objects.filter(id=data["user_id"])
            movie = Movie.objects.filter(id=movie_id)
            
            if not movie.exists():
                return JsonResponse({"MESSAGE" : "MOVIE_DOES_NOT_EXIST"}, status=404)
            
            if not user.exists():
                return JsonResponse({"MESSAGE" : "USER_DOES_NOT_EXIST"}, status=404)
            
            if not Rating.objects.filter(user_id=data["user_id"]).exists():
                return JsonResponse({"MESSAGE" : "ENTER_RATING_FIRST"}, status=404)

            Rating.objects.update(
                user_id    = data["user_id"],
                rate       = Rating.objects.get(user_id=data["user_id"]).rate,
                comment    = data["comment"],
                movie_id = movie_id
            )

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
        }for rating in Rating.objects.filter(movie_id=movie_id)]

        return JsonResponse({"MESSAGE" :comment_list}, status=200)