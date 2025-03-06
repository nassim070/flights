def is_usa(faa):
    for x in faa:
        row = df[df["faa"] == x]
        is_usa = row["lat"].between(24, 50) & row["lon"].between(-125, -66)

        if (is_usa.any() == False):
            return False

    
    return True

def plot_flight_to_airport(faa_list):
    nyc_lat, nyc_lon = df[df["faa"] == "JFK"]["lat"].values[0], df[df["faa"] == "JFK"]["lon"].values[0] #JFK

    fig = px.scatter_geo(
        df[df["faa"].isin(["JFK", faa_list])], lat="lat", lon="lon", hover_name="name",
        title=f"Flight from New York to Multiple Airports"
    )

    for faa in faa_list:
        airport = df[df["faa"] == faa]

        if not airport.empty:
            airport_lat = airport["lat"].values[0]
            airport_lon = airport["lon"].values[0]
            airport_name = airport["name"].values[0]

            fig.add_trace(go.Scattergeo(
                lat=[nyc_lat, airport_lat],
                lon=[nyc_lon, airport_lon],
                mode="lines",
                line=dict(width=2, color="red")
            ))

            fig.add_trace(go.Scattergeo(
                lat=[airport_lat],
                lon=[airport_lon],
                mode="markers",
                marker=dict(size=8, color="blue"),
                text=[airport_name]
            ))

    fig.add_trace(go.Scattergeo(
                lat=[nyc_lat],
                lon=[nyc_lon],
                mode="markers",
                marker=dict(size=8, color="green"),
                text=[airport_name]
            ))

    if (is_usa(faa_list)):
        fig.update_layout(geo_scope = 'usa')

    fig.show()

faa = ["AUW", "AVX", "BEC", "FCA", "SOW", "TZR"]

plot_flight_to_airport(faa)

def euclidean_distance_plot():
    jfk = df[df["faa"] == "JFK"].iloc[0]
    jfk_lat, jfk_lon = jfk["lat"], jfk["lon"]

    df["distance"] = np.sqrt((df["lat"] - jfk_lat) ** 2 + (df["lon"] - jfk_lon) ** 2)

    # Plot the distribution of distances
    plt.figure(figsize=(10, 5))
    plt.hist(df["distance"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Euclidean Distance from JFK")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Euclidean Distances from JFK Airport")
    plt.grid(True)
    plt.show()

def geodesic_distance_plot():
    R = 6371.0

    # JFK Airport coordinates (from the dataset or known values)
    jfk = df[df["faa"] == "JFK"].iloc[0]
    jfk_lat, jfk_lon = np.radians(jfk["lat"]), np.radians(jfk["lon"])

    # Convert latitude and longitude to radians
    df["lat_rad"], df["lon_rad"] = np.radians(df["lat"]), np.radians(df["lon"])

    # Compute differences in latitude and longitude
    delta_lat = df["lat_rad"] - jfk_lat
    delta_lon = df["lon_rad"] - jfk_lon

    # Compute the midpoint latitude
    phi_m = (df["lat_rad"] + jfk_lat) / 2

    # Compute geodesic distance using the given formula
    df["distance"] = R * np.sqrt(
        (2 * np.sin(delta_lat / 2))**2 + (2 * np.cos(phi_m) * np.sin(delta_lon / 2))**2
    )

    # Plot the distribution of distances
    plt.figure(figsize=(10, 5))
    plt.hist(df["distance"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Geodesic Distance from JFK (km)")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Geodesic Distances from JFK Airport")
    plt.grid(True)
    plt.show()

def analyse_time_zones():
    # Analyze time zones
    timezone_counts = df["tz"].value_counts()

    # Plot time zone distribution
    plt.figure(figsize=(12, 6))
    plt.bar(timezone_counts.index, timezone_counts.values, color="royalblue")
    plt.xlabel("Time Zone")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Airports by Time Zone")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def analysis_airport_altitudes():
    plt.figure(figsize=(10, 5))
    plt.hist(df["alt"], bins=30, edgecolor='black', alpha=0.7, color="teal")
    plt.xlabel("Altitude (ft)")
    plt.ylabel("Number of Airports")
    plt.title("Distribution of Airport Altitudes")
    plt.grid(True)
    plt.show()
