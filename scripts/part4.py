import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect("data/flights_database.db")

def clean_and_process_flights_data():
    query = "SELECT * FROM flights;"
    df = pd.read_sql_query(query, conn)
    
    missing_values = df.isnull().sum()
    print("Missing values per column:\n", missing_values)

    for column in df.columns:
        if df[column].dtype == 'object': 
            most_common_value = df[column].mode()[0]
            df[column] = df[column].fillna(most_common_value)
        elif df[column].dtype in ['float64', 'int64']:  
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value).astype(int)

    df = df.dropna(subset=["tailnum"])

    duplicates = df[df.duplicated()]
    print(f"\nNumber of exact duplicates found: {len(duplicates)}")
    df = df.drop_duplicates()

    print("\nCleaning completed. Remaining rows:", len(df))

    time_columns = ['sched_dep_time', 'sched_arr_time', 'dep_time', 'arr_time']
    
    for col in time_columns:
        df[col] = df[col].astype(str).str.zfill(4)
        df[col] = pd.to_datetime(df[col], format='%H%M', errors='coerce').dt.time

    return df


def check_flight_data_consistency(df):
    inconsistent_rows = []
    
    def clean_time(value):
        if pd.isnull(value):
            return None
        value = str(value)
        if ':' in value:
            return datetime.strptime(value, "%H:%M:%S").time()
        elif len(value) == 4 and value.isdigit():
            return datetime.strptime(value, "%H%M").time()
        return None
    
    for index, row in df.iterrows():
        sched_dep = clean_time(row['sched_dep_time'])
        dep = clean_time(row['dep_time']) if pd.notnull(row['dep_time']) else sched_dep
        sched_arr = clean_time(row['sched_arr_time'])
        arr = clean_time(row['arr_time']) if pd.notnull(row['arr_time']) else sched_arr
        
        if not all([sched_dep, dep, sched_arr, arr]):
            continue
        
        dep_datetime = datetime.combine(datetime.today(), dep)
        arr_datetime = datetime.combine(datetime.today(), arr)
        
        calculated_air_time = (arr_datetime - dep_datetime).total_seconds() / 60
        if calculated_air_time < 0:
            calculated_air_time += 1440
        
        if row['air_time'] != calculated_air_time:
            inconsistent_rows.append(index)
            df.at[index, 'air_time'] = calculated_air_time

        inconsistent_delay = []
        calculated_dep_delay = (dep_datetime - datetime.combine(datetime.today(), sched_dep)).total_seconds() / 60
        if calculated_dep_delay < 0:
            calculated_dep_delay += 1440
        
        if row['dep_delay'] != calculated_dep_delay:
            inconsistent_delay.append(index)
            df.at[index, 'dep_delay'] = calculated_dep_delay

        inconsistent_arrival = []
        calculated_arr_delay = (arr_datetime - datetime.combine(datetime.today(), sched_arr)).total_seconds() / 60
        if calculated_arr_delay < 0:
            calculated_arr_delay += 1440
        
        if row['arr_delay'] != calculated_arr_delay:
            inconsistent_arrival.append(index)
            df.at[index, 'arr_delay'] = calculated_arr_delay
    
    if not inconsistent_rows:
        print("All flight data is consistent.")
    else:
        print(f"Total inconsistent rows: {len(inconsistent_rows)}")
        print(f"Total inconsistent delays: {len(inconsistent_delay)}")
        print(f"Total inconsistent arrivals: {len(inconsistent_arrival)}")
    
    return df


def convert_to_local_time(df):
        airports_query = "SELECT faa, tz FROM airports;"
        airports_df = pd.read_sql_query(airports_query, conn)

        airport_timezones = dict(zip(airports_df['faa'], airports_df['tz']))
        local_arrival_times = []

        for index, row in df.iterrows():
            dest = str(row['dest']) if pd.notna(row['dest']) else "UNKNOWN"
            dest_tz = airport_timezones.get(dest, -5)  

            time_diff = dest_tz - (-5)

            if pd.isna(row['arr_time']):
                local_arrival_times.append(None)
                continue

            arr_time = datetime.combine(datetime.today(), row['arr_time'])

            local_arr_time = arr_time + timedelta(hours=time_diff)

            local_arrival_times.append(local_arr_time.time())

        df['local_arr_time'] = local_arrival_times
        return df


def get_final_df():
    return check_flight_data_consistency(clean_and_process_flights_data())
