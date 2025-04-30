import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

MODEL_PATH = "data/traffic_model.pkl"

# Categorical mappings
day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

weather_mapping = {
    "Clear": 0,
    "Cloudy": 1,
    "Rainy": 2,
    "Snowy": 3
}

def train_model(csv_path="data/sample_traffic.csv"):
    df = pd.read_csv(csv_path)

    # Convert date_time to datetime object
    df['date_time'] = pd.to_datetime(df['date_time'], format="%d-%m-%Y %H:%M")

    # Extract hour, day name, and month
    df['hour'] = df['date_time'].dt.hour
    df['day'] = df['date_time'].dt.day_name()
    df['month'] = df['date_time'].dt.month

    # Fix holiday values: replace 'None' with 0
    df['holiday'] = df['holiday'].fillna(0)
    df['holiday'] = df['holiday'].apply(lambda x: 1 if x in ["Yes", 1] else 0)

    # Encode categorical values
    df['day'] = df['day'].map(day_mapping)
    df['weather'] = df['weather_main'].map(weather_mapping)

    # Features and target
    X = df[['hour', 'day', 'weather', 'month', 'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'holiday']]
    y = df['traffic_volume']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor().fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)




def predict_traffic(hour, day, month, temp, rain_1h, snow_1h, clouds_all, holiday, weather):
    # Convert inputs to numeric values
    day_encoded = day_mapping.get(day, 0)
    weather_encoded = weather_mapping.get(weather, 0)

    # Train model if it doesn't exist
    if not os.path.exists(MODEL_PATH):
        train_model()

    model = joblib.load(MODEL_PATH)
    
    # Make the prediction with all input parameters
    prediction = model.predict([[hour, day_encoded, weather_encoded, month, temp, rain_1h, snow_1h, clouds_all, holiday]])[0]
    return prediction
