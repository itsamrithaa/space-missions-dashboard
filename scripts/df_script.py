from tqdm import tqdm
import requests
import pandas as pd
import time
import folium

# Get SpaceX launch data API
url = "https://api.spacexdata.com/v4/launches"

# API call
response = requests.get(url)

# Conversion of JSON to Python list
launch_data = response.json()

# Get rocket names API, call API, and convert to list
rockets = requests.get("https://api.spacexdata.com/v4/rockets").json()

# Repeat this for payload and launchpad
payload = requests.get("https://api.spacexdata.com/v4/payloads").json()
launchpad = requests.get("https://api.spacexdata.com/v4/launchpads").json()

# Read launch data as data frame
df = pd.DataFrame(launch_data)

# Convert launch date to datetime
df['date_utc'] = pd.to_datetime(df['date_utc'])
# Rename mission name for clarity 
df = df.rename(columns={'name': 'mission_name'})

rocket_df = pd.DataFrame(rockets)
payload_df = pd.DataFrame(payload)
launchpad_df = pd.DataFrame(launchpad)

# Merge rocket name and launch data 
rocket_dict = rocket_df.set_index('id')['name'].to_dict()
df['rocket_name'] = df['rocket'].map(rocket_dict)

# Merge payload ID and launch site with launch data 
df['first_payload_id'] = df['payloads'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
merged_df = df.merge(payload_df, how='left', left_on='first_payload_id', right_on='id', suffixes=('', '_payload')) # payload ID
merged_df = merged_df.merge(launchpad_df[['id', 'name', 'locality', 'region', 'latitude', 'longitude']], #launch site
                          how='left', 
                          left_on='launchpad', 
                          right_on='id', 
                          suffixes=('', '_launchpad'))


# Generate features such as payload type, launch site, rocket type and region
merged_df = merged_df.rename(columns={'type': 'payload_type', 'locality': 'launch_location', 'rocket_name':'rocket_type', 'region':'launch_region'}) # Rename columns for clarity
merged_df['launch_date'] = pd.to_datetime(merged_df['date_utc']).dt.strftime('%Y-%m-%d')

# Create empty lists for each weather feature
avg_temps = []
avg_winds = []
avg_humidities = []

# Update API call to include multiple weather parameters
for idx, row in tqdm(merged_df.iterrows(), total=merged_df.shape[0]):
    lat = row['latitude']
    lon = row['longitude']
    date = pd.to_datetime(row['date_utc']).strftime('%Y-%m-%d')

    if pd.isna(lat) or pd.isna(lon):
        avg_temps.append(None)
        avg_winds.append(None)
        avg_humidities.append(None)
        continue

    weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={date}&end_date={date}"
        f"&hourly=temperature_2m,wind_speed_10m,relative_humidity_2m"
    )

    try:
        response = requests.get(weather_url, timeout=10)
        if response.status_code == 200:
            data = response.json().get('hourly', {})
            temps = data.get('temperature_2m', [])
            winds = data.get('wind_speed_10m', [])
            humidity = data.get('relative_humidity_2m', [])

            avg_temp = sum(temps) / len(temps) if temps else None
            avg_wind = sum(winds) / len(winds) if winds else None
            avg_humidity = sum(humidity) / len(humidity) if humidity else None
        else:
            avg_temp = avg_wind = avg_humidity = None
    
    except Exception as e:
        print(f"Error at index {idx} - {e}")
        avg_temp = avg_wind = avg_humidity = None

    avg_temps.append(avg_temp)
    avg_winds.append(avg_wind)
    avg_humidities.append(avg_humidity)
    time.sleep(1)  # Avoid API rate limits

# Add all weather data to the DataFrame
merged_df['average_temp'] = avg_temps
merged_df['average_wind_speed'] = avg_winds
merged_df['average_humidity'] = avg_humidities


# 1. Extract rocket type from rocket API
# 2. Extract orbit, mass and payload type from payload API
# 3. Extract launch location and region from launchpad API
# 4. Extract average temperature, windspeed and humidity from weather API
# 5. Merge extracted info with mission name, date and success from SpaceX launches API

final_df = merged_df[['mission_name', 'date_utc', 'latitude', 'longitude', 'rocket_type', 'payload_type', 'mass_kg', 'orbit', 'launch_location', 'launch_region', 'average_temp', 'average_wind_speed', 'average_humidity','success']] # final df with all merged and necessary data
final_df.to_csv("Project-Template/data/raw/spacex_df.csv")

print(final_df)
print("Data frame processed.")