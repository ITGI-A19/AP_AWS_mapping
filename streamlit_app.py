import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="APSAC WMS + Points Viewer", layout="wide")

# --- Load CSV ---
data = pd.read_csv("AP Lat_long State and ITGI(1).csv")
data.columns = data.columns.str.strip()

lat_col = [c for c in data.columns if "lat" in c.lower()][0]
lon_col = [c for c in data.columns if "lon" in c.lower()][0]
info_columns = [c for c in data.columns if c not in [lat_col, lon_col]]

# --- Create map ---
m = folium.Map(location=[data[lat_col].mean(), data[lon_col].mean()], zoom_start=7)

# --- APSAC GeoServer WMS URL ---
wms_url = "https://apsac.ap.gov.in/geoserver/ows?"

# District Boundary layer
folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name="AP District Boundary",
    layers="admin:ap_district_boundary",
    fmt="image/png",
    transparent=True,
    version="1.3.0",
).add_to(m)

# Mandal Boundary layer (added between district and village)
folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name="AP Mandal Boundary",
    layers="admin:ap_mandal_boundary",
    fmt="image/png",
    transparent=True,
    version="1.3.0",
).add_to(m)

# Village Boundary layer
folium.raster_layers.WmsTileLayer(
    url=wms_url,
    name="AP Village Boundary",
    layers="admin:ap_village_boundary",
    fmt="image/png",
    transparent=True,
    version="1.3.0",
).add_to(m)

# --- Add points ---
for _, row in data.iterrows():
    popup_html = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in info_columns])
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=5,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
    ).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

st_folium(m, width="100%", height=700)
