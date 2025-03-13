# Flight Information Analysis

This project visualizes and analyzes airport data from airports.csv using Python and various libraries such as Pandas, Plotly, and Matplotlib.

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

# Requirements
- Python 3.x
- Pandas
- Plotly
- Matplotlib
- Numpy

# Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/flight-analysis.git
cd flight-analysis
```

2. Install dependencies:
```
pip install pandas plotly matplotlib numpy
```

3. Place the airports.csv file inside the data folder.

# Usage
Run the script:
```
python script.py
```







Test Nassim ff

test noureddine 3