# Final and perfected models.py
from django.db import models

class Genre(models.Model):
    genreid = models.AutoField(db_column='GenreID', primary_key=True)
    genrename = models.CharField(db_column='GenreName', unique=True, max_length=100)
    class Meta: db_table = 'genre'

class Person(models.Model):
    personid = models.AutoField(db_column='PersonID', primary_key=True)
    fullname = models.CharField(db_column='FullName', max_length=255)
    birthdate = models.DateField(db_column='BirthDate', blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=50, blank=True, null=True)
    nationality = models.CharField(db_column='Nationality', max_length=100, blank=True, null=True)
    class Meta: db_table = 'person'

class Movie(models.Model):
    movieid = models.AutoField(db_column='MovieID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=255)
    releaseyear = models.IntegerField(db_column='ReleaseYear', blank=True, null=True)
    summary = models.TextField(db_column='Summary', blank=True, null=True)
    durationinminutes = models.IntegerField(db_column='DurationInMinutes', blank=True, null=True)
    country = models.CharField(db_column='Country', max_length=100, blank=True, null=True)
    posterurl = models.CharField(db_column='PosterURL', max_length=512, blank=True, null=True)
    tmdbscore = models.DecimalField(db_column='TMDbScore', max_digits=3, decimal_places=1, blank=True, null=True)
    directorid = models.ForeignKey(Person, models.SET_NULL, db_column='DirectorID', blank=True, null=True)
    class Meta: db_table = 'movie'

class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)
    username = models.CharField(db_column='Username', unique=True, max_length=100)
    email = models.CharField(db_column='Email', unique=True, max_length=255)
    passwordhash = models.CharField(db_column='PasswordHash', max_length=255)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    class Meta: db_table = 'user'

class MovieGenre(models.Model):
    movieid = models.ForeignKey(Movie, models.CASCADE, db_column='MovieID')
    genreid = models.ForeignKey(Genre, models.CASCADE, db_column='GenreID')
    class Meta:
        db_table = 'movie_genre'
        unique_together = (('movieid', 'genreid'),)

class MovieActor(models.Model):
    movieid = models.ForeignKey(Movie, models.CASCADE, db_column='MovieID')
    personid = models.ForeignKey(Person, models.CASCADE, db_column='PersonID')
    class Meta:
        db_table = 'movie_actor'
        unique_together = (('movieid', 'personid'),)

class Rating(models.Model):
    userid = models.ForeignKey(User, models.CASCADE, db_column='UserID')
    movieid = models.ForeignKey(Movie, models.CASCADE, db_column='MovieID')
    score = models.IntegerField(db_column='Score')
    ratedat = models.DateTimeField(db_column='RatedAt', blank=True, null=True)
    class Meta:
        db_table = 'rating'
        unique_together = (('userid', 'movieid'),)