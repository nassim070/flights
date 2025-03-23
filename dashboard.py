import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from scripts import part1 as p1  
from scripts import statistics as stats

st.set_page_config(layout="wide", page_title="Flight Statistics Dashboard", page_icon=":airplane:")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
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
    .em9zgd02 {
        background-color: #FFA500;
        color: white;
        margin: 0 auto;
        display: block;
    }
    .em9zgd02:hover {
        background-color: white;
        color: #FFA500;
    }
    .em9zgd02:focus:not(:active) {
        background-color: #FFA500;
        color: white;
        margin: 0 auto;
        display: block;
    }
    .em9zgd02:focus:not(:active):hover {
        background-color: white;
        color: #FFA500;
    }
    
    """,
    unsafe_allow_html=True,
)

conn = sqlite3.connect("data/flights_database.db")

@st.cache_data
def get_airports():
    df = pd.read_sql_query("SELECT * FROM airports;", conn)
    return df

@st.cache_data
def get_flights():
    df = pd.read_sql_query("SELECT * FROM flights;", conn)
    return df

@st.cache_data
def cached_get_number_of_flights(df, dep, arr, airline=None):
    return stats.get_number_of_flights(df, dep, arr, airline)

@st.cache_data
def cached_get_average_dep_delay(df, dep, arr, airline=None):
    return stats.get_average_dep_delay(df, dep, arr, airline)

@st.cache_data
def cached_get_percentage_delayed_flights(df, dep, arr, airline=None):
    return stats.get_percentage_delayed_flights(df, dep, arr, airline)

@st.cache_data
def cached_get_percentage_on_time_arrivals(df, dep, arr, airline=None):
    return stats.get_percentage_on_time_arrivals(df, dep, arr, airline)

@st.cache_data
def cached_plot_flight_to_airport(dep, faa_list):
    return p1.plot_flight_to_airport(dep, faa_list)

@st.cache_data
def cached_show_globalmap():
    return p1.show_globalmap()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# Sidebar navigation
if st.sidebar.button("Home", key="home_button"):
    st.session_state.page = "dashboard"

df_airports = get_airports()
df_flights = get_flights()

airports_arr = df_airports['faa'].dropna().unique().tolist()
airports_dep = ['JFK', 'LGA', 'EWR']

selected_departure = st.sidebar.selectbox("Choose Departure Airport", airports_dep)
selected_destination = st.sidebar.selectbox("Choose Arrival Airport", airports_arr)
faa_list = [selected_destination]

if st.session_state.page == "dashboard":
    st.sidebar.button("Go to Flight Overview", key="overview_button", disabled=True if st.session_state.page == "overview" else False, on_click=lambda: st.session_state.update(page="overview"))

if st.session_state.page == "overview":
    if not df_flights[(df_flights["origin"] == selected_departure) & (df_flights["dest"] == selected_destination)].empty:
        airlines = df_flights[(df_flights["origin"] == selected_departure) & (df_flights["dest"] == selected_destination)]["carrier"].unique().tolist()
        airlines.insert(0, "All")
        selected_airline = st.sidebar.selectbox("Choose Airline", airlines)

        st.markdown(f"<h1 style='text-align: center;'>Statistics of flights from {selected_departure} to {selected_destination}{' by ' + selected_airline if selected_airline != 'All' else ''}</h1>", unsafe_allow_html=True)

        flight_map = cached_plot_flight_to_airport(selected_departure, faa_list).update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0}, height = 300)
        st.plotly_chart(flight_map, use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            number_of_flights = cached_get_number_of_flights(df_flights, selected_departure, selected_destination, None if selected_airline == "All" else selected_airline)
            st.markdown(f'<div class="metric-box orange-box"><h3>Total Flights</h3><h1>{number_of_flights}</h1></div>', unsafe_allow_html=True)
        
        with col6:
            distance = stats.get_distance(df_flights, selected_departure, selected_destination)
            st.markdown(f'<div class="metric-box orange-box"><h3>Distance</h3><h1>{distance}</h1></div>', unsafe_allow_html=True)

        col7, col8, col9 = st.columns(3)
        with col7:
            avg_delay = cached_get_average_dep_delay(df_flights, selected_departure, selected_destination, None if selected_airline == "All" else selected_airline)
            st.markdown(f'<div class="metric-box black-box"><h3>Average Delay</h3><h2>{avg_delay}</h2></div>', unsafe_allow_html=True)
        
        with col8:
            percent_delayed = cached_get_percentage_delayed_flights(df_flights, selected_departure, selected_destination, None if selected_airline == "All" else selected_airline)
            st.markdown(f'<div class="metric-box black-box"><h3>Percentage of Delay</h3><h1>{percent_delayed}</h1></div>', unsafe_allow_html=True)
        
        with col9:
            percent_on_time = cached_get_percentage_on_time_arrivals(df_flights, selected_departure, selected_destination, None if selected_airline == "All" else selected_airline)
            st.markdown(f'<div class="metric-box black-box"><h3>Percentage of Flights on Time</h3><h1>{percent_on_time}</h1></div>', unsafe_allow_html=True)

        col10, col11 = st.columns(2)
        df_weather = pd.read_sql_query("SELECT * FROM weather;", conn)
        if selected_airline == "All":
            fig_delays_per_day = stats.plot_delays_per_day(df_flights, selected_departure, selected_destination)
            fig_delays_vs_windspeed = stats.plot_delay_vs_windspeed(df_flights, df_weather, selected_departure, selected_destination)
        else:
            fig_delays_per_day = stats.plot_delays_per_day(df_flights, selected_departure, selected_destination, selected_airline)
            fig_delays_vs_windspeed = stats.plot_delay_vs_windspeed(df_flights, df_weather, selected_departure, selected_destination, selected_airline)

        with col10:
            st.plotly_chart(fig_delays_per_day, use_container_width=True)

        with col11:
            st.plotly_chart(fig_delays_vs_windspeed, use_container_width=True)
        
    else:
        st.markdown(f"<h1 style='text-align: center;'>Error: no flight from {selected_departure} to {selected_destination}</h1>", unsafe_allow_html=True)
else:
    st.markdown('<div class="title">Flight Statistics Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="metric-box orange-box"><h3>Total Flights</h3><h1>{len(df_flights):,}</h1></div>', unsafe_allow_html=True)
    with col2:
        total_flight_hours = df_flights['air_time'].sum() / 60
        st.markdown(f'<div class="metric-box orange-box"><h3>Total Flight Hours</h3><h1>{total_flight_hours:,.0f}</h1></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        delayed_flights = len(df_flights[df_flights['dep_delay'] > 0])
        st.markdown(f'<div class="metric-box black-box"><h3>Percentage Delayed Flights</h3><h1>{(delayed_flights / len(df_flights)) * 100:.2f}%</h1></div>', unsafe_allow_html=True)
    with col4:
        early_flights = len(df_flights[df_flights['arr_delay'] <= 0])
        st.markdown(f'<div class="metric-box black-box"><h3>Percentage Flights on Time</h3><h1>{(early_flights / len(df_flights)) * 100:.2f}%</h1></div>', unsafe_allow_html=True)
    
    st.subheader("Global Flight Map")
    st.plotly_chart(cached_show_globalmap(), use_container_width=True)

conn.close()