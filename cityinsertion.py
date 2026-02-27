import sqlite3
import requests
from entities.city import City
from typing import List

conn = sqlite3.connect('db/weather.db')

c = conn.cursor()

polish_cities_map = [
    "Warsaw",      # Central
    "Krakow",      # South
    "Lodz",        # Central
    "Wroclaw",     # Southwest
    "Poznan",      # West (your location!)
    "Gdansk",      # North (coast)
    "Szczecin",    # Northwest (coast)
    "Lublin",      # East
    "Katowice",    # South (Silesia)
    "Bialystok",   # Northeast
    "Olsztyn",     # North
    "Rzeszow",     # Southeast
    "Zielona Gora",
    "Opole",
    "Torun",
    "Kielce"
]

URL = 'https://geocoding-api.open-meteo.com/v1/search'

def cities_payload(city: str) -> dict:
    return {
        'name': city, 
        'count': '1',
        'language': 'en',
        'format' : 'json'
    }   

def fetch_city(city_payload: dict) -> dict:
    request = requests.get(
        URL,
        params=city_payload
    )
    data = request.json()
    return data

def fetch_cities(cities: list) -> List[City]:
    
    cities_li = []
    for city in cities:
        
        city_payload = cities_payload(city)
        city_data = fetch_city(city_payload)
        
        results = city_data['results'][0]
        
        city = City(
            id=results['id'],
            name=results['name'],
            latitude = results['latitude'],
            longitude = results['longitude'],
            voivodeship = results['admin1'],
            elevation = results['elevation']
        )
        
        cities_li.append(city)

    return cities_li

def insert_cities(cities: List[City]):
    with conn:
        for city in cities:
            c.execute("""INSERT OR IGNORE INTO city 
                      VALUES (:id, :name, :latitude, :longitude, 
                      :voivodeship, :elevation)""", 
                      {
                          'id': city.id,
                          'name': city.name,
                          'latitude': city.latitude,
                          'longitude': city.longitude,
                          'voivodeship': city.voivodeship,
                          'elevation': city.elevation,
                          })

def check_results():
    with conn:
        c.execute('SELECT * FROM city')
        results = c.fetchall()
        print(type(results))
        print(results)

cities = fetch_cities(polish_cities_map)
insert_cities(cities)
check_results()

conn.close()