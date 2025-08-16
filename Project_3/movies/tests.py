from django.test import TestCase
from .models import Movie, Person, Genre, MovieActor

class QueryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data ONCE for all tests
        cls.actor1 = Person.objects.create(fullname="Leonardo DiCaprio")
        cls.actor2 = Person.objects.create(fullname="Tom Hardy")
        cls.movie = Movie.objects.create(
            title="Inception", 
            releaseyear=2010,
            tmdbscore=8.8,
            durationinminutes=148
        )
        MovieActor.objects.create(movieid=cls.movie, personid=cls.actor1)
        MovieActor.objects.create(movieid=cls.movie, personid=cls.actor2)
        
        Genre.objects.create(genrename="Action")
        
    def test_query8_movies_with_two_actors(self):
        from django.db.models import Count
        actor_names = ['Leonardo DiCaprio', 'Tom Hardy']
        queryset = Movie.objects.filter(
            movieactor__personid__fullname__in=actor_names
        ).annotate(actor_count=Count('movieid')).filter(actor_count=len(actor_names))
        
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().title, "Inception")

    def test_query4_genre_stats(self):
        from django.db.models import Count, Avg
        queryset = Genre.objects.annotate(
            numberofmovies=Count('moviegenre__movieid'),
            averagescore=Avg('moviegenre__movieid__tmdbscore')
        )
        
        # Just test the annotation works
        genre = queryset.first()
        self.assertIsNotNone(genre.numberofmovies)
        self.assertIsNotNone(genre.averagescore)