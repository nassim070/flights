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
            df[column] = df[column].fillna(median_value)
    df = df.dropna(subset=["tailnum"])

    duplicates = df[df.duplicated(keep=False)]
    print(f"\nNumber of exact duplicates found: {len(duplicates)}")

    df = df.drop_duplicates()

    print("\nCleaning completed. Remaining rows:", len(df))

    conn.close()
    return df

#cleaned_df = clean_flights_data()
