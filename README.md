# Flight Information Analysis

This project visualizes and analyzes airport data from airports.csv using Python and various libraries such as Pandas, Plotly, and Matplotlib.

## Features
- World map visualization of airports

- USA-only map with altitude-based color coding

- Plot flights from JFK airport to multiple airports

- Euclidean and geodesic distance calculations from JFK airport

- Time zone distribution analysis

- Airport altitude distribution analysis

## Features
1. **World Map of Airports:**

    - A scatter plot is generated using Plotly to visualize all airports in the dataset.

    - Airports are color-coded based on their time zone.

2. **USA Map of Airports:**

    - A second scatter plot is created to show only airports within the USA.

    - Airports are color-coded by their altitude.

3. **Flight Route Visualization:**

    - A function is created to plot a flight route from JFK (New York City) to a given airport using its FAA abbreviation.

    - If multiple FAA abbreviations are provided, multiple routes are drawn.

    - If the destination airport is in the USA, the map is restricted to the USA.

4. **Distance Calculations:**

    - Euclidean and geodesic distances from JFK to all other airports are calculated.

    - A histogram is used to show the distribution of distances.

5. **Time Zone Analysis:**

    - A graphical representation of time zones is created to illustrate the relative number of flights to different time zones.

6. **Airport Altitudes:**
    - A graphical representation of altitudes is created to illustrate the relative number of airports to different Altitudes.

