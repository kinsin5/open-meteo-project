import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng
import sqlite3

conn = sqlite3.connect('db/weather.db')

c = conn.cursor()

def get_cities() -> pd.DataFrame:
    with conn:
        c.execute('SELECT * FROM city')
        data = c.fetchall()
        cols = ['id', 'name', 'latitude', 'longitude', 'voivodeship', 'elevation']
        return pd.DataFrame(data=data, columns=cols)
    
df = get_cities()

st.map(df)