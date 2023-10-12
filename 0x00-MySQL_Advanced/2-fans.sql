-- a SQL script
-- ranks country origins of bands, ordered by the number of (non-unique) fans

SELECT
    origin,
    SUM(nb_fans) AS total_fans,
    (SELECT COUNT(DISTINCT origin) + 1
	     FROM metal_bands AS subquery
	     WHERE SUM(nb_fans) > (SELECT SUM(nb_fans) FROM metal_bands WHERE origin = subquery.origin)
	    ) AS country_rank
	FROM metal_bands
	GROUP BY origin
	ORDER BY total_fans DESC;

