
SELECT
    title,
    budget,
    revenue,
    revenue - budget AS profit
FROM movies
WHERE budget > 0
  AND revenue > 0
ORDER BY revenue DESC
LIMIT 20;
