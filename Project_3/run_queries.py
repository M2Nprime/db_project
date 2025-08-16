import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movieproject.settings')
django.setup()

# Import models and ORM tools
from movies.models import Movie, Person, Genre, MovieActor
from django.db.models import Count, Avg, Q, F

def run():
    print("--- ORM Query 1: Movies after 2010 ---")
    query1 = Movie.objects.filter(releaseyear__gt=2010).order_by('-tmdbscore')
    for movie in query1[:5]:
        print(f"  - {movie.title} ({movie.releaseyear}) - Score: {movie.tmdbscore}")

    print("\n--- ORM Query 2: 'Action' movies ---")
    query2 = Movie.objects.filter(moviegenre__genreid__genrename='Action')
    for movie in query2[:5]:
        print(f"  - {movie.title}")

    print("\n--- ORM Query 3: Top 10 actors by movie count ---")
    query3 = Person.objects.annotate(movie_count=Count('movieactor__movieid')).order_by('-movie_count')[:10]
    for actor in query3:
        print(f"  - {actor.fullname} has been in {actor.movie_count} movies.")

    print("\n--- ORM Query 4: Genre stats (with HAVING) ---")
    query4 = Genre.objects.annotate(
        numberofmovies=Count('moviegenre__movieid'),
        averagescore=Avg('moviegenre__movieid__tmdbscore')
    ).filter(numberofmovies__gt=5).order_by('-averagescore')
    for genre in query4:
        print(f"  - Genre: {genre.genrename}, Movies: {genre.numberofmovies}, Avg Score: {round(genre.averagescore, 2)}")

    print("\n--- ORM Query 5: Advanced filter with Q objects (OR condition) ---")
    query5 = Movie.objects.filter(Q(durationinminutes__gt=180) | Q(tmdbscore__gt=8.5)).order_by('-tmdbscore')
    print("Movies longer than 3 hours OR score > 8.5:")
    for movie in query5[:10]:
        print(f"  - {movie.title} (Duration: {movie.durationinminutes} min, Score: {movie.tmdbscore})")

    print("\n--- ORM Query 6: Advanced filter with F objects ---")
    query6 = Movie.objects.filter(
        durationinminutes__gt=F('tmdbscore') * 20,
        durationinminutes__isnull=False,
        tmdbscore__isnull=False
    )
    print("Movies with runtime > 20x their score:")
    for movie in query6[:5]:
        print(f"  - {movie.title} (Runtime: {movie.durationinminutes}, Score: {movie.tmdbscore})")

    print("\n--- ORM Query 7: Subquery to find above-average movies ---")
    average_score = Movie.objects.filter(tmdbscore__isnull=False).aggregate(avg_score=Avg('tmdbscore'))['avg_score']
    query7 = Movie.objects.filter(tmdbscore__gt=average_score, releaseyear__gt=2000).order_by('-tmdbscore')
    print(f"Movies made after 2000 with score > average ({round(average_score, 2)}):")
    for movie in query7[:5]:
        print(f"  - {movie.title} ({movie.releaseyear}) - Score: {movie.tmdbscore}")

    print("\n--- ORM Query 8: Finding movies with two specific actors ---")
    actor_names = ['Leonardo DiCaprio', 'Tom Hardy']
    query8 = Movie.objects.filter(
        movieactor__personid__fullname__in=actor_names
    ).annotate(actor_count=Count('movieid')).filter(actor_count=len(actor_names))
    print(f"Movies starring both {actor_names[0]} and {actor_names[1]}:")
    for movie in query8:
        print(f"  - {movie.title}")

    print("\n--- ORM Query 9: Chaining multiple filters (AND condition) ---")
    query9 = Movie.objects.filter(
    country='United States of America',
    releaseyear__gt=2010,
    durationinminutes__lt=110,
    durationinminutes__isnull=False # To be safe
    ).order_by('-releaseyear')

    print("American movies post-2010, shorter than 110 minutes:")
    if not query9:
        print("  - No such movies found.")
    else:
        for movie in query9[:5]:
            print(f"  - {movie.title} ({movie.releaseyear}) - Runtime: {movie.durationinminutes} min")


    print("\n--- ORM Query 10: Performance optimization with prefetch_related ---")

    # This query finds the top 5 directors by movie count and efficiently fetches all their movies.
    # This is a perfect and clean example of solving the N+1 problem.
    top_directors = Person.objects.annotate(
        movie_count=Count('movie') # We can count the reverse relationship directly
    ).order_by(
        '-movie_count'
    ).prefetch_related('movie_set')[:5]

    print("Top 5 directors and their movies (fetched efficiently):")
    for director in top_directors:
        print(f"  - Director: {director.fullname} ({director.movie_count} movies)")
        # Accessing director.movie_set.all() here does NOT cause a new database query.
        movie_titles = [movie.title for movie in director.movie_set.all()]
        for title in movie_titles:
            print(f"    - {title}")

    # --- NEW QUERY TO TEST THE CUSTOM METHOD ---
    print("\n--- Testing Custom Model Method ---")
    
    # Get a few movies that have a long duration
    long_movies = Movie.objects.filter(durationinminutes__isnull=False).order_by('-durationinminutes')[:5]
    
    print("Displaying movie duration using the custom model method:")
    for movie in long_movies:
        # We can call our new method directly on the movie object!
        print(f"  - {movie.title}: {movie.get_duration_display()}")

    # --- NEW SECTION TO TEST THE CUSTOM PROPERTY ---
    print("\n--- Testing Custom Model Property (@property) ---")
    
    # Get one person who has a birthdate recorded in the database
    actor_with_bday = Person.objects.filter(birthdate__isnull=False).first()
    
    if actor_with_bday:
        print(f"Testing with actor: {actor_with_bday.fullname}")
        # Access the 'age' property just like a regular field (NO parentheses!)
        print(f"  - Birth Date: {actor_with_bday.birthdate}")
        print(f"  - Calculated Age: {actor_with_bday.age} years old")
    else:
        print("  - Could not find any actor with a birthdate to test.")
        
# --- Main execution block ---
if __name__ == "__main__":
    run()