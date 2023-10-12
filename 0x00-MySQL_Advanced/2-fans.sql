-- a SQL script
-- ranks country origins of bands, ordered by the number of (non-unique) fans

SELECT origin, SUM(nb_fans) AS total_fans, RANK() OVER (ORDER BY SUM(nb_fans) DESC) AS country_rank
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
