import sqlite3
import pandas as pd

conn = sqlite3.connect("data/flights_database.db")

def clean_flights_data():

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

    duplicates = df[df.duplicated(keep=False)]
    print(f"\nNumber of exact duplicates found: {len(duplicates)}")

    df = df.drop_duplicates()

    print("\nCleaning completed. Remaining rows:", len(df))

    return df

#print(clean_flights_data())


def convert_to_datetime(df):
    time_columns = ['sched_dep_time', 'sched_arr_time', 'dep_time', 'arr_time']
    
    for col in time_columns:
        df[col] = df[col].astype(str).str.zfill(4)
        df[col] = pd.to_datetime(df[col], format='%H%M', errors='coerce').dt.time

    return df

#df_cleaned = clean_flights_data()
#df_convert = convert_to_datetime(df_cleaned)
#print(df_convert)

def check_and_fix_flights():
    query = "SELECT flight, sched_dep_time, dep_time, sched_arr_time, arr_time, air_time, distance FROM flights;"
    df = pd.read_sql_query(query, conn)

    inconsistencies = []

    incorrect_dep_times = df[df["dep_time"] < df["sched_dep_time"]]
    if not incorrect_dep_times.empty:
        inconsistencies.append("Some flights have departure times earlier than scheduled.")
        df.loc[df["dep_time"] < df["sched_dep_time"], "dep_time"] = df["sched_dep_time"]

    incorrect_arrival_times = df[df["arr_time"] < df["dep_time"]]
    if not incorrect_arrival_times.empty:
        inconsistencies.append("Some flights have arrival times earlier than departure times.")
        df.loc[df["arr_time"] < df["dep_time"], "arr_time"] = df["dep_time"] + df["air_time"]

    speed_threshold = 8
    incorrect_air_times = df[df["air_time"] < df["distance"] / speed_threshold]
    if not incorrect_air_times.empty:
        inconsistencies.append("Some flights have unrealistically short air times.")
        df.loc[df["air_time"] < df["distance"] / speed_threshold, "air_time"] = df["distance"] / speed_threshold

    df["dep_time"] = df["dep_time"].fillna(df["sched_dep_time"])
    df["arr_time"] = df["arr_time"].fillna(df["sched_arr_time"])

    if inconsistencies:
        print("\n".join(inconsistencies))
        print("Issues have been corrected.")
    else:
        print("All flight data is consistent.")

    return df

#cleaned_flights = check_and_fix_flights()