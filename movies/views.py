import json

from django.http.response import JsonResponse
from movies.models        import *
from typing               import KeysView
from users.views          import Login
from decimal              import *

from django.views         import View
from django.db.models     import F, Sum, Count, Avg 

from users.utils          import login_decorator


# 영화에 별점 매긴 사람들, 펼점 평균
class RateUpdate(View):
    # @login_decorator
    # def post(self, movie_id, request):
    #     try:
    #         data = json.loads(request.body)
            
    #         rate = data['rate']
            
    #         movie = Movie.objects.get(id=movie_id)
            
    #         # 별점 업데이트
    #         Rating.objects.create(user_id=request.user.id, movie_id=movie_id, rate=rate)
    #         # 명수
    #         total_rate_point = Rating.objects.filter(movie_id=movie_id).count()
            
    #         # 평균 값(이렇게 안하고 aggre 머시기 쓰면 됨)
    #         avg_rate = movie.average_rating
            
    #         new_rate = (float(avg_rate) * total_rate_point + rate) // (total_rate_point + 1)
    #         new_rate = Decimal(round(new_rate, 1))
            
    #         Movie.objects.filter(id=movie_id).select_for_update(average_rate=new_rate)
            
    #         movie = {
    #             "name"              : movie.name, 
    #             "user_rate"         : rate,
    #             "avg_rate"          : new_rate,
    #             "total_rated_people": total_rate_point + 1,
    #         }

    #         return JsonResponse({"movie": movie}, status=200)

    #     except KeyError:
    #         return JsonResponse({"message": "INVALID FORMAT"}, status=400)
        
    def get(self, request, movie_id):
        '''
        반환할 필드: 특정 영화, 평균 별점 및 참여자 수, 이미지들, 비슷한 장르 영화들(이름, 이미지) 
        
        '''
        
        movie = Movie.objects.get(id=movie_id)

        # movie & grade join
        get_related = Movie.objects.select_related('grade').get(id=movie_id)
                
        rate = Rating.objects.filter(movie_id=1)
        
        # 별점 평균
        avg_rate = rate.aggregate(avg_rate=Avg('rate'))
        
        # 별점 부여한 인원
        total_rated = rate.count()
        
        # 영화의 이미지들 가져오기
        mv_images = Movie.objects.filter(id=movie_id).prefetch_related('image_set')[0].image_set.values('image_url')
        
        image_list = []
        
        for image in mv_images:
            image_list.append(image)
        
        
        items = {
            "movie_title"   : get_related.title,
            "released"      : movie.release_date,
            "description"   : movie.description,
            "running_time"  : movie.running_time,
            "average_rating": avg_rate['avg_rate'],
            "grade"         : get_related.grade.grade,
            "total_rated"   : total_rated,
            "poster"        : movie.poster_image,
            "images"        : image_list,
        }
        

        return JsonResponse({
            "message": "Success",
            "items": items
        }, status=200)

# 상세페이지2: 특정 영화의 비슷한 영화 불러오는 API
class RelatedMovie(View):
    def get(self, request, movie_id):
        
        try:
            genres = MovieGenre.objects.filter(movie_id=movie_id)
        
            related = []

            for i in genres:
                mv_list = MovieGenre.objects.filter(genre_id=i.genre_id).exclude(movie_id=movie_id)
                for mv in mv_list:
                    tmp = Movie.objects.get(id=mv.movie_id)
                    
                    related.append({
                        "title": tmp.title,
                        "avg": tmp.average_rating,
                        "poster": tmp.poster_image,    
                    })

            return JsonResponse({
                "message": "SUCCESS",
                "related_movies": related,
            },status=200)
        
        except KeyError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)