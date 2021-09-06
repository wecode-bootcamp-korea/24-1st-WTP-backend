from django.core.management.base import BaseCommand
import pandas as pd
import random
from users.models import User
from movies.models import *
from my_settings import RATE

# from users.models import User
# import django
# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram.settings")
# django.setup()

# from instagram_app.models import *

# user = pd.read_csv('user.csv')

# print(user['name'])


# class Command(BaseCommand):

#     def handle(self, *args, **options):

#         df = pd.read_csv('user.csv')

        

'''
grades, movies 완료
'''
class Command(BaseCommand):

    def handle(self, *args, **options):
        
        '''
        # Participant
        participants =pd.read_csv('participant.csv')

        for i in range(len(participants)):
            Participant.objects.create(
                name = participants['name'][i],
                image_url = participants['img_url'][i]
            )


        # movie_participants
        movie_participants =pd.read_csv('movie_participants.csv')

        for i in range(len(movie_participants)):
            MovieParticipant.objects.create(
                movie_id = movie_participants['movie_id'][i],
                participant_id = movie_participants['participant_id'][i],
                role = movie_participants['role'][i]
            )


        # movie_countries
        movie_countries = pd.read_csv('movie_countries.csv')

        for i in range(len(movie_countries)):
            MovieCountry.objects.create(
                movie_id = movie_countries['movie_id'][i],
                country_id = movie_countries['country_id'][i]
            )


        # countries
        country = pd.read_csv('country.csv')
        for i in range(len(country)):
            Country.objects.create(
                name = country['name'][i]
            )


        # grade 
        grade = pd.read_csv('grade.csv')
        for i in range(len(grade)):
            Grade.objects.create(
                grade = grade['grade'][i]
            )


        # genres
        genre = pd.read_csv('genre.csv')
        for i in range(len(genre)):
            Genre.objects.create(
                name = genre['name'][i]
            )


        


        # movies
        movie = pd.read_csv('movie.csv')
        for i in range(len(movie)):
            Movie.objects.create(
                title          = movie['title'][i],
                release_date   = movie['release_date'][i],
                description    = movie['description'][i],
                running_time   = movie['running_time'][i],
                average_rating = movie['avg_rating'][i],
                grade_id       = movie['grade_id'][i],
                poster_image   = movie['poster_image'][i],
                trailer        = movie['trailer'][i],
            )
        '''
        # ratings

        # ratings = pd.read_csv('csvsheets/ratings.csv')
        # for i in range(len(ratings)):
        #     Rating.objects.create(
        #         user_id = ratings['user_id'][i],
        #         movie_id = ratings['movie_id'][i],
        #         comment = ratings['comment'][i],
        #         rate = random.choice(RATE)
        #     )

        # images

        # images = pd.read_csv('csvsheets/images.csv')
        # for i in range(len(images)):
        #     Image.objects.create(
        #         movie_id = images['movie_id'][i],
        #         image_url = images['image_url'][i],
        #     )

        # movie_genres
        # movie_genres = pd.read_csv('csvsheets/movie_genres.csv')
        # for i in range(len(movie_genres)):
        #     MovieGenre.objects.create(
        #         movie_id = movie_genres['movie_id'][i],
        #         genre_id = movie_genres['genre_id'][i],
        #     )
        