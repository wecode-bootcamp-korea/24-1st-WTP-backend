from django.views     import View
from django.http      import JsonResponse

from movies.models    import *

class MovieDetailView(View):
    def get(self, request, movie_id):
        

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({'MESSAGE':'Movie Not Exists'}, status = 404)

        movie = Movie.objects.get(id = movie_id)

        title          = movie.title
        release_date   = movie.release_date
        average_rating = movie.average_rating
        poster_image   = movie.poster_image
        trailer        = movie.trailer

        movie_details = {
            'title'          : title,
            'release_date'   : release_date,
            'genre'          : [genre.name for genre in movie.genre.all()],
            'country'        : [country.name for country in movie.country.all()],
            'average_rating' : average_rating,
            'poster_image'   : poster_image,
            'trailer'        : trailer
        }

        return JsonResponse({'movie_info': movie_details}, status = 200)
