-- 1. Create new table without interval_seconds
CREATE TABLE weather_current_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_call_id INTEGER REFERENCES api_call(id),
    city_id INTEGER REFERENCES city(id),
    time TEXT,
    temperature_2m REAL,
    relative_humidity_2m REAL,
    apparent_temperature REAL,
    is_day INTEGER,
    precipitation REAL,
    weather_code INTEGER,
    cloud_cover INTEGER,
    pressure_msl REAL,
    surface_pressure REAL,
    wind_speed_10m REAL
);

-- 2. Copy data (excluding interval_seconds)
INSERT INTO weather_current_new 
    (id, api_call_id, city_id, time, temperature_2m, relative_humidity_2m,
     apparent_temperature, is_day, precipitation, weather_code,
     cloud_cover, pressure_msl, surface_pressure, wind_speed_10m)
SELECT 
    id, api_call_id, city_id, time, temperature_2m, relative_humidity_2m,
    apparent_temperature, is_day, precipitation, weather_code,
    cloud_cover, pressure_msl, surface_pressure, wind_speed_10m
FROM weather_current;

-- 3. Drop old table
DROP TABLE weather_current;

-- 4. Rename new table
ALTER TABLE weather_current_new RENAME TO weather_current;