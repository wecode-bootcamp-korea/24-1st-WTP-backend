import csv
import os
import django
import sys

# 현재 디렉토리 경로 표시
os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

# 프로젝트명.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atchapedia.settings")
django.setup()

from movies.models import *
from users.models import User


# csv 파일 경로
# CSV_PATH = './grades.csv'
# CSV_PATH = './movies.csv'
# CSV_PATH = './countries.csv'
# CSV_PATH = './movies_countries.csv'
# CSV_PATH = './genres.csv'
# CSV_PATH = './movies_genres.csv'
# CSV_PATH = './userss.csv'
CSV_PATH = './ratings.csv'

# encoding 설정 필요
with open(CSV_PATH, newline='', encoding='utf-8-sig') as csvfile:
    data_reader = csv.DictReader(csvfile)

    # for row in data_reader:
    #     # print(row)
    #     Grade.objects.create(
    #         grade = row['grade']
    #     )

    # for row in data_reader:
    #     # print(row)
    #     Movie.objects.create(
    #         title          = row['title'],
    #         release_date   = row['release_date'],
    #         description    = row['description'],
    #         running_time   = row['running_time'],
    #         average_rating = row['average_rating'],
    #         grade_id       = row['grade_id'],
    #         poster_image   = row['poster_image'],
    #         trailer        = row['trailer']
    #     )

    # for row in data_reader:
    #     # print(row)
    #     Country.objects.create(
    #         name = row['name']
    #     )

    # for row in data_reader:
    #     # print(row)
    #     MovieCountry.objects.create(
    #         movie_id = row['movie_id'],
    #         country_id = row['country_id']
    #     )

    # for row in data_reader:
    #     # print(row)
    #     Genre.objects.create(
    #         name = row['name']
    #     )

    # for row in data_reader:
    #     print(row)
    #     MovieGenre.objects.create(
    #         movie_id = row['movie_id'],
    #         genre_id = row['genre_id']
    #     )

    # for row in data_reader:
    #     print(row)
    #     User.objects.create(
    #         name         = row['name'],
    #         email        = row['email'],
    #         password     = row['password'],
    #         introduction = row['introduction']
    #    )

    for row in data_reader:
        print(row)
        Rating.objects.create(
            user_id    = row['user_id'],
            movie_id   = row['movie_id'],
            rate       = row['rate'],
            comment    = row['comment']
        )