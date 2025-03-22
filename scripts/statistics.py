import sqlite3
import pandas as pd
import plotly.express as px

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


def plot_delays_per_day(df, dep, arr):
    df_filtered = df[(df["origin"] == dep) & (df["dest"] == arr)].copy()

    df_filtered.loc[:, 'date'] = pd.to_datetime(df_filtered[['year', 'month', 'day']])
    
    df_filtered.loc[:, 'day_of_week'] = df_filtered['date'].dt.dayofweek
    
    delayed_flights = df_filtered[df_filtered['dep_delay'] > 0]
    
    delays_per_day = delayed_flights.groupby('day_of_week').size().reset_index(name='delays')
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    delays_per_day['day_of_week'] = delays_per_day['day_of_week'].map(lambda x: day_names[x])
    
    fig = px.bar(delays_per_day, x='day_of_week', y='delays', 
                 title=f'Number of Delays per Day of the Week ({dep} to {arr})',
                 labels={'day_of_week': 'Day of the Week', 'delays': 'Number of Delays'},
                 text='delays')
    
    fig.update_traces(marker_color='#FFA500', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, 
                      yaxis_gridcolor='lightgray', 
                      yaxis_gridwidth=0.5, 
                      yaxis_showgrid=True,
                      plot_bgcolor='white')
    
    return fig

