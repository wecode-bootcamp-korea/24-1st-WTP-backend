from django.db import models
from django.db.models.deletion import SET_DEFAULT

from users.models import User


class Movie(models.Model):
    title          = models.CharField(max_length=100) 
    release_date   = models.DateField()
    description    = models.TextField(default="등록된 소개글이 없습니다.")
    running_time   = models.IntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    grade          = models.ForeignKey("Grade", null=True, on_delete=models.SET_NULL)
    poster_image   = models.URLField(max_length=500)
    trailer        = models.CharField(max_length=500, null=True)
    participant    = models.ManyToManyField("Participant", through="MovieParticipant")
    user_rating    = models.ManyToManyField(User, through="Rating", related_name="rater")
    user_wish      = models.ManyToManyField(User, through="WishList", related_name="wisher")
    genre          = models.ManyToManyField("Genre", through="MovieGenre")
    country        = models.ManyToManyField("Country", through="MovieCountry")

    class Meta:
        db_table = "movies"


class Grade(models.Model):
    grade = models.CharField(max_length=45)
    
    class Meta:
        db_table = "grades"


class Participant(models.Model):
    name      = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = "participants"


class MovieParticipant(models.Model):
    movie       = models.ForeignKey("Movie", on_delete=models.CASCADE)
    participant = models.ForeignKey("Participant", on_delete=models.CASCADE)
    role        = models.CharField(max_length=10)

    class Meta:
        db_table = "movie_participants"


class Rating(models.Model):
    user    = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    movie   = models.ForeignKey("Movie", on_delete=models.CASCADE)
    rate    = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=1000)

    class Meta:
        db_table = "ratings"


class WishList(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    movie        = models.ForeignKey("Movie", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wish_lists"


class Genre(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "genres"


class MovieGenre(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_genres"


class Image(models.Model):
    image_url = models.URLField(max_length=500)
    movie     = models.ForeignKey("Movie", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"


class Country(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "countries"


class MovieCountry(models.Model):
    movie   = models.ForeignKey("Movie", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_countries"