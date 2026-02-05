import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

# 1. Load the dataset
# Replace 'US_Accidents_Sample.csv' with your filename
df = pd.read_csv('US_Accidents_Sample.csv')

# 2. Data Preprocessing
# Convert Start_Time to datetime objects
df['Start_Time'] = pd.to_datetime(df['Start_Time'])

# Extract Hour, Day, and Month for pattern analysis
df['Hour'] = df['Start_Time'].dt.hour
df['DayOfWeek'] = df['Start_Time'].dt.day_name()
df['Month'] = df['Start_Time'].dt.month

# --- ANALYSIS 1: TIME OF DAY PATTERNS ---
plt.figure(figsize=(12, 5))
sns.countplot(data=df, x='Hour', palette='viridis')
plt.title('Accident Frequency by Hour of Day')
plt.xlabel('Hour (0-23)')
plt.ylabel('Number of Accidents')
plt.show()

# --- ANALYSIS 2: WEATHER & ROAD CONDITIONS ---
# Top 10 Weather Conditions
plt.figure(figsize=(12, 5))
weather_counts = df['Weather_Condition'].value_counts().head(10)
sns.barplot(x=weather_counts.index, y=weather_counts.values, palette='magma')
plt.title('Top 10 Weather Conditions at Accident Sites')
plt.xticks(rotation=45)
plt.show()

# Road Features Impact (Contributing Factors)
road_features = ['Traffic_Signal', 'Junction', 'Crossing', 'Stop']
# Summing True values for each feature
feature_counts = df[road_features].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=feature_counts.index, y=feature_counts.values, palette='coolwarm')
plt.title('Impact of Road Features on Accidents')
plt.ylabel('Count of Accidents')
plt.show()

# --- ANALYSIS 3: ACCIDENT HOTSPOTS (MAP) ---
# We use a sample for the map to ensure performance
sample_map = df.sample(n=min(1000, len(df))) 

# Initialize the map at a central US location
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Create a list of Latitude and Longitude pairs
heat_data = [[row['Start_Lat'], row['Start_Lng']] for index, row in sample_map.iterrows()]

# Add HeatMap to the map
HeatMap(heat_data).add_to(m)

# Save the map to an HTML file
m.save('accident_hotspots.html')
print("Hotspot map has been saved as 'accident_hotspots.html'. Open it in a browser.")