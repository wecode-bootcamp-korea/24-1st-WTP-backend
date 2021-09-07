from django.views              import View
from django.http.response      import JsonResponse

from movies.models    import *

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