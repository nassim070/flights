import part1 as p1
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/flights_database.db")
cursor = conn.cursor()

def compare_distances():
    df = pd.read_sql_query("SELECT distance FROM flights;", conn)

    conn.close()

    plt.figure(figsize=(10, 5))
    plt.hist(df["distance"], bins=30, edgecolor="black", alpha=0.7, color="teal")
    plt.xlabel("Distance")
    plt.ylabel("Frequency")
    plt.title("Distribution fo distances")
    plt.grid(True)
    plt.show()

    p1.geodesic_distance_plot()

def depart_from_NYC (origin):
     df = pd.read_sql_query(f"SELECT * FROM flights WHERE origin = '{origin}';" , conn)

     print(df)


def plot_flights_on_date(month, day, origin):
    df_airports = pd.read_csv("data/airports.csv")
    query = f"""
        SELECT dest 
        FROM flights 
        WHERE origin = '{origin}' 
        AND month = {month} 
        AND day = {day};
    """

    df_flights = pd.read_sql_query(query, conn)

    destinations = df_airports[df_airports["faa"].isin(df_flights["dest"])]

    origin_airport = df_airports[df_airports["faa"] == origin]
    
    origin_lat, origin_lon = origin_airport["lat"].values[0], origin_airport["lon"].values[0]

    fig = px.scatter_geo(
        destinations, lat="lat", lon="lon", hover_name="name",
        title=f"Flights from {origin} on {month}/{day}"
    )

    for _, row in destinations.iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[origin_lat, row["lat"]],
            lon=[origin_lon, row["lon"]],
            mode="lines",
            line=dict(width=2, color="red")
        ))

    fig.add_trace(go.Scattergeo(
        lat=[origin_lat], lon=[origin_lon],
        mode="markers",
        marker=dict(size=8, color="green"),
        text=[origin]
    ))

    fig.show()


def flight_statistics_on_date(month, day, origin):
    query = f"""
        SELECT dest 
        FROM flights 
        WHERE origin = '{origin}' 
        AND month = {month} 
        AND day = {day};
    """

    df_flights = pd.read_sql_query(query, conn)

    total_flights = len(df_flights)
    unique_destinations = df_flights["dest"].nunique()
    most_common_destination = df_flights["dest"].value_counts().idxmax()
    most_common_count = df_flights["dest"].value_counts().max()

    print(f"Flight statistics for {origin} on {month}/{day}:")
    print(f"- Total flights: {total_flights}")
    print(f"- Unique destinations: {unique_destinations}")
    print(f"- Most visited destination: {most_common_destination} ({most_common_count} times)")

    return {
        "total_flights": total_flights,
        "unique_destinations": unique_destinations,
        "most_common_destination": most_common_destination,
        "most_common_count": most_common_count
    }

def aircraft_usage_by_route(origin, destination):
    query = """
        SELECT tailnum, COUNT(*) as count
        FROM flights
        WHERE origin = ? AND dest = ?
        GROUP BY tailnum
        ORDER BY count DESC;
    """

    cursor.execute(query, (origin, destination))
    results = cursor.fetchall()

    tailnum_counts = {row[0]: row[1] for row in results}

    print(f"Aircraft usage from {origin} to {destination}:")
    for tailnum, count in tailnum_counts.items():
        print(f"- {tailnum}: {count} times")

    return tailnum_counts











