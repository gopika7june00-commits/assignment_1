
SELECT
    CAST(strftime('%Y', release_date) AS INTEGER) AS release_year,
    COUNT(*) AS movie_count
FROM movies
WHERE release_date IS NOT NULL
  AND TRIM(release_date) != ''
GROUP BY release_year
ORDER BY release_year;
