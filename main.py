import pandas as pd
import requests
import matplotlib.pyplot as plt
import sqlite3

# -------------------------------
# STEP 1: Load Fitness Data
# -------------------------------
fitness = pd.read_csv("fitness.csv")

print("Fitness Data:\n")
print(fitness)

# -------------------------------
# STEP 2: Weather API
# -------------------------------
API_KEY = "4129919c424252044b1f2888d52d02fa"
city = "Hyderabad,IN"

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

# -------------------------------
# STEP 3: Check API Response
# -------------------------------
if "list" not in data:
    print("❌ API Error:")
    print(data)
    exit()

# -------------------------------
# STEP 4: Convert Weather Data
# -------------------------------
weather_list = []

for item in data["list"]:
    weather_list.append({
        "date": item["dt_txt"].split(" ")[0],
        "temp": item["main"]["temp"],
        "humidity": item["main"]["humidity"]
    })

weather = pd.DataFrame(weather_list)

# Remove duplicate dates
weather = weather.drop_duplicates(subset="date")

# Save weather data
weather.to_csv("weather.csv", index=False)

print("\nWeather Data:\n")
print(weather)

# -------------------------------
# STEP 5: Merge Data
# -------------------------------
merged = pd.merge(fitness, weather, on="date")

print("\nMerged Data:\n")
print(merged)

# Save merged data
merged.to_csv("merged.csv", index=False)

# -------------------------------
# STEP 6: Visualization
# -------------------------------
plt.figure(figsize=(8, 5))

plt.scatter(merged["temp"], merged["steps"])

plt.xlabel("Temperature (°C)")
plt.ylabel("Steps")
plt.title("Steps vs Temperature")

plt.grid(True)

plt.savefig("graph.png")

plt.show()

# -------------------------------
# STEP 7: Correlation Insight
# -------------------------------
corr = merged["steps"].corr(merged["temp"])

print("\n📊 Correlation:", round(corr, 2))

if corr > 0:
    print("👉 People are more active in hotter weather")
else:
    print("👉 People are more active in cooler weather")

# -------------------------------
# STEP 8: Store in SQLite Database
# -------------------------------
conn = sqlite3.connect("fitness_weather.db")

fitness.to_sql("fitness", conn, if_exists="replace", index=False)
weather.to_sql("weather", conn, if_exists="replace", index=False)
merged.to_sql("merged", conn, if_exists="replace", index=False)

conn.close()

print("\n✅ Database created successfully")