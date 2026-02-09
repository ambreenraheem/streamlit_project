import streamlit as st
import requests
import pandas as pd
import datetime as dt
import urllib
import json
import time
from helpers import *
import folium
from streamlit_folium import folium_static

# Page configuration
st.set_page_config(
    page_title="Toronto Bike Share Station Status",
    page_icon="🚲",
    layout="wide"
)

# Example URL to fetch bike share data
station_url = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'
latlon_url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

# Streamlit app setup
st.title('🚲 Toronto Bike Share Station Status')
st.markdown('This dashboard tracks bike availability at each bike share station in Toronto.')

# Fetch data for initial visualization
try:
    data_df = query_station_status(station_url)
    latlon_df = get_station_latlon(latlon_url)
    data = join_latlon(data_df, latlon_df)
except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.stop()

# Display initial metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Bikes Available Now", value=sum(data['num_bikes_available']))
    st.metric(label="E-Bikes Available Now", value=sum(data["ebike"]))
with col2:
    st.metric(label="Stations w Available Bikes", value=len(data[data['num_bikes_available'] > 0]))
    st.metric(label="Stations w Available E-Bikes", value=len(data[data['ebike'] > 0]))
with col3:
    st.metric(label="Stations w Empty Docks", value=len(data[data['num_docks_available'] > 0]))

# Track metrics for delta calculation
deltas = [
    sum(data['num_bikes_available']),
    sum(data["ebike"]),
    len(data[data['num_bikes_available'] > 0]),
    len(data[data['ebike'] > 0]),
    len(data[data['num_docks_available'] > 0])
]

# Initialize variables for user input and state
iamhere = 0
iamhere_return = 0
findmeabike = False
findmeadock = False
input_bike_modes = []

# Add sidebar selection for user inputs
with st.sidebar:
    bike_method = st.selectbox("Are you looking to rent or return a bike?", ("Rent", "Return"))
    if bike_method == "Rent":
        input_bike_modes = st.multiselect("What kind of bikes are you looking to rent?", ["ebike", "mechanical"])
        st.subheader('Where are you located?')
        input_street = st.text_input("Street", "")
        input_city = st.text_input("City", "Toronto")
        input_country = st.text_input("Country", "Canada")
        drive = st.checkbox("I'm driving there.")
        findmeabike = st.button("Find me a bike!", type="primary")
        if findmeabike:
            if input_street != "":
                iamhere = geocode(input_street + " " + input_city + " " + input_country)
                if iamhere == '':
                    st.subheader(':red[Input address not valid!]')
            else:
                st.subheader(':red[Please input your location.]')
    elif bike_method == "Return":
        st.subheader('Where are you located?')
        input_street_return = st.text_input("Street", "")
        input_city_return = st.text_input("City", "Toronto")
        input_country_return = st.text_input("Country", "Canada")
        findmeadock = st.button("Find me a dock!", type="primary")
        if findmeadock:
            if input_street_return != "":
                iamhere_return = geocode(input_street_return + " " + input_city_return + " " + input_country_return)
                if iamhere_return == '':
                    st.subheader(':red[Input address not valid!]')
            else:
                st.subheader(':red[Please input your location.]')

# Initial map setup based on user selection
if bike_method == "Return" and findmeadock == False:
    center = [43.65306613746548, -79.38815311015]
    m = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=2,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7,
            popup=folium.Popup(f"Station ID: {row['station_id']}<br>"
                               f"Total Bikes Available: {row['num_bikes_available']}<br>"
                               f"Mechanical Bike Available: {row['mechanical']}<br>"
                               f"eBike Available: {row['ebike']}", max_width=300)
        ).add_to(m)
    folium_static(m)

if bike_method == "Rent" and findmeabike == False:
    center = [43.65306613746548, -79.38815311015]
    m = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')
    for _, row in data.iterrows():
        marker_color = get_marker_color(row['num_bikes_available'])
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=2,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7,
            popup=folium.Popup(f"Station ID: {row['station_id']}<br>"
                               f"Total Bikes Available: {row['num_bikes_available']}<br>"
                               f"Mechanical Bike Available: {row['mechanical']}<br>"
                               f"eBike Available: {row['ebike']}", max_width=300)
        ).add_to(m)
    folium_static(m)

# Logic for finding a bike
if findmeabike:
    if input_street != "":
        if iamhere != "":
            chosen_station = get_bike_availability(iamhere, data, input_bike_modes)
            center = iamhere
            m1 = folium.Map(location=center, zoom_start=16, tiles='cartodbpositron')
            for _, row in data.iterrows():
                marker_color = get_marker_color(row['num_bikes_available'])
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=2,
                    color=marker_color,
                    fill=True,
                    fill_color=marker_color,
                    fill_opacity=0.7,
                    popup=folium.Popup(f"Station ID: {row['station_id']}<br>"
                                       f"Total Bikes Available: {row['num_bikes_available']}<br>"
                                       f"Mechanical Bike Available: {row['mechanical']}<br>"
                                       f"eBike Available: {row['ebike']}", max_width=300)
                ).add_to(m1)
            folium.Marker(
                location=iamhere,
                popup="You are here.",
                icon=folium.Icon(color="blue", icon="person", prefix="fa")
            ).add_to(m1)
            folium.Marker(location=(chosen_station[1], chosen_station[2]),
                          popup="Rent your bike here.",
                          icon=folium.Icon(color="red", icon="bicycle", prefix="fa")
                          ).add_to(m1)
            coordinates, duration = run_osrm(chosen_station, iamhere)
            folium.PolyLine(
                locations=coordinates,
                color="blue",
                weight=5,
                tooltip="it'll take you {} to get here.".format(duration),
            ).add_to(m1)
            folium_static(m1)
            with col3:
                st.metric(label=":green[Travel Time (min)]", value=duration)

# Logic for finding a dock
if findmeadock:
    if input_street_return != "":
        if iamhere_return != "":
            chosen_station = get_dock_availability(iamhere_return, data)
            center = iamhere_return
            m1 = folium.Map(location=center, zoom_start=16, tiles='cartodbpositron')
            for _, row in data.iterrows():
                marker_color = get_marker_color(row['num_bikes_available'])
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=2,
                    color=marker_color,
                    fill=True,
                    fill_color=marker_color,
                    fill_opacity=0.7,
                    popup=folium.Popup(f"Station ID: {row['station_id']}<br>"
                                       f"Total Bikes Available: {row['num_bikes_available']}<br>"
                                       f"Mechanical Bike Available: {row['mechanical']}<br>"
                                       f"eBike Available: {row['ebike']}", max_width=300)
                ).add_to(m1)
            folium.Marker(
                location=iamhere_return,
                popup="You are here.",
                icon=folium.Icon(color="blue", icon="person", prefix="fa")
            ).add_to(m1)
            folium.Marker(location=(chosen_station[1], chosen_station[2]),
                          popup="Return your bike here.",
                          icon=folium.Icon(color="red", icon="bicycle", prefix="fa")
                          ).add_to(m1)
            coordinates, duration = run_osrm(chosen_station, iamhere_return)
            folium.PolyLine(
                locations=coordinates,
                color="blue",
                weight=5,
                tooltip="it'll take you {} to get here.".format(duration),
            ).add_to(m1)
            folium_static(m1)
            with col3:
                st.metric(label=":green[Travel Time (min)]", value=duration)
