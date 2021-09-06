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

        # # 1
        # image_url = [image.image_url for image in movie.image_set.all()]

        # 2
        image_url = []
        images = Image.objects.filter(movie_id = movie_id)
        for image in images:
            image_url.append(image.image_url)

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

        print(participants)

        movie_details = {
            'title'          : title,
            'release_date'   : release_date,
            'genre'          : [genre.name for genre in movie.genre.all()],
            'country'        : [country.name for country in movie.country.all()],
            'average_rating' : average_rating,
            'poster_image'   : poster_image,
            'trailer'        : trailer,
            'image_url'      : image_url,
            'participants'   : participants,
        }

        return JsonResponse({'movie_info': movie_details}, status = 200)
