import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from scripts import part1 as p1  
from scripts import part4 as p4
from scripts import statistics as stats

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
    .st-emotion-cache-zaw6nw {
        background-color: #FFA500;
        color: white;
        margin: 0 auto;
        display: block;
    }
    .st-emotion-cache-zaw6nw:hover {
        background-color: white;
        color: #FFA500;
    }

    .st-emotion-cache-mtjnbi {
        max-width: 80%;}
    </style>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("Home", key="home_button"):
    page = "dashboard"

conn = sqlite3.connect("data/flights_database.db")

df_airports = pd.read_sql_query("SELECT * FROM airports;", conn)
airports_arr= df_airports['faa'].dropna().unique().tolist()
airports_dep= ['JFK','LGA','EWR']

df_flights = pd.read_sql_query("SELECT * FROM flights;", conn)

selected_departure = st.sidebar.selectbox("Choose Departure Airport", airports_dep)
selected_destination = st.sidebar.selectbox("Choose Arrival Airport", airports_arr)
faa_list = [selected_destination]

def flight_exists(df, dep, arr):
    return not df[(df["origin"] == dep) & (df["dest"] == arr)].empty

page = "dashboard"

if st.sidebar.button("Go to Flight Overview", key="overview_button"):
    page = "overview"

if page == "overview":
    if flight_exists(df_flights, selected_departure, selected_destination):

        st.markdown(f"<h1 style='text-align: center;'>Statistics of flights from {selected_departure} to {selected_destination}</h1>", unsafe_allow_html=True)

        fig_dep_to_arr = p1.plot_flight_to_airport(selected_departure, faa_list)
        st.plotly_chart(fig_dep_to_arr, use_container_width=True)

        col5, col6 = st.columns(2)

        with col5:
            st.markdown(
                f'<div class="metric-box orange-box">'
                f'<h3>Total Flights</h3>'
                f'<h1>{stats.get_number_of_flights(df_flights, selected_departure, selected_destination)}</h1>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col6:
            st.markdown(
                f'<div class="metric-box orange-box">'
                f'<h3>Distance</h3>'
                f'<h1>{stats.get_distance(df_flights, selected_departure, selected_destination)}</h1>'
                f'</div>',
                unsafe_allow_html=True,
            )

        col7, col8, col9 = st.columns(3)

        with col7:
            st.markdown(
                f'<div class="metric-box black-box">'
                f'<h3>Average Delay</h3>'
                f'<h2>{stats.get_average_dep_delay(df_flights, selected_departure, selected_destination)}</h2>'
                f'</div>',
                unsafe_allow_html=True,
            )
        
        with col8:
            st.markdown(
                f'<div class="metric-box black-box">'
                f'<h3>Percentage of Delay</h3>'
                f'<h1>{stats.get_percentage_delayed_flights(df_flights, selected_departure, selected_destination)}</h1>'
                f'</div>',
                unsafe_allow_html=True,
            )
        
        with col9:
            st.markdown(
                f'<div class="metric-box black-box">'
                f'<h3>Percentage of Flights on Time</h3>'
                f'<h1>{stats.get_percentage_on_time_arrivals(df_flights, selected_departure, selected_destination)}</h1>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(f"<h1 style='text-align: center;'>Error: no flight from {selected_departure} to {selected_destination}</h1>", unsafe_allow_html=True)

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
        early_flights = df_flights[df_flights['arr_delay'] <= 0]
        percentage_early = (len(early_flights) / total_flights) * 100
        st.markdown(
            f'<div class="metric-box black-box">'
            f'<h3>Percentage Flights on Time</h3>'
            f'<h1>{percentage_early:.2f}%</h1>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.subheader("Global Flight Map")
    fig_globalmap = p1.show_globalmap()
    st.plotly_chart(fig_globalmap, use_container_width=True)

conn.close()