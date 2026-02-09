# Deployment Guide for Toronto Bike Share App

## Files Created

1. **app.py** - Your main Streamlit application
2. **helpers.py** - Helper functions (you need to replace with your actual implementation)
3. **requirements.txt** - Python dependencies
4. **README.md** - Project documentation with Hugging Face metadata
5. **.gitignore** - Files to ignore in version control

## Deployment Steps for Hugging Face Spaces

### Option 1: Using Hugging Face Web Interface

1. **Create a Hugging Face Account**
   - Go to https://huggingface.co/
   - Sign up or log in

2. **Create a New Space**
   - Click on your profile → "New Space"
   - Choose a name for your space (e.g., "toronto-bike-share")
   - Select "Streamlit" as the SDK
   - Choose visibility (Public or Private)
   - Click "Create Space"

3. **Upload Your Files**
   - In your new Space, click "Files" → "Add file" → "Upload files"
   - Upload ALL these files:
     - app.py
     - helpers.py (make sure to use YOUR actual helpers.py with working functions)
     - requirements.txt
     - README.md
   - Commit the changes

4. **Wait for Build**
   - Hugging Face will automatically build and deploy your app
   - This usually takes 2-5 minutes
   - You'll see the build logs in the "Logs" tab

### Option 2: Using Git (Recommended for Updates)

1. **Install Git** (if not already installed)

2. **Clone Your Space**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cd YOUR_SPACE_NAME
   ```

3. **Add Your Files**
   ```bash
   # Copy all the files to this directory
   cp /path/to/app.py .
   cp /path/to/helpers.py .
   cp /path/to/requirements.txt .
   cp /path/to/README.md .
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

## Deployment to Streamlit Cloud

### Steps:

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push all your files to the repository
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch (main), and main file (app.py)
   - Click "Deploy"

## Important Notes

### ⚠️ CRITICAL: Update helpers.py

The `helpers.py` file I created contains TEMPLATE/PLACEHOLDER functions. You MUST replace it with your actual `helpers.py` file that contains your working implementations of:

- `query_station_status()`
- `get_station_latlon()`
- `join_latlon()`
- `get_marker_color()`
- `geocode()`
- `get_bike_availability()`
- `get_dock_availability()`
- `run_osrm()`

### API Considerations

1. **Geocoding**: The template uses OpenStreetMap's Nominatim. If you're using a different service (Google Maps, Mapbox, etc.), update the `geocode()` function and add any required API keys to Hugging Face Secrets.

2. **OSRM Routing**: The template uses the public OSRM server. For production, consider hosting your own OSRM instance or using a commercial routing API.

### Adding Secrets (if needed)

If your app requires API keys:

1. In Hugging Face Spaces:
   - Go to Settings → Repository secrets
   - Add your secrets as key-value pairs

2. Access secrets in your code:
   ```python
   import os
   API_KEY = os.environ.get('API_KEY')
   ```

## Troubleshooting

### Build Fails
- Check the "Logs" tab for error messages
- Ensure all dependencies are in requirements.txt
- Verify that helpers.py has all required functions

### App Crashes
- Check if all API endpoints are accessible
- Verify that your helper functions handle errors gracefully
- Add try-except blocks around API calls

### Slow Performance
- The free tier has limited resources
- Consider caching data using `@st.cache_data` decorator
- Optimize map rendering for large datasets

## Next Steps

1. Replace the template `helpers.py` with your actual implementation
2. Test locally: `streamlit run app.py`
3. Deploy to Hugging Face or Streamlit Cloud
4. Share your app URL!

## Support

- Hugging Face Spaces Docs: https://huggingface.co/docs/hub/spaces
- Streamlit Docs: https://docs.streamlit.io/
- Toronto Bike Share API: https://tor.publicbikesystem.net/ube/gbfs/v1/
