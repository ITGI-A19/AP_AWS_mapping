import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# --- Page setup ---
st.set_page_config(page_title="APSAC WMS + Points Viewer", layout="wide")

# --- Load and clean CSV ---
data = pd.read_csv("AP Lat_long State and ITGI(1).csv")
data.columns = data.columns.str.strip()  # Remove spaces in headers

# --- Detect Latitude and Longitude columns ---
lat_candidates = [c for c in data.columns if "lat" in c.lower()]
lon_candidates = [c for c in data.columns if "lon" in c.lower()]

if not lat_candidates or not lon_candidates:
    st.error(f"CSV columns found: {data.columns.tolist()} - Could not detect Lat/Lon.")
    st.stop()

lat_col = lat_candidates[0]
lon_col = lon_candidates[0]

# --- Detect popup column ---
popup_candidates = [c for c in data.columns if c not in [lat_col, lon_col]]
popup_col = popup_candidates[0] if popup_candidates else None

st.write("Detected Columns:", data.columns.tolist())
st.write(f"Latitude column → {lat_col}")
st.write(f"Longitude column → {lon_col}")
if popup_col:
    st.write(f"Popup column → {popup_col}")
else:
    st.write("No popup column detected, using coordinates only.")

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

# --- Add point markers safely ---
for _, row in data.iterrows():
    popup_value = str(row.get(popup_col, "")) if popup_col else ""
    folium.Marker(
        location=[row[lat_col], row[lon_col]],
        popup=popup_value,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# --- Display map in Streamlit ---
st_data = st_folium(m, width=1200, height=700)
