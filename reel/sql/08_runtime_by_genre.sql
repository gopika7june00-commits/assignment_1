
SELECT
    g.genre_name,
    ROUND(AVG(m.runtime), 1) AS average_runtime_minutes,
    COUNT(DISTINCT m.movie_id) AS movie_count
FROM movie_genres AS mg
JOIN genres AS g
    ON mg.genre_id = g.genre_id
JOIN movies AS m
    ON mg.movie_id = m.movie_id
WHERE m.runtime IS NOT NULL
  AND m.runtime > 0
GROUP BY g.genre_name
ORDER BY average_runtime_minutes DESC;
