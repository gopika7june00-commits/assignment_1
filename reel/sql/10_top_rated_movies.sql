
SELECT
    title,
    vote_average,
    vote_count
FROM movies
WHERE vote_average IS NOT NULL
  AND vote_count >= 100
ORDER BY vote_average DESC, vote_count DESC
LIMIT 10;
