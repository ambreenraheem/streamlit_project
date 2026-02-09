"""
Helper functions for Toronto Bike Share Dashboard

IMPORTANT: This is a template file. You need to replace these placeholder functions
with your actual implementations from your helpers.py file.
"""

import requests
import pandas as pd
from math import radians, cos, sin, asin, sqrt


def query_station_status(station_url):
    """
    Fetch station status data from the API
    
    Args:
        station_url: URL to fetch station status
        
    Returns:
        pandas.DataFrame: DataFrame with station status information
    """
    # TODO: Replace with your actual implementation
    response = requests.get(station_url)
    data = response.json()
    
    # Parse the data and create a DataFrame
    stations = data['data']['stations']
    df = pd.DataFrame(stations)
    
    # Add bike type counts if available
    if 'num_bikes_available_types' in df.columns:
        df['ebike'] = df['num_bikes_available_types'].apply(
            lambda x: x.get('ebike', 0) if isinstance(x, dict) else 0
        )
        df['mechanical'] = df['num_bikes_available_types'].apply(
            lambda x: x.get('mechanical', 0) if isinstance(x, dict) else 0
        )
    else:
        df['ebike'] = 0
        df['mechanical'] = df['num_bikes_available']
    
    return df


def get_station_latlon(latlon_url):
    """
    Fetch station location data from the API
    
    Args:
        latlon_url: URL to fetch station locations
        
    Returns:
        pandas.DataFrame: DataFrame with station latitude and longitude
    """
    # TODO: Replace with your actual implementation
    response = requests.get(latlon_url)
    data = response.json()
    
    stations = data['data']['stations']
    df = pd.DataFrame(stations)
    
    return df[['station_id', 'lat', 'lon']]


def join_latlon(data_df, latlon_df):
    """
    Join station status data with location data
    
    Args:
        data_df: DataFrame with station status
        latlon_df: DataFrame with station locations
        
    Returns:
        pandas.DataFrame: Merged DataFrame
    """
    # TODO: Replace with your actual implementation
    merged = pd.merge(data_df, latlon_df, on='station_id', how='left')
    return merged


def get_marker_color(num_bikes):
    """
    Get marker color based on number of available bikes
    
    Args:
        num_bikes: Number of available bikes
        
    Returns:
        str: Color name
    """
    # TODO: Customize these thresholds if needed
    if num_bikes == 0:
        return 'red'
    elif num_bikes < 5:
        return 'orange'
    else:
        return 'green'


def geocode(address):
    """
    Convert address to coordinates using a geocoding service
    
    Args:
        address: Full address string
        
    Returns:
        list or str: [latitude, longitude] or empty string if failed
    """
    # TODO: Replace with your actual implementation
    # Example using Nominatim (OpenStreetMap)
    try:
        import urllib.parse
        encoded_address = urllib.parse.quote(address)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json&limit=1"
        
        headers = {'User-Agent': 'Toronto Bike Share App'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data:
            return [float(data[0]['lat']), float(data[0]['lon'])]
        return ''
    except:
        return ''


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points on earth
    
    Args:
        lon1, lat1: Coordinates of first point
        lon2, lat2: Coordinates of second point
        
    Returns:
        float: Distance in kilometers
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def get_bike_availability(user_location, data, bike_modes):
    """
    Find the nearest station with available bikes
    
    Args:
        user_location: [latitude, longitude] of user
        data: DataFrame with station data
        bike_modes: List of bike types requested (e.g., ['ebike', 'mechanical'])
        
    Returns:
        tuple: (station_id, latitude, longitude)
    """
    # TODO: Replace with your actual implementation
    filtered_data = data.copy()
    
    # Filter by bike type if specified
    if bike_modes:
        if 'ebike' in bike_modes and 'mechanical' not in bike_modes:
            filtered_data = filtered_data[filtered_data['ebike'] > 0]
        elif 'mechanical' in bike_modes and 'ebike' not in bike_modes:
            filtered_data = filtered_data[filtered_data['mechanical'] > 0]
        else:
            filtered_data = filtered_data[filtered_data['num_bikes_available'] > 0]
    else:
        filtered_data = filtered_data[filtered_data['num_bikes_available'] > 0]
    
    # Calculate distances
    filtered_data['distance'] = filtered_data.apply(
        lambda row: haversine(user_location[1], user_location[0], row['lon'], row['lat']),
        axis=1
    )
    
    # Find nearest station
    nearest = filtered_data.loc[filtered_data['distance'].idxmin()]
    
    return (nearest['station_id'], nearest['lat'], nearest['lon'])


def get_dock_availability(user_location, data):
    """
    Find the nearest station with available docks
    
    Args:
        user_location: [latitude, longitude] of user
        data: DataFrame with station data
        
    Returns:
        tuple: (station_id, latitude, longitude)
    """
    # TODO: Replace with your actual implementation
    filtered_data = data[data['num_docks_available'] > 0].copy()
    
    # Calculate distances
    filtered_data['distance'] = filtered_data.apply(
        lambda row: haversine(user_location[1], user_location[0], row['lon'], row['lat']),
        axis=1
    )
    
    # Find nearest station
    nearest = filtered_data.loc[filtered_data['distance'].idxmin()]
    
    return (nearest['station_id'], nearest['lat'], nearest['lon'])


def run_osrm(destination_station, user_location):
    """
    Get route from user location to destination using OSRM
    
    Args:
        destination_station: (station_id, lat, lon)
        user_location: [lat, lon]
        
    Returns:
        tuple: (coordinates_list, duration_string)
    """
    # TODO: Replace with your actual implementation
    try:
        # OSRM API for walking route
        url = f"http://router.project-osrm.org/route/v1/foot/{user_location[1]},{user_location[0]};{destination_station[2]},{destination_station[1]}?overview=full&geometries=geojson"
        
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok':
            # Extract coordinates
            coordinates = [[coord[1], coord[0]] for coord in data['routes'][0]['geometry']['coordinates']]
            
            # Get duration in minutes
            duration_seconds = data['routes'][0]['duration']
            duration_minutes = int(duration_seconds / 60)
            duration_string = f"{duration_minutes} min"
            
            return coordinates, duration_string
        else:
            # Fallback: straight line
            return [[user_location[0], user_location[1]], 
                    [destination_station[1], destination_station[2]]], "N/A"
    except:
        # Fallback: straight line
        return [[user_location[0], user_location[1]], 
                [destination_station[1], destination_station[2]]], "N/A"
