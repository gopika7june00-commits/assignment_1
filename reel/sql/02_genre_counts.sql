SELECT
    g.genre_name,
    COUNT(DISTINCT mg.movie_id) AS movie_count
FROM movie_genres AS mg
JOIN genres AS g
    ON mg.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY movie_count DESC;