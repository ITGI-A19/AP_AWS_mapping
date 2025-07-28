import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# --- Page setup ---
st.set_page_config(page_title="APSAC WMS + Points Viewer", layout="wide")

# --- Load CSV ---
data = pd.read_csv("AP Lat_long State and ITGI(1).csv")

# Ensure column names match your file
# Assuming columns: Latitude, Longitude, Name
lat_col = "Latitude"
lon_col = "Longitude"
popup_col = "Name"  # Change to actual column with names/labels

# --- Create folium map ---
m = folium.Map(location=[15.9, 79.7], zoom_start=7)

# --- APSAC GeoServer WMS URL ---
wms_url = "https://apsac.ap.gov.in/geoserver/ows?"

# Add District Boundary layer
folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name="AP District Boundary",
    layers="admin:ap_district_boundary",
    fmt="image/png",
    transparent=True,
    version="1.3.0",
).add_to(m)

# Add Village Boundary layer
folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name="AP Village Boundary",
    layers="admin:ap_village_boundary",
    fmt="image/png",
    transparent=True,
    version="1.3.0",
).add_to(m)

# --- Add point markers ---
for _, row in data.iterrows():
    folium.Marker(
        location=[row[lat_col], row[lon_col]],
        popup=str(row[popup_col]),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# --- Display map in Streamlit ---
st_data = st_folium(m, width=1200, height=700)
