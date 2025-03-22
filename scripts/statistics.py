import sqlite3
import pandas as pd

#conn = sqlite3.connect("data/flights_database.db")
#df = pd.read_sql_query("SELECT * FROM airports;", conn)

def get_number_of_flights(df, dep, arr, conn):
    query = "SELECT COUNT(*) FROM flights WHERE origin = ? AND dest = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (dep  , arr))
    return cursor.fetchone()[0]

def get_average_dep_delay(df, dep, arr, conn):
    query = "SELECT SUM(dep_delay) FROM flights WHERE origin = ? AND dest = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (dep  , arr))
    total_delay = cursor.fetchone()[0]
    
    total_flights = get_number_of_flights(df, dep, arr, conn)

    avg_delay = total_delay / total_flights
    minutes = int(avg_delay)
    seconds = round((avg_delay - minutes) * 60) 

    return f"{minutes} minutes and {seconds} seconds"

def get_percentage_delayed_flights(df, dep, arr, conn):
    query = "SELECT COUNT(*) FROM flights WHERE origin = ? AND dest = ? AND dep_delay > 0;"
    cursor = conn.cursor()
    cursor.execute(query, (dep  , arr))
    delayed_flights = cursor.fetchone()[0]

    total_flights = get_number_of_flights(df, dep, arr, conn)

    return f"{round((delayed_flights / total_flights) * 100, 1)}%"

def get_percentage_on_time_arrivals(df, dep, arr, conn):
    query = "SELECT COUNT(*) FROM flights WHERE origin = ? AND dest = ? AND arr_delay <= 0;"
    cursor = conn.cursor()
    cursor.execute(query, (dep  , arr))
    on_time_flights = cursor.fetchone()[0]

    total_flights = get_number_of_flights(df, dep, arr, conn)

    return f"{round((on_time_flights / total_flights) * 100, 1)}%"

def get_distance(df, dep, arr, conn):
    query = "SELECT distance FROM flights WHERE origin = ? AND dest = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (dep  , arr))

    return f"{cursor.fetchone()[0]} miles"



