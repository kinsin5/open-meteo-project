SELECT name, latitude, longitude, temperature_2m
FROM (
    SELECT c.name, c.latitude, c.longitude, w.temperature_2m,
        ROW_NUMBER() OVER (PARTITION BY c.name ORDER BY c.name) AS rn
    FROM weather_current w
    JOIN city c ON w.city_id = c.id
) t
WHERE rn = 1;