SELECT
    g.genre_name,
    ROUND(AVG(m.vote_average), 2) AS average_rating,
    COUNT(DISTINCT m.movie_id) AS movie_count
FROM movie_genres AS mg
JOIN genres AS g
    ON mg.genre_id = g.genre_id
JOIN movies AS m
    ON mg.movie_id = m.movie_id
WHERE m.vote_average IS NOT NULL
GROUP BY g.genre_name
ORDER BY average_rating DESC;