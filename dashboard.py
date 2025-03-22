import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from scripts import part1 as p1  
from datetime import datetime

st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 20px;
    }
    .metric-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
    }
    .orange-box {
        background-color: #FFA500;
        color: white;
    }
    .black-box {
        background-color: #333333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Titel
st.markdown('<div class="title">Flight Statistics Dashboard</div>', unsafe_allow_html=True)

# Sidebar voor gebruikersinvoer (indien nodig)
st.sidebar.title("Filters")
selected_date = st.sidebar.date_input("Select a Date", min_value=datetime(2023, 1, 1), max_value=datetime(2023, 12, 31))

# Laad de data
conn = sqlite3.connect("data/flights_database.db")
df_flights = pd.read_sql_query("SELECT * FROM flights;", conn)

# Eerste rij: Total Flights en Flight Hours in oranje vakken
col1, col2 = st.columns(2)

with col1:
    total_flights = len(df_flights)
    st.markdown(
        f'<div class="metric-box orange-box">'
        f'<h3>Total Flights</h3>'
        f'<h1>{total_flights:,}</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col2:
    total_flight_hours = df_flights['air_time'].sum() / 60  # Converteer minuten naar uren
    st.markdown(
        f'<div class="metric-box orange-box">'
        f'<h3>Total Flight Hours</h3>'
        f'<h1>{total_flight_hours:,.0f}</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )

# Tweede rij: Percentage vertraagde vluchten en percentage te vroeg aangekomen vluchten in zwarte vakken
col3, col4 = st.columns(2)

with col3:
    delayed_flights = df_flights[df_flights['dep_delay'] > 0]
    percentage_delayed = (len(delayed_flights) / total_flights) * 100
    st.markdown(
        f'<div class="metric-box black-box">'
        f'<h3>Percentage Delayed Flights</h3>'
        f'<h1>{percentage_delayed:.2f}%</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col4:
    early_flights = df_flights[df_flights['arr_delay'] < 0]
    percentage_early = (len(early_flights) / total_flights) * 100
    st.markdown(
        f'<div class="metric-box black-box">'
        f'<h3>Percentage Early Arrivals</h3>'
        f'<h1>{percentage_early:.2f}%</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )


df = pd.read_csv('data/airports.csv')
def show_globalmap():
    # Maak de Plotly-figuur
    fig = px.scatter_geo(
        data_frame=df, 
        lat='lat', 
        lon='lon', 
        color='tzone', 
    )
    return fig  # Retourneer de figuur in plaats van deze te tonen

st.subheader("Global Flight Map")
fig = show_globalmap()  # Haal de Plotly-figuur op
st.plotly_chart(fig, use_container_width=True)

# Sluit de databaseverbinding
conn.close()