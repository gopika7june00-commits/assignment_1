
SELECT
    keyword_name,
    COUNT(DISTINCT movie_id) AS movie_count
FROM movie_keywords
WHERE keyword_name IS NOT NULL
  AND TRIM(keyword_name) != ''
GROUP BY keyword_name
ORDER BY movie_count DESC
LIMIT 10;
