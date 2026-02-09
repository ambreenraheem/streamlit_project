---
title: Toronto Bike Share Station Status
emoji: 🚲
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
---

# Toronto Bike Share Station Status

This interactive dashboard tracks real-time bike availability at each bike share station in Toronto.

## Features

- **Real-time Data**: View current bike and dock availability across all Toronto bike share stations
- **Bike Finder**: Find the nearest available bike based on your location
- **Dock Finder**: Locate the nearest available dock to return your bike
- **Route Planning**: Get walking directions and estimated travel time to your destination
- **Bike Type Selection**: Filter by e-bikes or mechanical bikes

## How to Use

1. **Rent a Bike**:
   - Select "Rent" from the dropdown
   - Choose bike type (e-bike or mechanical)
   - Enter your current location
   - Click "Find me a bike!"

2. **Return a Bike**:
   - Select "Return" from the dropdown
   - Enter your current location
   - Click "Find me a dock!"

## Data Source

Real-time data is fetched from Toronto's Public Bike System GBFS API.

## Technologies Used

- Streamlit
- Folium (for interactive maps)
- Pandas (for data processing)
- OSRM (for routing)
