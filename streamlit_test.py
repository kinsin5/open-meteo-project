import pandas as pd
import streamlit as st
import sqlite3

conn = sqlite3.connect('db/weather.db')

c = conn.cursor()

def get_cities() -> pd.DataFrame:
    with conn:
        c.execute('SELECT * FROM city')
        data = c.fetchall()
        cols = ['id', 'name', 'latitude', 'longitude', 'voivodeship', 'elevation']
        return pd.DataFrame(data=data, columns=cols)
    

df_current = pd.read_sql('SELECT * FROM weather_current', con=conn)
df_city = pd.read_sql('SELECT * FROM city', con=conn).set_index('id')

df = df_current.join(df_city, on='city_id', how='inner')

st.map(
    data=df, latitude='latitude', longitude='longitude',
    size='temperature_2m')
st.write(df)
