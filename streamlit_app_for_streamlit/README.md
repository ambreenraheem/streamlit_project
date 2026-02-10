## Toronto Bike Share Dashboard 🚴
### A real-time Streamlit dashboard for tracking bike availability at Toronto Bike Share stations.
### Features

📊 Real-time metrics on bike and dock availability
🗺️ Interactive map showing all bike share stations
🔍 Find nearest bike station based on your location
🚲 Filter by bike type (e-bikes or mechanical bikes)
🅿️ Find nearest dock to return your bike
📍 Route visualization with estimated walking time

Local Setup

Install dependencies:
```
bashpip install -r requirements.txt
```
Run the app:
```
# bash
streamlit run app.py
```
Deployment on Streamlit Cloud

**Step 1: Prepare Your Repository**

Create a new GitHub repository

Add these files to your repository:

- app.py (main application)
- requirements.txt (dependencies)
- .streamlit/config.toml (optional configuration)
- README.md (this file)



**Step 2: Deploy on Streamlit Cloud**

- Go to share.streamlit.io
- Sign in with your GitHub account
- Click "New app"
- Select your repository, branch, and app.py
- Click "Deploy"

**Step 3: Configuration (Optional)**

If you need custom settings, create a .streamlit/config.toml file in your repo.

Files Structure

toronto-bikeshare/\
│
├── app.py                 # Main Streamlit application\
├── requirements.txt       # Python dependencies\
├── .streamlit/
│   └── config.toml       # Streamlit configuration\
└── README.md             # This file\

**Key Changes from Original**

- Removed external helpers.py: All helper functions are now included in app.py
- Added error handling: Better error messages and graceful failures
- Improved UI: Better spacing, icons, and user feedback
- Caching: Added @st.cache_data to API calls for better performance
- Geocoding: Uses Nominatim (free) instead of requiring API keys
- Route calculation: Uses public OSRM API for routing

**Dependencies**

- streamlit: Web app framework
- requests: HTTP requests for API calls
- pandas: Data manipulation
- folium: Interactive maps
- streamlit-folium: Folium integration for Streamlit
- geopy: Geocoding and distance calculations
- polyline: Route geometry decoding

**Data Sources**

- Toronto Bike Share real-time GBFS feed
- OpenStreetMap (via Nominatim) for geocoding
- OSRM (Open Source Routing Machine) for route calculation
