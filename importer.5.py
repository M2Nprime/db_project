import requests
import mysql.connector
from mysql.connector import Error
import time

# --- Database Functions ---
# (These functions are complete and remain unchanged)
def create_db_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password, database=db_name)
        print("MySQL connection successful!")
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None
# This is the corrected function that accepts 3 arguments
def insert_or_update_movie(cursor, movie_details, director_id):
    release_year = int(movie_details.get('release_date', '0').split('-')[0]) if movie_details.get('release_date') else None
    poster_url = f"https://image.tmdb.org/t/p/w500{movie_details.get('poster_path')}" if movie_details.get('poster_path') else None
    country = movie_details.get('production_countries', [{}])[0].get('name') if movie_details.get('production_countries') else None
    
    # The SQL query is updated to include the DirectorID column
    query = """
        INSERT INTO Movie (MovieID, Title, ReleaseYear, Summary, PosterURL, TMDbScore, DirectorID, DurationInMinutes, Country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            TMDbScore = VALUES(TMDbScore),
            DirectorID = VALUES(DirectorID);
    """
    values = (
        movie_details.get('id'),
        movie_details.get('title'),
        release_year,
        movie_details.get('overview'),
        poster_url,
        movie_details.get('vote_average'),
        director_id, # The 3rd argument is now used here
        movie_details.get('runtime'),
        country
    )
    
    try:
        cursor.execute(query, values)
    except Error as e:
        print(f"Error inserting/updating movie {values[1]}: {e}")

def insert_genre(cursor, genre_data):
    query = "INSERT IGNORE INTO Genre (GenreID, GenreName) VALUES (%s, %s)"
    cursor.execute(query, (genre_data.get('id'), genre_data.get('name')))

def insert_or_update_person(cursor, person_details):
    gender_map = {1: 'Female', 2: 'Male'}
    gender = gender_map.get(person_details.get('gender'))
    nationality = person_details.get('place_of_birth')
    query = """
        INSERT INTO Person (PersonID, FullName, BirthDate, Nationality, Gender)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE FullName=VALUES(FullName), BirthDate=VALUES(BirthDate), 
                                Nationality=VALUES(Nationality), Gender=VALUES(Gender);"""
    values = (
        person_details.get('id'), person_details.get('name'), person_details.get('birthday'),
        nationality, gender
    )
    cursor.execute(query, values)

def link_movie_to_genre(cursor, movie_id, genre_id):
    query = "INSERT IGNORE INTO Movie_Genre (MovieID, GenreID) VALUES (%s, %s)"
    cursor.execute(query, (movie_id, genre_id))

def link_movie_to_actor(cursor, movie_id, person_id):
    query = "INSERT IGNORE INTO Movie_Actor (MovieID, PersonID) VALUES (%s, %s)"
    cursor.execute(query, (movie_id, person_id))

# --- API Functions ---
# --- MODIFIED FUNCTION ---
def fetch_movies_from_list(api_key, list_type='popular', page_number=1):
    """ Fetches movies from a specified list type ('popular' or 'top_rated'). """
    api_url = f"https://api.themoviedb.org/3/movie/{list_type}?api_key={api_key}&language=en-US&page={page_number}"
    print(f"Fetching page {page_number} from '{list_type}' list...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.exceptions.RequestException: 
        return None

def fetch_movie_details(api_key, movie_id):
    # (Unchanged)
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=credits"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException: 
        return None

def fetch_person_details(api_key, person_id):
    # (Unchanged)
    api_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException: 
        return None

# --- Main Execution Block ---
if __name__ == "__main__":
    MY_API_KEY = "0d43d0069dc593f8ee0b63ae11c07f16"
    DB_PASSWORD = "Mohamadnabi@12"
    
    db_connection = create_db_connection("localhost", "root", DB_PASSWORD, "movie_rating_db")
    
    if db_connection and db_connection.is_connected():
        cursor = db_connection.cursor()
        
        # --- MODIFICATION 1: Processing BOTH lists ---
        lists_to_process = ['popular', 'top_rated']
        
        for list_name in lists_to_process:
            print(f"\n================ PROCESSING: {list_name.upper()} ================")
            for page_num in range(1, 4):
                # ... (بقیه کد بدون تغییر)
                movies_summary_list = fetch_movies_from_list(MY_API_KEY, list_name, page_num)
                if not movies_summary_list: continue

                for movie_summary in movies_summary_list:
                    # ... (کد پردازش هر فیلم)
                    movie_id = movie_summary.get('id')
                    movie_title = movie_summary.get('title')
                    print(f"Processing: {movie_title}")
                    
                    details = fetch_movie_details(MY_API_KEY, movie_id)
                    if not details: continue
                    
                    director_id = None
                    for member in details.get('credits', {}).get('crew', []):
                        if member.get('job') == 'Director':
                            director_id = member.get('id')
                            person_details = fetch_person_details(MY_API_KEY, director_id)
                            if person_details:
                                insert_or_update_person(cursor, person_details)
                            time.sleep(0.2) # Reduced sleep time
                            break
                    
                    insert_or_update_movie(cursor, details, director_id)

                    for genre in details.get('genres', []):
                        insert_genre(cursor, genre)
                        link_movie_to_genre(cursor, movie_id, genre.get('id'))

                    for actor_summary in details.get('credits', {}).get('cast', [])[:5]:
                        person_id = actor_summary.get('id')
                        person_details = fetch_person_details(MY_API_KEY, person_id)
                        if person_details:
                            insert_or_update_person(cursor, person_details)
                            link_movie_to_actor(cursor, movie_id, person_id)
                        
                        # --- MODIFICATION 2: Reduced sleep time ---
                        time.sleep(0.2)
                
                print(f"--- Committing changes for Page {page_num} of {list_name} ---")
                db_connection.commit()
        
        print("\nAll data has been successfully inserted/updated!")
        
        cursor.close()
        db_connection.close()
        print("MySQL connection is closed.")