import folium
import requests
import geopandas as gpd
from shapely.geometry import Point, LineString
import streamlit as st
from streamlit.components.v1 import html

def fetch_osm_data(bbox):
    """
    Fetches OpenStreetMap road data from Overpass API based on bounding box coordinates.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["highway"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def convert_to_gdf(osm_data):
    """
    Converts OSM data to GeoDataFrame.
    """
    elements = osm_data['elements']
    ways = []

    for element in elements:
        if element['type'] == 'way':
            coordinates = [(coord['lon'], coord['lat']) for coord in element['geometry']]
            ways.append(coordinates)

    gdf = gpd.GeoDataFrame(geometry=[LineString(coords) for coords in ways])
    return gdf

def display_map(roads, center=[20.5937, 78.9629], zoom_start=5):
    """
    Displays a map with the roads highlighted as lines.
    
    roads: A GeoDataFrame with roads' coordinates (could be Point or LineString).
    center: Latitude and longitude of the map center (default is India).
    zoom_start: Initial zoom level of the map.
    """
    # Initialize map centered around India
    m = folium.Map(location=center, zoom_start=zoom_start)
    
    # Iterate through the rows of the GeoDataFrame
    for _, row in roads.iterrows():
        # Check if the geometry is a Point or LineString
        if row['geometry'].geom_type == 'Point':
            # If it's a Point, use it directly
            folium.Marker([row['geometry'].y, row['geometry'].x], popup="Road Point").add_to(m)
        elif row['geometry'].geom_type == 'LineString':
            # If it's a LineString, iterate over the coordinates and add a polyline
            folium.PolyLine(locations=[(coord[1], coord[0]) for coord in row['geometry'].coords], color="blue", weight=2.5, opacity=1).add_to(m)
    
    # Convert the folium map to HTML and render it inside Streamlit
    map_html = m._repr_html_()  # This is the HTML representation of the folium map
    html(map_html, height=600)
