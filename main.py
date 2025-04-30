import sys
import os
import streamlit as st

# ✅ Ensure root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Now import using relative path, not 'app.' prefix
from app import ml_model, traffic_api, map_utils

st.set_page_config(page_title="Transportation Optimizer", layout="wide")

st.title("🚦 Transportation Optimization Dashboard")
st.markdown("Use traffic prediction and OSM routing to optimize your travel.")

# Sidebar input for Traffic Prediction
st.sidebar.header("Traffic Prediction Input")
hour = st.sidebar.slider("Hour of Day", 0, 23, 8)
day = st.sidebar.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
month = st.sidebar.selectbox("Month", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
temp = st.sidebar.number_input("Temperature (K)", min_value=-50.0, max_value=350.0, value=290.13, step=0.1)

rain_1h = st.sidebar.number_input("Rain in the last hour (mm)", min_value=0.0, max_value=500.0, value=0.0)
snow_1h = st.sidebar.number_input("Snow in the last hour (mm)", min_value=0.0, max_value=500.0, value=0.0)
clouds_all = st.sidebar.slider("Cloud Coverage (%)", 0, 100, 75)
holiday = st.sidebar.selectbox("Holiday", ["Yes", "No"])

weather = st.sidebar.selectbox("Weather Condition", ["Clear", "Rainy", "Cloudy", "Snowy"])

# Encode holiday input to binary
holiday_binary = 1 if holiday == "Yes" else 0

# Predict traffic
if st.sidebar.button("Predict Traffic Volume"):
    # Encode holiday input to binary
    holiday_binary = 1 if holiday == "Yes" else 0

    # Use the `ml_model.predict_traffic` function to predict traffic volume
    prediction = ml_model.predict_traffic(
        hour,
        day,
        month,
        temp,
        rain_1h,
        snow_1h,
        clouds_all,
        holiday_binary,
        weather  # Pass weather directly, not encoded
    )

    st.sidebar.success(f"Predicted Traffic Volume: {prediction:.2f}")


st.markdown("---")
st.header("🗺️ Road Network from OpenStreetMap")

if st.button("Fetch OSM Road Data"):
    # Bounding box for a region (example: [south, west, north, east])
    bbox = [12.92, 77.58, 12.96, 77.62]   # e.g., Mumbai area
    roads = traffic_api.fetch_traffic_data(bbox)
    st.success(f"Fetched {len(roads)} roads from OSM.")
    map_utils.display_map(roads)
