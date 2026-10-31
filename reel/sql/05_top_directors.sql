
SELECT
    person_name AS director_name,
    COUNT(DISTINCT movie_id) AS movie_count
FROM crew
WHERE LOWER(TRIM(job)) = 'director'
  AND person_name IS NOT NULL
GROUP BY person_name
ORDER BY movie_count DESC
LIMIT 10;
