SELECT site_name,
       SUM(electricity_usage) AS total_usage,
       RANK() OVER (ORDER BY SUM(electricity_usage) DESC) AS usage_rank
FROM fact_energy
GROUP BY site_name
ORDER BY usage_rank;
