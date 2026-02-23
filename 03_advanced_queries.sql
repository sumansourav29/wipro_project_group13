WITH yearly_usage AS (
    SELECT year,
           SUM(electricity_usage) AS total_usage
    FROM fact_energy
    GROUP BY year
)
SELECT year,
       total_usage,
       LAG(total_usage) OVER (ORDER BY year) AS previous_year,
       total_usage - LAG(total_usage) OVER (ORDER BY year) AS growth
FROM yearly_usage;
