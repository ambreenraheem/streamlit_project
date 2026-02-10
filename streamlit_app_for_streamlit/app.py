import streamlit as st
import requests
import pandas as pd
import datetime as dt
import urllib
import json
import time
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import polyline

# Configure page
st.set_page_config(
    page_title="Toronto Bike Share",
    page_icon="🚴",
    layout="wide"
)

# Helper Functions
@st.cache_data(ttl=60)
def query_station_status(url):
    """Fetch and parse station status data"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stations = []
        for station in data['data']['stations']:
            stations.append({
                'station_id': station['station_id'],
                'num_bikes_available': station['num_bikes_available'],
                'num_docks_available': station['num_docks_available'],
                'ebike': station.get('num_ebikes_available', 0),
                'mechanical': station['num_bikes_available'] - station.get('num_ebikes_available', 0)
            })
        return pd.DataFrame(stations)
    except Exception as e:
        st.error(f"Error fetching station status: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_station_latlon(url):
    """Fetch station location data"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stations = []
        for station in data['data']['stations']:
            stations.append({
                'station_id': station['station_id'],
                'lat': station['lat'],
                'lon': station['lon'],
                'name': station.get('name', 'Unknown')
            })
        return pd.DataFrame(stations)
    except Exception as e:
        st.error(f"Error fetching station locations: {e}")
        return pd.DataFrame()

def join_latlon(status_df, latlon_df):
    """Join status and location dataframes"""
    if status_df.empty or latlon_df.empty:
        return pd.DataFrame()
    return pd.merge(status_df, latlon_df, on='station_id', how='inner')

def geocode(address):
    """Convert address to coordinates"""
    try:
        geolocator = Nominatim(user_agent="toronto_bikeshare_app")
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        return ''
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return ''

def get_marker_color(num_bikes):
    """Determine marker color based on bike availability"""
    if num_bikes == 0:
        return 'red'
    elif num_bikes <= 3:
        return 'orange'
    else:
        return 'green'

def get_bike_availability(user_location, data, bike_modes):
    """Find nearest station with requested bike types"""
    filtered_data = data.copy()
    
    # Filter based on bike modes
    if 'ebike' in bike_modes and 'mechanical' not in bike_modes:
        filtered_data = filtered_data[filtered_data['ebike'] > 0]
    elif 'mechanical' in bike_modes and 'ebike' not in bike_modes:
        filtered_data = filtered_data[filtered_data['mechanical'] > 0]
    elif bike_modes:  # Both selected
        filtered_data = filtered_data[
            (filtered_data['ebike'] > 0) | (filtered_data['mechanical'] > 0)
        ]
    else:  # No preference
        filtered_data = filtered_data[filtered_data['num_bikes_available'] > 0]
    
    if filtered_data.empty:
        st.warning("No bikes available matching your criteria")
        return None
    
    # Find nearest station
    min_distance = float('inf')
    nearest_station = None
    
    for _, row in filtered_data.iterrows():
        distance = geodesic(user_location, (row['lat'], row['lon'])).meters
        if distance < min_distance:
            min_distance = distance
            nearest_station = (row['station_id'], row['lat'], row['lon'])
    
    return nearest_station

def get_dock_availability(user_location, data):
    """Find nearest station with available docks"""
    available_docks = data[data['num_docks_available'] > 0]
    
    if available_docks.empty:
        st.warning("No docks available")
        return None
    
    # Find nearest station
    min_distance = float('inf')
    nearest_station = None
    
    for _, row in available_docks.iterrows():
        distance = geodesic(user_location, (row['lat'], row['lon'])).meters
        if distance < min_distance:
            min_distance = distance
            nearest_station = (row['station_id'], row['lat'], row['lon'])
    
    return nearest_station

def run_osrm(station, user_location):
    """Get route from OSRM and calculate duration"""
    try:
        url = f"http://router.project-osrm.org/route/v1/foot/{user_location[1]},{user_location[0]};{station[2]},{station[1]}?overview=full&geometries=polyline"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['code'] == 'Ok':
            route = data['routes'][0]
            duration_seconds = route['duration']
            duration_minutes = round(duration_seconds / 60, 1)
            
            # Decode polyline
            encoded_polyline = route['geometry']
            coordinates = polyline.decode(encoded_polyline)
            
            return coordinates, duration_minutes
        return [], 0
    except Exception as e:
        st.error(f"Route calculation error: {e}")
        return [], 0

# URLs
station_url = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
latlon_url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

# App Header
st.title('🚴 Toronto Bike Share Station Status')
st.markdown('This dashboard tracks bike availability at each bike share station in Toronto.')

# Fetch data
with st.spinner('Loading bike share data...'):
    data_df = query_station_status(station_url)
    latlon_df = get_station_latlon(latlon_url)
    data = join_latlon(data_df, latlon_df)

if data.empty:
    st.error("Unable to load bike share data. Please try again later.")
    st.stop()

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Bikes Available Now", sum(data['num_bikes_available']))
    st.metric("E-Bikes Available Now", sum(data["ebike"]))
with col2:
    st.metric("Stations w/ Available Bikes", len(data[data['num_bikes_available'] > 0]))
    st.metric("Stations w/ Available E-Bikes", len(data[data['ebike'] > 0]))
with col3:
    st.metric("Stations w/ Empty Docks", len(data[data['num_docks_available'] > 0]))

# Sidebar
with st.sidebar:
    st.header("Find a Bike or Dock")
    bike_method = st.selectbox("Are you looking to rent or return a bike?", ("Rent", "Return"))
    
    if bike_method == "Rent":
        input_bike_modes = st.multiselect(
            "What kind of bikes are you looking to rent?", 
            ["ebike", "mechanical"],
            help="Select one or both bike types"
        )
        st.subheader('Where are you located?')
        input_street = st.text_input("Street", "")
        input_city = st.text_input("City", "Toronto")
        input_country = st.text_input("Country", "Canada")
        findmeabike = st.button("🔍 Find me a bike!", type="primary", use_container_width=True)
        
    elif bike_method == "Return":
        st.subheader('Where are you located?')
        input_street_return = st.text_input("Street", "")
        input_city_return = st.text_input("City", "Toronto")
        input_country_return = st.text_input("Country", "Canada")
        findmeadock = st.button("🔍 Find me a dock!", type="primary", use_container_width=True)

# Map Display
center = [43.65306613746548, -79.38815311015]

# Rent bike logic
if bike_method == "Rent":
    if 'findmeabike' in locals() and findmeabike:
        if not input_street:
            st.warning("Please input your location.")
        else:
            with st.spinner("Finding your location..."):
                iamhere = geocode(f"{input_street} {input_city} {input_country}")
            
            if not iamhere:
                st.error("Input address not valid!")
            else:
                with st.spinner("Finding nearest bike..."):
                    chosen_station = get_bike_availability(iamhere, data, input_bike_modes)
                
                if chosen_station:
                    m1 = folium.Map(location=iamhere, zoom_start=15, tiles='cartodbpositron')
                    
                    # Add all stations
                    for _, row in data.iterrows():
                        marker_color = get_marker_color(row['num_bikes_available'])
                        folium.CircleMarker(
                            location=[row['lat'], row['lon']],
                            radius=3,
                            color=marker_color,
                            fill=True,
                            fill_color=marker_color,
                            fill_opacity=0.7,
                            popup=folium.Popup(
                                f"<b>Station ID:</b> {row['station_id']}<br>"
                                f"<b>Total Bikes:</b> {row['num_bikes_available']}<br>"
                                f"<b>Mechanical:</b> {row['mechanical']}<br>"
                                f"<b>E-Bike:</b> {row['ebike']}", 
                                max_width=300
                            )
                        ).add_to(m1)
                    
                    # User location
                    folium.Marker(
                        location=iamhere,
                        popup="You are here",
                        icon=folium.Icon(color="blue", icon="user", prefix="fa")
                    ).add_to(m1)
                    
                    # Chosen station
                    folium.Marker(
                        location=(chosen_station[1], chosen_station[2]),
                        popup="Rent your bike here",
                        icon=folium.Icon(color="red", icon="bicycle", prefix="fa")
                    ).add_to(m1)
                    
                    # Route
                    coordinates, duration = run_osrm(chosen_station, iamhere)
                    if coordinates:
                        folium.PolyLine(
                            locations=coordinates,
                            color="blue",
                            weight=4,
                            opacity=0.7,
                            tooltip=f"Travel time: {duration} minutes"
                        ).add_to(m1)
                    
                    folium_static(m1, width=1200)
                    
                    if duration:
                        st.success(f"🚶 Travel time: **{duration} minutes**")
    else:
        # Default map
        m = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')
        for _, row in data.iterrows():
            marker_color = get_marker_color(row['num_bikes_available'])
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=3,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>Station ID:</b> {row['station_id']}<br>"
                    f"<b>Total Bikes:</b> {row['num_bikes_available']}<br>"
                    f"<b>Mechanical:</b> {row['mechanical']}<br>"
                    f"<b>E-Bike:</b> {row['ebike']}", 
                    max_width=300
                )
            ).add_to(m)
        folium_static(m, width=1200)

# Return bike logic
elif bike_method == "Return":
    if 'findmeadock' in locals() and findmeadock:
        if not input_street_return:
            st.warning("Please input your location.")
        else:
            with st.spinner("Finding your location..."):
                iamhere_return = geocode(f"{input_street_return} {input_city_return} {input_country_return}")
            
            if not iamhere_return:
                st.error("Input address not valid!")
            else:
                with st.spinner("Finding nearest dock..."):
                    chosen_station = get_dock_availability(iamhere_return, data)
                
                if chosen_station:
                    m1 = folium.Map(location=iamhere_return, zoom_start=15, tiles='cartodbpositron')
                    
                    # Add all stations
                    for _, row in data.iterrows():
                        marker_color = get_marker_color(row['num_bikes_available'])
                        folium.CircleMarker(
                            location=[row['lat'], row['lon']],
                            radius=3,
                            color=marker_color,
                            fill=True,
                            fill_color=marker_color,
                            fill_opacity=0.7,
                            popup=folium.Popup(
                                f"<b>Station ID:</b> {row['station_id']}<br>"
                                f"<b>Docks Available:</b> {row['num_docks_available']}<br>"
                                f"<b>Bikes Available:</b> {row['num_bikes_available']}", 
                                max_width=300
                            )
                        ).add_to(m1)
                    
                    # User location
                    folium.Marker(
                        location=iamhere_return,
                        popup="You are here",
                        icon=folium.Icon(color="blue", icon="user", prefix="fa")
                    ).add_to(m1)
                    
                    # Chosen station
                    folium.Marker(
                        location=(chosen_station[1], chosen_station[2]),
                        popup="Return your bike here",
                        icon=folium.Icon(color="green", icon="bicycle", prefix="fa")
                    ).add_to(m1)
                    
                    # Route
                    coordinates, duration = run_osrm(chosen_station, iamhere_return)
                    if coordinates:
                        folium.PolyLine(
                            locations=coordinates,
                            color="blue",
                            weight=4,
                            opacity=0.7,
                            tooltip=f"Travel time: {duration} minutes"
                        ).add_to(m1)
                    
                    folium_static(m1, width=1200)
                    
                    if duration:
                        st.success(f"🚶 Travel time: **{duration} minutes**")
    else:
        # Default map
        m = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')
        for _, row in data.iterrows():
            marker_color = get_marker_color(row['num_bikes_available'])
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=3,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>Station ID:</b> {row['station_id']}<br>"
                    f"<b>Total Bikes:</b> {row['num_bikes_available']}<br>"
                    f"<b>Mechanical:</b> {row['mechanical']}<br>"
                    f"<b>E-Bike:</b> {row['ebike']}", 
                    max_width=300
                )
            ).add_to(m)
        folium_static(m, width=1200)

# Footer
st.markdown("---")
st.markdown("Data updates every minute. Map shows: 🟢 Green (4+ bikes) | 🟠 Orange (1-3 bikes) | 🔴 Red (0 bikes)")
