-- =================================================================
-- File: schema.sql
-- Purpose: Defines the database structure. Can be run multiple times without errors.
-- =================================================================

-- Part 1: Database Setup
CREATE DATABASE IF NOT EXISTS movie_rating_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movie_rating_db;

-- Part 2: Table Creation (DDL)

CREATE TABLE IF NOT EXISTS Genre (
  GenreID INT PRIMARY KEY AUTO_INCREMENT,
  GenreName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Person (
  PersonID INT PRIMARY KEY AUTO_INCREMENT,
  FullName VARCHAR(255) NOT NULL,
  BirthDate DATE NULL,
  Gender VARCHAR(50) NULL,
  Nationality VARCHAR(100) NULL
);

CREATE TABLE IF NOT EXISTS Movie (
  MovieID INT PRIMARY KEY AUTO_INCREMENT,
  Title VARCHAR(255) NOT NULL,
  ReleaseYear INT NULL,
  Summary TEXT NULL,
  DurationInMinutes INT NULL,
  Country VARCHAR(100) NULL,
  PosterURL VARCHAR(512) NULL,
  TMDbScore DECIMAL(3, 1) NULL,
  DirectorID INT NULL,
  CONSTRAINT fk_director FOREIGN KEY (DirectorID) REFERENCES Person(PersonID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS User (
  UserID INT PRIMARY KEY AUTO_INCREMENT,
  Username VARCHAR(100) NOT NULL UNIQUE,
  Email VARCHAR(255) NOT NULL UNIQUE,
  PasswordHash VARCHAR(255) NOT NULL,
  CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Movie_Genre (
  MovieID INT,
  GenreID INT,
  PRIMARY KEY (MovieID, GenreID),
  FOREIGN KEY (MovieID) REFERENCES Movie(MovieID) ON DELETE CASCADE,
  FOREIGN KEY (GenreID) REFERENCES Genre(GenreID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movie_Actor (
  MovieID INT,
  PersonID INT,
  PRIMARY KEY (MovieID, PersonID),
  FOREIGN KEY (MovieID) REFERENCES Movie(MovieID) ON DELETE CASCADE,
  FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Rating (
  UserID INT,
  MovieID INT,
  Score INT NOT NULL CHECK (Score >= 1 AND Score <= 10),
  RatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (UserID, MovieID),
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
  FOREIGN KEY (MovieID) REFERENCES Movie(MovieID) ON DELETE CASCADE
);

-- Part 3: View Creation
-- =================================================================
CREATE OR REPLACE VIEW v_MovieWithDirector AS
SELECT
    m.MovieID, m.Title, m.ReleaseYear, m.TMDbScore, m.Country, p.FullName AS DirectorName
FROM Movie AS m JOIN Person AS p ON m.DirectorID = p.PersonID;

CREATE OR REPLACE VIEW v_GenreStats AS
SELECT
    g.GenreName, COUNT(m.MovieID) AS NumberOfMovies, ROUND(AVG(m.TMDbScore), 2) AS AverageScore
FROM Genre AS g JOIN Movie_Genre AS mg ON g.GenreID = mg.GenreID
JOIN Movie AS m ON mg.MovieID = m.MovieID
WHERE m.TMDbScore IS NOT NULL
GROUP BY g.GenreName;


-- Stored Procedure 1: Get all movies for a specific genre name.
DELIMITER $$

CREATE PROCEDURE sp_GetMoviesByGenre(IN genre_name_param VARCHAR(100))
BEGIN
    SELECT
        m.Title,
        m.ReleaseYear,
        m.TMDbScore
    FROM
        Movie AS m
    JOIN
        Movie_Genre AS mg ON m.MovieID = mg.MovieID
    JOIN
        Genre AS g ON mg.GenreID = g.GenreID
    WHERE
        g.GenreName = genre_name_param
    ORDER BY
        m.TMDbScore DESC;
END$$

DELIMITER ;
