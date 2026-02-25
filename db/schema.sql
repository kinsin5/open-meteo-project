CREATE TABLE IF NOT EXISTS api_call (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    call_timestamp TEXT DEFAULT (datetime('now')),
    status TEXT,
    cities_fetched INTEGER
);

CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL,
    voivodeship TEXT,
    elevation INTEGER

);

CREATE TABLE IF NOT EXISTS weather_current (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_call_id  INTEGER REFERENCES api_call(id),
    city_id  INTEGER REFERENCES city(id),
    time  TEXT,
    interval_seconds INTEGER,
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

CREATE TABLE IF NOT EXISTS weather_forecast(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    api_call_id  INTEGER REFERENCES api_call(id),
    city_id  INTEGER REFERENCES city(id),
    time  TEXT,
    temperature_2m REAL,
    relative_humidity_2m REAL,
    apparent_temperature REAL,
    precipitation_probability INTEGER,
    precipitation REAL,
    weather_code INTEGER,
    cloud_cover INTEGER,
    pressure_msl REAL,
    surface_pressure REAL,
    wind_speed_10m REAL
);
