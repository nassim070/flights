import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/flights_database.db")
df = pd.read_sql_query("SELECT * FROM flights;", conn)


def get_number_of_flights(df, dep, arr):
    return len(df[(df["origin"] == dep) & (df["dest"] == arr)])
    

def get_average_dep_delay(df, dep, arr):
    avg_delay = df[(df["origin"] == dep) & (df["dest"] == arr)]["dep_delay"].mean()
    minutes = int(avg_delay)
    seconds = round((avg_delay - minutes) * 60) 

    return f"{minutes} minutes and {seconds} seconds"


def get_percentage_delayed_flights(df, dep, arr):
    delayed_flights = len(df[(df["origin"] == dep) & (df["dest"] == arr) & (df["dep_delay"] > 0)])
    total_flights = get_number_of_flights(df, dep, arr)

    return f"{round((delayed_flights / total_flights) * 100, 1)}%"
    

def get_percentage_on_time_arrivals(df, dep, arr):
    on_time_arrivals = len(df[(df["origin"] == dep) & (df["dest"] == arr) & (df["arr_delay"] <= 0)])
    total_flights = get_number_of_flights(df, dep, arr)

    return f"{round((on_time_arrivals / total_flights) * 100, 1)}%"
    

def get_distance(df, dep, arr):
    return df[(df["origin"] == dep) & (df["dest"] == arr)]["distance"].mean()


#plot the number of delays per day (monday till sunday) from departure airport to arrival airport
def plot_delays_per_day(df, dep, arr):
    df = df[(df["origin"] == dep) & (df["dest"] == arr)]
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    df['day_of_week'] = df['date'].dt.dayofweek

    delayed_flights = df[df['dep_delay'] > 0]

    delays_per_day = delayed_flights.groupby('day_of_week').size()

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    delays_per_day.index = [day_names[i] for i in delays_per_day.index]

    plt.figure(figsize=(10, 6))
    delays_per_day.plot(kind='bar', color='#FFA500')
    plt.title('Number of Delays per Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Delays')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return plt

