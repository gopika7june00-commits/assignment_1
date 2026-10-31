SELECT
    title,
    revenue
FROM movies
WHERE revenue > 0
ORDER BY revenue DESC
LIMIT 10;