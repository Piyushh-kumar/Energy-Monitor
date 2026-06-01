import pandas as pd

df = pd.read_csv("turbine_data.csv")

# Average Wind Speed
avg_wind = df["wind_speed"].mean()

# Maximum Power
max_power = df["power"].max()

# Total Energy
df["energy_wh"] = df["power"] / 3600
total_energy = df["energy_wh"].sum()

print("Average Wind Speed:", round(avg_wind,2))
print("Maximum Power:", round(max_power,2))
print("Total Energy (Wh):", round(total_energy,2))