import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/airports.csv')

def show_globalmap():
    map = px.scatter_geo(data_frame=df, lat= 'lat', lon='lon', color='tzone')
    return map


def show_usamap():
    usa_map = px.scatter_geo(data_frame=df, lat= 'lat', lon='lon', color='alt')
    usa_map.update_layout(geo_scope = 'usa')
    return usa_map


def is_usa(faa):
    for x in faa:
        row = df[df["faa"] == x]
        is_usa = row["lat"].between(24, 50) & row["lon"].between(-125, -66)

        if (is_usa.any() == False):
            return False
    
    return True


def plot_flight_to_airport(departure_faa, faa_list):
    departure_airport = df[df["faa"] == departure_faa]

    dep_lat, dep_lon = departure_airport["lat"].values[0], departure_airport["lon"].values[0]

    fig = px.scatter_geo(
        df[df["faa"].isin([departure_faa] + faa_list)], lat="lat", lon="lon", hover_name="name"
    )

    fig.add_trace(go.Scattergeo(
        lat=[dep_lat],
        lon=[dep_lon],
        mode="markers",
        marker=dict(size=8, color="green"),
        text=[departure_faa],
        name=f"Departure: {departure_faa}"
    ))

    for faa in faa_list:
        airport = df[df["faa"] == faa]

        if not airport.empty:
            airport_lat = airport["lat"].values[0]
            airport_lon = airport["lon"].values[0]
            airport_name = airport["name"].values[0]

            fig.add_trace(go.Scattergeo(
                lat=[dep_lat, airport_lat],
                lon=[dep_lon, airport_lon],
                mode="lines",
                line=dict(width=2, color="red"),
                name=f"Flight to {faa}"
            ))

            fig.add_trace(go.Scattergeo(
                lat=[airport_lat],
                lon=[airport_lon],
                mode="markers",
                marker=dict(size=8, color="blue"),
                text=[airport_name],
                name=f"Arrival: {faa}" 
            ))

    if is_usa(faa_list):
        fig.update_layout(geo_scope='usa')

    return fig
    

def euclidean_distance_plot():
    jfk = df[df["faa"] == "JFK"].iloc[0]
    jfk_lat, jfk_lon = jfk["lat"], jfk["lon"]

    df["distance"] = np.sqrt((df["lat"] - jfk_lat) ** 2 + (df["lon"] - jfk_lon) ** 2)

    plt.figure(figsize=(10, 5))
    plt.hist(df["distance"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Euclidean Distance from JFK")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Euclidean Distances from JFK Airport")
    plt.grid(True)
    
    return plt


def geodesic_distance_plot():
    R = 6371.0

    jfk = df[df["faa"] == "JFK"].iloc[0]
    jfk_lat, jfk_lon = np.radians(jfk["lat"]), np.radians(jfk["lon"])

    df["lat_rad"], df["lon_rad"] = np.radians(df["lat"]), np.radians(df["lon"])

    delta_lat = df["lat_rad"] - jfk_lat
    delta_lon = df["lon_rad"] - jfk_lon

    phi_m = (df["lat_rad"] + jfk_lat) / 2

    df["distance"] = R * np.sqrt(
        (2 * np.sin(delta_lat / 2))**2 + (2 * np.cos(phi_m) * np.sin(delta_lon / 2))**2
    )

    plt.figure(figsize=(10, 5))
    plt.hist(df["distance"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Geodesic Distance from JFK (km)")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Geodesic Distances from JFK Airport")
    plt.grid(True)
    
    return plt


def analyse_time_zones():
    timezone_counts = df["tz"].value_counts()

    plt.figure(figsize=(12, 6))
    plt.bar(timezone_counts.index, timezone_counts.values, color="royalblue")
    plt.xlabel("Time Zone")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Airports by Time Zone")
    plt.xticks(rotation=45)
    plt.grid(True)
    
    return plt


def analysis_airport_altitudes():
    plt.figure(figsize=(10, 5))
    plt.hist(df["alt"], bins=30, edgecolor='black', alpha=0.7, color="teal")
    plt.xlabel("Altitude (ft)")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Airport Altitudes")
    plt.grid(True)
    
    return plt