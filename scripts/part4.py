import sqlite3
import pandas as pd

conn = sqlite3.connect("data/flights_database.db")

def clean_flights_data():

    query = "SELECT * FROM flights;"
    df = pd.read_sql_query(query, conn)

    missing_values = df.isnull().sum()
    print("📌 Missing values per column:\n", missing_values)

    for column in df.columns:
        if df[column].dtype == 'object':  # Categorische kolommen
            # Vul ontbrekende categorische waarden in met de meest voorkomende waarde (modus)
            most_common_value = df[column].mode()[0]
            df[column] = df[column].fillna(most_common_value)
        elif df[column].dtype in ['float64', 'int64']:  # Numerieke kolommen
            # Vul ontbrekende numerieke waarden in met de mediaan
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)
    #df = df.dropna(subset=["tailnum"])

   # duplicates = df[df.duplicated(keep=False)]
    #print(f"\n🚨 Number of exact duplicates found: {len(duplicates)}")

   # df = df.drop_duplicates()

    print("\n✅ Cleaning completed. Remaining rows:", len(df))

    conn.close()
    return df

cleaned_df = clean_flights_data()

#Close the original database connection
conn.close()

#Run query1 on cleaned_df
#Create a new in-memory database
conn_new = sqlite3.connect(":memory:")

#Store cleaned DataFrame in the new database
cleaned_df.to_sql("flights", conn_new, index=False, if_exists="replace")

#Query the cleaned data
query1 = """SELECT * FROM flights
            WHERE year = '2023' AND month = '1' AND day = '1' 
            AND carrier = 'F9' AND distance = '950'"""

filtered_df = pd.read_sql_query(query1, conn_new)
print(filtered_df)
