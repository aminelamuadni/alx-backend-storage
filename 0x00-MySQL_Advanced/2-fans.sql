-- Rank countries by the total number of fans of metal bands
SELECT
    origin,
    SUM(fans) AS nb_fans
FROM
    bands
GROUP BY
    origin
ORDER BY
    nb_fans DESC;