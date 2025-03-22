import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from scripts import part1 as p1  
from scripts import part4 as p4
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
    .sidebar-button {
        background-color: #FFA500;
        color: white;
        border: none;
        padding: 10px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }
    .sidebar-button:hover {
        background-color: #e69500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

conn = sqlite3.connect("data/flights_database.db")

df_airports = pd.read_sql_query("SELECT * FROM airports;", conn)
airports_arr= df_airports['faa'].dropna().unique().tolist()
airports_dep= ['JFK','LGA','EWR']

df_flights = pd.read_sql_query("SELECT * FROM flights;", conn)

selected_departure = st.sidebar.selectbox("Choose Departure Airport", airports_dep)
selected_destination = st.sidebar.selectbox("Choose Arrival Airport", airports_arr)
faa_list = [selected_destination]


page = "dashboard"

if st.sidebar.button("Home", key="home_button"):
    page = "dashboard"

if st.sidebar.button("Go to Flight Overview", key="overview_button"):
    page = "overview"

if page == "overview":
    st.markdown("<h1 style='text-align: center;'>Welcome</h1>", unsafe_allow_html=True)

    fig_dep_to_arr = p1.plot_flight_to_airport(selected_departure, faa_list)
    st.plotly_chart(fig_dep_to_arr, use_container_width=True)
else:
    # Titel
    st.markdown('<div class="title">Flight Statistics Dashboard</div>', unsafe_allow_html=True)

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

    def show_globalmap():
        fig = px.scatter_geo(
            data_frame=df_airports, 
            lat='lat', 
            lon='lon', 
            color='tzone', 
        )
        return fig

    st.subheader("Global Flight Map")
    fig_globalmap = show_globalmap()
    st.plotly_chart(fig_globalmap, use_container_width=True)

conn.close()


