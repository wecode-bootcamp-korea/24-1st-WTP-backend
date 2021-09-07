import json
from json.decoder           import JSONDecodeError
from decimal                import *
from django.http            import JsonResponse

from django.views           import View
from django.db.models       import Avg 
from django.core.exceptions import ValidationError

from users.utils            import login_decorator
from movies.models          import Movie, Rating, MovieGenre, MovieParticipant





# 영화에 별점 매긴 사람들, 펼점 평균
class RateUpdate(View):
    @login_decorator
    def post(self, request, movie_id):
        try:
            data = json.loads(request.body)
            
            rate = data['rate']
            
            mv_rate = Rating.objects.filter(movie_id=movie_id)
            
            # 별점 평균
            avg_rate = mv_rate.aggregate(avg_rate=Avg('rate'))
            
            Movie.objects.filter(id=movie_id).update(average_rating=avg_rate['avg_rate'])

            if Rating.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
                Rating.objects.filter(user_id=request.user.id, movie_id=movie_id).update(rate=rate)
            
            else:
                Rating.objects.create(
                    user_id  = request.user.id,
                    movie_id = movie_id,
                    rate     = rate,
                )

            return JsonResponse({"movie": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID FORMAT"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "NO DATA"}, status=400)
        
        except ValidationError:
            return JsonResponse({"message": "TYPE DOESNT MATCH"}, status=400)


# 상세페이지2: 특정 영화의 비슷한 영화 불러오는 API
class RelatedMovie(View):
    def get(self, request):
            
        OFFSET = 0
        LIMIT = 16

        try:
            movie_id = request.GET.get('id', None)
            
            if not movie_id:
                return JsonResponse({"message": "NO QUERY STRING"}, status=201)  
            
            if not MovieGenre.objects.filter(movie_id=movie_id).exists():
                return JsonResponse({"message": "QUERY DOES NOT MATCH"}, status=201)

            genres = MovieGenre.objects.filter(movie_id=movie_id)

            related = []

            for i in genres:
                mv_list = MovieGenre.objects.filter(genre_id=i.genre_id).exclude(movie_id=movie_id)
                
                for mv in mv_list:
                    related.append({
                        "title": mv.movie.title,
                        "avg": mv.movie.average_rating,
                        "poster": mv.movie.poster_image,    
                    })

            # 중복 값 제거
            related_movies = list({rel['title']: rel for rel in related}.values())
            
            return JsonResponse({
                "message": "SUCCESS",
                "related_movies": related_movies[OFFSET:LIMIT],
            },status=200)
        
        except KeyError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)


class MovieDetailView(View):
    def get(self, request, movie_id):
        
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

