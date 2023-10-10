# -*- coding: utf-8 -*-

#Imports
import numpy as np
import pandas as pd
import math
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sodapy import Socrata
from io import StringIO
import datetime as dt
import meteomatics.api as api

!pip install sodapy

!pip install requests

!pip install meteomatics

"""## API Connections

### NASA FIRMS

Connecting the database on real time fire data from NASA FIRMS.

Instructions: input information below based on the parameters from the last active session on the FIRMS API.

Access to the API key: [API Key](https://https://firms.modaps.eosdis.nasa.gov/api/)
"""

url = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv'

params = {
    'api_key': api_key,
    'source': 'VIIRS_NOAA20_NRT',  # Example latitude (replace with your own)
    'country_code': 'USA',  # Example longitude (replace with your own)
    'day_range': '7',  # Example start date in YYYYMMDD format
    'date': '2023-10-07'    # Example end date in YYYYMMDD format
}

response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Print the first few lines of the CSV data
      # Adjust the number to display more or fewer characters

    try:
        # Parse the CSV data into a Pandas DataFrame
        firms_df = pd.read_csv(StringIO(response.text))

        # Print the DataFrame
        print(firms_df.head())
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}")

firms_df

"""## Streetlights Data - Socrata

Community-based database of streetlights in San Francisco.

**Edits to original:** addition of two columns on latitude and longitude, extracted from object contained in the feature 'point'.
"""

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.sfgov.org", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.sfgov.org,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("6tt8-ugnj", limit=2000)

# Convert to pandas DataFrame
streetlights_df = pd.DataFrame.from_records(results)
streetlights_df[['latitude', 'longitude']] = streetlights_df['point'].apply(lambda x: pd.Series([x['latitude'], x['longitude']]))

"""## Meteomatics - Live Weather Information

Default Time Frame: 1 day, 25 hour intevrals, to obtain the daily wind speed and precipitation values
"""

# Authentication
username = 'USERNAME'
password = 'PASSWORD'

# Params
coordinates = [(37.7790262, -122.419906)] # filler coordinates of San Francisco to test the database, later the API will be called for every coordinate of street lights
parameters = ['t_2m:C', 'msl_pressure:hPa', 'precip_24h:mm', 'wind_speed_10m:ms', 'weather_symbol_24h:idx']
model = 'mix'
startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
enddate = startdate + dt.timedelta(days=1)
interval = dt.timedelta(hours=25)

# Call to API
meteomatics_df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password, model=model)
wind_speed = meteomatics_df['wind_speed_10m:ms']
precipitation = meteomatics_df['precip_24h:mm']

meteomatics_df

"""## Distance Calculation and Management

Calculating distance based on latitude and longitude considering the Haversine Distance formula.
"""

from math import radians, sin, cos, sqrt, atan2, inf, e, log

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the Earth's surface.

    Parameters:
    - lat1, lon1: Latitude and longitude of point 1 in degrees
    - lat2, lon2: Latitude and longitude of point 2 in degrees

    Returns:
    - Distance in kilometers
    """
    # Radius of the Earth in Km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in Km
    distance = R * c

    return round(distance)

"""## Coordinates to Radians

### Street Lights
"""

# Convert latitude and longitude columns to float, handle NaN values
streetlights_df['latitude'] = pd.to_numeric(streetlights_df['latitude'], errors='coerce')
streetlights_df['longitude'] = pd.to_numeric(streetlights_df['longitude'], errors='coerce')

# Drop rows with NaN values
streetlights_df = streetlights_df.dropna(subset=['latitude', 'longitude'])

# Convert latitude and longitude to radians element-wise
streetlights_df['latitude_rad'] = streetlights_df['latitude'].apply(radians)
streetlights_df['longitude_rad'] = streetlights_df['longitude'].apply(radians)

"""### FIRMS Active Fire Data"""

# Convert latitude and longitude columns to float, handle NaN values
firms_df['latitude'] = pd.to_numeric(firms_df['latitude'], errors='coerce')
firms_df['longitude'] = pd.to_numeric(firms_df['longitude'], errors='coerce')

# Drop rows with NaN values
firms_df = firms_df.dropna(subset=['latitude', 'longitude'])

# Convert latitude and longitude to radians element-wise
firms_df['latitude_rad'] = firms_df['latitude'].apply(radians)
firms_df['longitude_rad'] = firms_df['longitude'].apply(radians)

firms_df

"""### Including id columns"""

# Including the streetlight_id feature
streetlights_df['streetlight_id'] = range(len(streetlights_df))

# Including the fire_id feature
firms_df['fire_id'] = range(len(firms_df))

"""## Functions for Danger Zones

### Z-Value
"""

def z_value(distance_fire_street_lights, wind_speed, precipitation):
  """
    Calculate a fire danger score, here called the z-value, based on the given parameters.

    Parameters:
    - distance_fire_street_lights (float): Distance between fire and street lights in km.
    - wind_speed (float): Wind speed. in m/s
    - precipitation (float): Precipitation in mm.

    Returns:
    - float: Calculated 'z' value rounded to two decimal places.
    """
  z = 1000*(((2**(1/distance_fire_street_lights) * (1 + wind_speed))/(math.log(math.e + precipitation))-1))
  return round(z, 2)

z_value()

"""### Danger Level"""

def danger_level(z_value):
  if z_value < 10:
    return 1
  elif z_value >= 10 and z_value < 14:
    return 2
  elif z_value >= 14 and z_value < 24:
    return 3
  elif z_value >= 24 and z_value < 70:
    return 4
  elif z_value >= 70:
    return 5

"""## [FINAL RESULT] Streetlight Database complemented with Danger Level Data

**How does this connect with other parts of A-Prometheus?** This database enables the construction of streetlight objects which can later be manipulated through the MESH networks. In other words, analysis was meant to complement the current database on streetlight lamps and it is supposed to demosntrate how the defintion of danger levels based on factors such as proximity to closest fire and real time weather data can be made possible.

Although San Francisco is a city without frequent fire reports, it was selected for this test given its open-sourced and comprehensive databse of streetlights. It is meant to introduce how this data analysis can be used in other scales.
"""

# Initialize variables and data structures
data = {}
requests = 0
smallest_distances = []
fire_ids = []
streetlight_ids = []
smallest_distance = math.inf

# Define meteomatics_df outside of the loop
meteomatics_df = None

# Loop over streetlights and fire incidents
for lat_rad_sl, lat_sl, long_rad_sl, long_sl, streetlight_id in zip(streetlights_df['latitude_rad'], streetlights_df['latitude'], streetlights_df['longitude_rad'], streetlights_df['longitude'], streetlights_df['streetlight_id']):

  # Increment the request counter, considering API limitations
  requests += 1

  # Check if the number of requests is within the limit
  if requests < 50:
    meteomatics_df = api.query_time_series([(lat_sl, long_sl)], startdate, enddate, interval, parameters, username, password, model=model)

  # Loop over fire incidents
  for lat_rad_fire, long_rad_fire, fire_id in zip(firms_df['latitude_rad'], firms_df['longitude_rad'], firms_df['fire_id']):

    # Calculate the Haversine distance between streetlight and fire incident
    curr_distance = haversine_distance(lat_rad_sl, long_rad_sl, lat_rad_fire, long_rad_fire)

    # Update the smallest distance if the current distance is smaller
    if curr_distance > 0 and curr_distance < smallest_distance:
      smallest_distance = curr_distance

  # Append data to lists
  smallest_distances.append(smallest_distance)
  fire_ids.append(fire_id)
  streetlight_ids.append(streetlight_id)

  # Reset smallest distance for the next streetlight
  smallest_distance = math.inf

# Create a dictionary to store the data
data['smallest_distances:km'] = smallest_distances
data['fire_ids'] = fire_ids
data['streetlight_id'] = streetlight_ids

# Sample wind speed and precipitation data from the meteomatics dataframe
data['wind_speed_10m:ms'] = meteomatics_df['wind_speed_10m:ms'].sample(n=len(streetlights_df), replace=True)
data['precipitation_24h:mm'] = meteomatics_df['precip_24h:mm'].sample(n=len(streetlights_df), replace=True)

# Create a Pandas DataFrame from the dictionary
intermediate_df = pd.DataFrame(data)

# Dropping previous indexes from the Meteomatics database
intermediate_df = intermediate_df.reset_index(drop=True)
intermediate_df

#Including new parameters to the intermediate database
intermediate_df['z_value'] = intermediate_df.apply(lambda row: z_value(row['smallest_distances:km'], row['precipitation_24h:mm'], row['precipitation_24h:mm']), axis = 1)

intermediate_df

intermediate_df['danger_level'] = intermediate_df.apply(lambda row: danger_level(row['z_value']), axis = 1)
intermediate_df

streetlights_df

streetlights_with_fire_weather_data = streetlights_df.merge(intermediate_df, left_on='streetlight_id', right_on='streetlight_id')

streetlights_with_fire_weather_data
