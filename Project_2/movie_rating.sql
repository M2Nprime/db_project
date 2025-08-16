

-- Query 1: Find movies released after 2010, ordered by score.
SELECT 
    Title, 
    ReleaseYear, 
    TMDbScore
FROM 
    Movie
WHERE 
    ReleaseYear > 2010
ORDER BY 
    TMDbScore DESC;
-- Query 2: Find all movies belonging to the 'Action' genre using JOINs.
SELECT
    m.Title,
    m.ReleaseYear,
    g.GenreName
FROM
    Movie AS m
JOIN
    Movie_Genre AS mg ON m.MovieID = mg.MovieID
JOIN
    Genre AS g ON mg.GenreID = g.GenreID
WHERE
    g.GenreName = 'Action';
    -- Query 3: Find the top 10 actors with the most movies.
SELECT
    p.FullName,
    COUNT(ma.MovieID) AS MovieCount
FROM
    Person AS p
JOIN
    Movie_Actor AS ma ON p.PersonID = ma.PersonID
GROUP BY
    p.PersonID, p.FullName
ORDER BY
    MovieCount DESC
LIMIT 10;
-- Query 4: Average score per genre, for genres with more than 5 movies.
SELECT
    g.GenreName,
    COUNT(m.MovieID) AS NumberOfMovies,
    AVG(m.TMDbScore) AS AverageScore
FROM
    Genre AS g
JOIN
    Movie_Genre AS mg ON g.GenreID = mg.GenreID
JOIN
    Movie AS m ON mg.MovieID = m.MovieID
WHERE
    m.TMDbScore IS NOT NULL -- Ignore movies with no score
GROUP BY
    g.GenreName
HAVING
    NumberOfMovies > 5
ORDER BY
    AverageScore DESC;
    
-- Query 5: Find the movie(s) with the highest score using a subquery.
SELECT
    Title,
    TMDbScore
FROM
    Movie
WHERE
    TMDbScore = (SELECT MAX(TMDbScore) FROM Movie);
    
-- Query 6: Find the debut year for actors with more than one movie.
SELECT
    p.FullName,
    COUNT(m.MovieID) AS MovieCount,
    MIN(m.ReleaseYear) AS DebutYear
FROM
    Person AS p
JOIN
    Movie_Actor AS ma ON p.PersonID = ma.PersonID
JOIN
    Movie AS m ON ma.MovieID = m.MovieID
WHERE
    m.ReleaseYear IS NOT NULL
GROUP BY
    p.PersonID, p.FullName
HAVING
    MovieCount > 1
ORDER BY
    DebutYear ASC;

-- Query 7: Find above-average movies made after the year 2000.
SELECT
    Title,
    TMDbScore,
    ReleaseYear
FROM
    Movie
WHERE
    TMDbScore > (SELECT AVG(TMDbScore) FROM Movie WHERE TMDbScore IS NOT NULL)
    AND ReleaseYear > 2000
ORDER BY
    TMDbScore DESC;
    
-- Query 8 
SELECT
    m.Title,
    m.ReleaseYear
FROM
    Movie AS m
JOIN
    Movie_Actor AS ma ON m.MovieID = ma.MovieID
JOIN
    Person AS p ON ma.PersonID = p.PersonID
WHERE
    p.FullName IN ('Leonardo DiCaprio', 'Tom Hardy') 
GROUP BY
    m.MovieID, m.Title, m.ReleaseYear
HAVING
    COUNT(p.PersonID) = 2;
-- Query 9: Find the director with the highest average movie score (for directors with >1 movie).
SELECT
    p.FullName AS DirectorName,
    COUNT(m.MovieID) AS MovieCount,
    AVG(m.TMDbScore) AS AverageScore
FROM
    Person AS p
JOIN
    Movie AS m ON p.PersonID = m.DirectorID
WHERE
    m.TMDbScore IS NOT NULL
GROUP BY
    p.PersonID, p.FullName
HAVING
    MovieCount > 1
ORDER BY
    AverageScore DESC
LIMIT 10;
    
-- Query 10: List all actors who have starred in a movie directed by Christopher Nolan.
SELECT
    p_actor.FullName AS ActorName,
    m.Title AS MovieTitle
FROM
    Movie AS m
-- Join to find the director's name
JOIN
    Person AS p_director ON m.DirectorID = p_director.PersonID
-- Join to get the actor links
JOIN
    Movie_Actor AS ma ON m.MovieID = ma.MovieID
-- Join to find the actor's name
JOIN
    Person AS p_actor ON ma.PersonID = p_actor.PersonID
WHERE
    p_director.FullName = 'Christopher Nolan'
ORDER BY
    ActorName ASC;
    
-- Example 1: See everything in the view
SELECT * FROM v_MovieWithDirector;
    
-- Example 2: filter and order the view
SELECT 
    Title, 
    DirectorName 
FROM 
    v_MovieWithDirector
WHERE 
    TMDbScore > 8.5
ORDER BY 
    ReleaseYear DESC;
    

-- Using the new view 2 to get the same result as Query 4
SELECT
    *
FROM
    v_GenreStats
WHERE
    NumberOfMovies > 5
ORDER BY
    AverageScore DESC;

-- Example 1: Get all 'Action' movies
CALL sp_GetMoviesByGenre('Action');

-- Example 2: Get all 'Drama' movies
CALL sp_GetMoviesByGenre('Drama');

-- Example 3: Get all 'Science Fiction' movies
CALL sp_GetMoviesByGenre('Science Fiction');


DROP TRIGGER IF EXISTS trg_AfterMovieUpdate;

DELIMITER $$
CREATE TRIGGER trg_AfterMovieUpdate
AFTER UPDATE ON Movie
FOR EACH ROW
BEGIN
    INSERT INTO Movie_Log (MovieID, ActionType)
    VALUES (NEW.MovieID, CONCAT('Movie details updated. New score: ', NEW.TMDbScore));
END$$
DELIMITER ;
-- Create an index on the 'Title' column of the 'Movie' table to speed up searches.
CREATE INDEX idx_movie_title ON Movie (Title);

SELECT * FROM Movie WHERE Title = 'Inception';
EXPLAIN SELECT * FROM Movie WHERE Title = 'Inception';