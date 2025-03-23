from scripts import part1 as p1
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/flights_database.db")
cursor = conn.cursor()

def compare_distances():
    df = pd.read_sql_query("SELECT distance FROM flights;", conn)

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

     return df


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


def aircraft_usage_by_route(origin, destination, df, airline=None):
    if airline:
        flights = df[(df["origin"] == origin) & (df["dest"] == destination) & (df["carrier"] == airline)]
    else:
        flights = df[(df["origin"] == origin) & (df["dest"] == destination)]

    aircraft_usage = flights["tailnum"].value_counts().head(5)

    return aircraft_usage


def average_departure_delay_per_airline():
    query = """
        SELECT a.name, AVG(f.dep_delay) AS avg_delay
        FROM flights f
        JOIN airlines a ON f.carrier = a.carrier
        GROUP BY a.name
        ORDER BY avg_delay DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()

    airlines, avg_delays = zip(*results)

    plt.figure(figsize=(12, 10))
    plt.bar(airlines, avg_delays, color="skyblue")
    plt.ylabel("Average Departure Delay (minutes)")
    plt.xlabel("Airline")
    plt.title("Average Departure Delay per Airline")
    plt.xticks(rotation=90)  
    plt.subplots_adjust(bottom=0.3)
    plt.show()

def delayed_flights_to_destination(start_month, end_month, destination):
    query = """
        SELECT COUNT(*) 
        FROM flights
        WHERE dest = ? 
        AND month BETWEEN ? AND ?
        AND dep_delay > 0;
    """

    cursor = conn.cursor()
    cursor.execute(query, (destination, start_month, end_month))

    result = cursor.fetchone()
    return result[0] if result else 0

#delayed_flights_count = delayed_flights_to_destination(1, 4, 'HNL')
#print(f"Number of delayed flights: {delayed_flights_count}")

def top_manufacturers_for_destination(destination):
    flights_query = """
    SELECT * FROM flights WHERE dest = ?
    """
    flights_df = pd.read_sql_query(flights_query, conn, params=(destination,))
    
    planes_query = """
    SELECT * FROM planes
    """
    planes_df = pd.read_sql_query(planes_query, conn)
    
    merged_df = pd.merge(flights_df, planes_df, on='tailnum', how='inner')
    
    manufacturer_counts = merged_df['manufacturer'].value_counts().head(5)

    return manufacturer_counts

#print(top_manufacturers_for_destination("SMF"))

def analyze_distance_vs_delay():
    query = """
        SELECT distance, arr_delay
        FROM flights
        WHERE distance IS NOT NULL AND arr_delay IS NOT NULL;
    """
    df = pd.read_sql_query(query, conn)

    plt.figure(figsize=(10, 6))
    plt.scatter(df['arr_delay'], df['distance'], alpha=0.5, color='b')
    plt.title('Relationship between Arrival Delay and Distance')
    plt.xlabel('Arrival Delay (minutes)')
    plt.ylabel('Distance (miles)')
    plt.grid(True)
    plt.show()

    correlation = df['arr_delay'].corr(df['distance'])
    print(f"Correlation between arrival delay and distance: {correlation:.2f}")

#analyze_distance_vs_delay()

def update_plane_speeds():
    query = """
        SELECT f.tailnum, f.distance, f.air_time, p.model
        FROM flights f
        JOIN planes p ON f.tailnum = p.tailnum
        WHERE f.air_time > 0 AND f.distance IS NOT NULL;
    """
    df = pd.read_sql_query(query, conn)

    df["speed"] = df["distance"] / df["air_time"]

    avg_speeds = df.groupby("model")["speed"].mean().reset_index()

    cursor = conn.cursor()
    for _, row in avg_speeds.iterrows():
        update_query = """
            UPDATE planes
            SET speed = ?
            WHERE model = ?;
        """
        cursor.execute(update_query, (row["speed"], row["model"]))

    conn.commit()
    print("Plane speeds updated successfully.")

#update_plane_speeds()

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Bereken de richting (bearing) van de vlucht tussen twee locaties."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1

    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)

    initial_bearing = np.arctan2(x, y)
    compass_bearing = (np.degrees(initial_bearing) + 360) % 360  

    return round(compass_bearing, 2)

def get_flight_directions():

    query = """
        SELECT f.origin, f.dest, a1.lat AS origin_lat, a1.lon AS origin_lon, 
               a2.lat AS dest_lat, a2.lon AS dest_lon
        FROM flights f
        JOIN airports a1 ON f.origin = a1.faa
        JOIN airports a2 ON f.dest = a2.faa
        WHERE f.origin IN ('JFK', 'LGA', 'EWR');
    """
    
    df = pd.read_sql_query(query, conn)

    df["bearing"] = df.apply(lambda row: calculate_bearing(row["origin_lat"], row["origin_lon"], 
                                                            row["dest_lat"], row["dest_lon"]), axis=1)
    
    return df[["origin", "dest", "bearing"]]

#print(get_flight_directions())


def compute_inner_product(year, month, day, flight, hour, minute):
    flight_query = """
    SELECT
    origin_airports.lat AS origin_lat,
    origin_airports.lon AS origin_lon,
    dest_airports.lat AS dest_lat,
    dest_airports.lon AS dest_lon,
    weather.wind_speed,
    weather.wind_dir
    FROM
        flights
    JOIN
        airports AS origin_airports ON flights.origin = origin_airports.faa
    JOIN
        airports AS dest_airports ON flights.dest = dest_airports.faa
    JOIN
        weather ON flights.origin = weather.origin
           AND flights.year = weather.year
           AND flights.month = weather.month
           AND flights.day = weather.day
           AND flights.hour = weather.hour
    WHERE
        flights.year = ?
        AND flights.month = ?
        AND flights.day = ?
        AND flights.flight = ?
        AND flights.hour = ?
        AND flights.minute = ?;
    """
    
    flight_data = pd.read_sql_query(flight_query, conn, params=(year, month, day, flight, hour, minute))
    
    origin_lat, origin_lon = np.radians(flight_data["origin_lat"].values[0]), np.radians(flight_data["origin_lon"].values[0])
    dest_lat, dest_lon = np.radians(flight_data["dest_lat"].values[0]), np.radians(flight_data["dest_lon"].values[0])
    
    delta_lat = dest_lat - origin_lat
    delta_lon = dest_lon - origin_lon

    norm = np.sqrt(delta_lat**2 + delta_lon**2)
    flight_direction = np.array([delta_lat / norm, delta_lon / norm]) if norm != 0 else np.array([0, 0])
    
    wind_speed = flight_data["wind_speed"].values[0]
    wind_dir = np.radians(flight_data["wind_dir"].values[0])
    
    wind_vector = np.array([wind_speed * np.cos(wind_dir), wind_speed * np.sin(wind_dir)])
    
    inner_product = np.dot(flight_direction, wind_vector)
    
    return inner_product

#print(compute_inner_product(2023, 1, 1, 628, 20, 38))

def visualize_inner_product_vs_air_time():
    query = """
    SELECT
        flights.flight,
        flights.air_time,
        airports_origin.lat AS origin_lat,
        airports_origin.lon AS origin_lon,
        airports_dest.lat AS dest_lat,
        airports_dest.lon AS dest_lon,
        weather.wind_speed,
        weather.wind_dir
    FROM flights
    JOIN airports AS airports_origin ON flights.origin = airports_origin.faa
    JOIN airports AS airports_dest ON flights.dest = airports_dest.faa
    JOIN weather ON flights.origin = weather.origin
        AND flights.year = weather.year
        AND flights.month = weather.month
        AND flights.day = weather.day
        AND flights.hour = weather.hour
    WHERE flights.air_time IS NOT NULL;
    """

    df = pd.read_sql_query(query, conn)

    inner_products = []
    air_times = []

    for _, row in df.iterrows():
       
        origin_lat, origin_lon = np.radians(row["origin_lat"]), np.radians(row["origin_lon"])
        dest_lat, dest_lon = np.radians(row["dest_lat"]), np.radians(row["dest_lon"])

        delta_lat = dest_lat - origin_lat
        delta_lon = dest_lon - origin_lon

        norm = np.sqrt(delta_lat*2 + delta_lon*2)
        flight_direction = np.array([delta_lat / norm, delta_lon / norm]) if norm != 0 else np.array([0, 0])

        wind_speed = row["wind_speed"]
        wind_dir = np.radians(row["wind_dir"])
        wind_vector = np.array([wind_speed * np.cos(wind_dir), wind_speed * np.sin(wind_dir)])

        inner_product = np.dot(flight_direction, wind_vector)

        inner_products.append(inner_product)
        air_times.append(row["air_time"])

    plot_df = pd.DataFrame({"Inner Product": inner_products, "Air Time": air_times})
    correlation = plot_df["Inner Product"].corr(plot_df["Air Time"])
    print(f"Correlation between wind effect (inner product) and air time: {correlation:.2f}")

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        plot_df["Inner Product"], plot_df["Air Time"],
        c=np.sign(plot_df["Inner Product"]), cmap="bwr", alpha=0.7
    )
    plt.colorbar(scatter, label="Wind Effect (-1: Headwind, 1: Tailwind)")
    plt.axvline(0, color="black", linestyle="--", alpha=0.7)  
    plt.xlabel("Inner Product (Wind Effect)")
    plt.ylabel("Air Time (minutes)")
    plt.title(f"Relationship Between Wind Effect and Air Time (Correlation: {correlation:.2f})")
    plt.grid(True)
    plt.show()


conn.close()