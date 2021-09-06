import json

from django.db.models import Q
from django.views import View
from django.http import JsonResponse

from movies.models import Movie, Rating
from users.models import User


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

#평점매긴 영화리스트가져오기
class RatingView(View):

    def get(self,request,user_id):
        user1 = User.objects.get(id=user_id)

        if not user1 :
            return JsonResponse({"MESSAGE" : "USER_DOES_NOT_EXIST"}, status=404)
            
        ratings = Rating.objects.filter(user__id=user_id).order_by('-id')
        
        rated_movies = [{
            "poster_image" : rating.movie.poster_image,
            "movie_name"   : rating.movie.title ,
            "movie_rating" : rating.rate
        } for rating in ratings]

        return JsonResponse({"RATED_MOVIES" : rated_movies}, status=200)


# #댓글 등록 및 사용자의 댓글 특정 영화 또는 전체 영화에 남긴 댓글 호출 구현            
# class Commment(View):
#     def post(self, request, user):
#         data = json.loads(request.body)
#         Rating.objects.create(user_id=user)

