# Flight Statistics Dashboard

This repository contains a Streamlit-based dashboard for analyzing flight statistics. The dashboard provides insights into flight data, including delays, distances, and other key metrics. It integrates data from a SQLite database and uses various Python scripts for data processing, visualization, and statistical analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)

## Features

- **Interactive Dashboard**: Built with Streamlit, the dashboard allows users to interactively explore flight data.
- **Flight Statistics**: View total flights, average delays, percentage of delayed flights, and more.
- **Visualizations**: Includes various charts and maps to visualize flight data, such as delay times per hour, delays per day of the week, and global flight maps.
- **Data Processing**: Scripts for cleaning and processing flight data, ensuring consistency and accuracy.
- **Customizable Queries**: Users can filter data by departure and arrival airports, airlines, and specific dates.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nassim070/flights.git
   cd flights
   ```

2. **Install dependencies**:   
    ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
    ```bash
    streamlit run dashboard.py
    ```

## Usage

- **Home Page**: The home page provides an overview of total flights, total flight hours, and percentages of delayed and on-time flights. It also displays a global flight map.
- **Flight Overview**: Users can select departure and arrival airports to view detailed statistics, including average delays, percentage of delayed flights, and top tail numbers.
- **Date Filter**: Users can select a specific date to view flight statistics for that day, including total flights, average departure delay, and percentage of delayed flights.
- **Visualizations**: The dashboard includes various visualizations, such as delay times per hour, delays per day of the week, and average delay per wind speed.

## File Structure

- **`dashboard.py`**: The main Streamlit app file that runs the dashboard.
- **`part1.py`**: Contains functions for generating global and USA flight maps, plotting flights to airports, and analyzing airport data.
- **`part3.py`**: Includes functions for comparing distances, plotting flights on specific dates, and analyzing flight statistics.
- **`part4.py`**: Handles data cleaning, processing, and consistency checks for flight data.
- **`statistics.py`**: Provides statistical functions for calculating flight metrics and generating visualizations.
- **`data/`**: Contains the SQLite database (`flights_database.db`) and CSV files used in the project.