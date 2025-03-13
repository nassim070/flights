import part1 as p1
import matplotlib.pyplot as plt
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





