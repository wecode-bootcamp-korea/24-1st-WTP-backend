import json
from json.decoder import JSONDecodeError
from django.core.exceptions import ValidationError

from django.http.response import JsonResponse
from movies.models        import *
from typing               import KeysView
from users.views          import Login
from decimal              import *

from django.views         import View
from django.db.models     import Avg 

from users.utils          import login_decorator


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

    # movie = {
            #     "name"              : movie.name, 
            #     "user_rate"         : rate,
            #     "avg_rate"          : new_rate,
            #     "total_rated_people": total_rate_point + 1,
            # }


    # def get(self, request, movie_id):
    #     '''
    #     반환할 필드: 특정 영화, 평균 별점 및 참여자 수, 이미지들, 비슷한 장르 영화들(이름, 이미지) 
        
    #     '''
        
    #     movie = Movie.objects.get(id=movie_id)

    #     # movie & grade join
    #     get_related = Movie.objects.select_related('grade').get(id=movie_id)
                
    #     rate = Rating.objects.filter(movie_id=1)
        
    #     # 별점 평균
    #     avg_rate = rate.aggregate(avg_rate=Avg('rate'))
        
    #     # 별점 부여한 인원
    #     total_rated = rate.count()
        
    #     # 영화의 이미지들 가져오기
        # mv_images = Movie.objects.filter(id=movie_id).prefetch_related('image_set')[0].image_set.values('image_url')
        
    #     image_list = []
        
    #     for image in mv_images:
    #         image_list.append(image)
        
        
    #     items = {
    #         "movie_title"   : get_related.title,
    #         "released"      : movie.release_date,
    #         "description"   : movie.description,
    #         "running_time"  : movie.running_time,
    #         "average_rating": avg_rate['avg_rate'],
    #         "grade"         : get_related.grade.grade,
    #         "total_rated"   : total_rated,
    #         "poster"        : movie.poster_image,
    #         "images"        : image_list,
    #     }
        

    #     return JsonResponse({
    #         "message": "Success",
    #         "items": items
    #     }, status=200)

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