from scripts import part1 as p1
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title("Flights Dashboard ✈️")

# Load sample flights data (replace with your own dataset)
@st.cache_data  # Cache the data for better performance
def load_data():
    # Sample data: You can replace this with your actual dataset
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'Airline': np.random.choice(['Airline A', 'Airline B', 'Airline C'], 100),
        'Origin': np.random.choice(['JFK', 'LAX', 'ORD', 'DFW'], 100),
        'Destination': np.random.choice(['SFO', 'ATL', 'DEN', 'SEA'], 100),
        'Passengers': np.random.randint(50, 200, 100),
        'Delay (mins)': np.random.randint(0, 120, 100)
    })
    return data

# Load the data
flights_data = load_data()

# Create 3 tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Airline Performance", "Delay Analysis"])

# Tab 1: Overview
with tab1:
    st.header("Overview of Flights Data")
    st.write("This tab provides a summary of the flights dataset.")
    
    # Display the raw data
    if st.checkbox("Show raw data"):
        st.write(flights_data)
    
    # Summary statistics
    st.subheader("Summary Statistics")
    st.write(flights_data.describe())
    
    # Number of flights by origin
    st.subheader("Number of Flights by Origin")
    origin_counts = flights_data['Origin'].value_counts()
    st.bar_chart(origin_counts)

# Tab 2: Airline Performance
with tab2:
    st.header("Airline Performance")
    st.write("Analyze the performance of different airlines.")
    
    # Select an airline
    selected_airline = st.selectbox("Select Airline", flights_data['Airline'].unique())
    
    # Filter data for the selected airline
    airline_data = flights_data[flights_data['Airline'] == selected_airline]
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Flights", len(airline_data))
    with col2:
        st.metric("Average Passengers", round(airline_data['Passengers'].mean(), 2))
    
    # Plot passengers over time
    st.subheader(f"Passengers Over Time for {selected_airline}")
    fig, ax = plt.subplots()
    ax.plot(airline_data['Date'], airline_data['Passengers'], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Passengers")
    st.pyplot(fig)

# Tab 3: Delay Analysis
with tab3:
    st.header("Flight Delay Analysis")

