import pandas as pd
import random
import time
from datetime import datetime
import os

csv_file = "turbine_data.csv"

if not os.path.exists(csv_file):

    pd.DataFrame(columns=[
        "timestamp",
        "wind_speed",
        "wind_direction",
        "rpm",
        "voltage",
        "current",
        "power",
        "temperature",
        "vibration",
        "status"
    ]).to_csv(csv_file, index=False)

while True:

    wind_speed = round(random.uniform(2,15),2)

    wind_direction = random.randint(0,360)

    rpm = round(wind_speed * 15,2)

    voltage = round(random.uniform(220,240),2)

    current = round(random.uniform(1,10),2)

    power = round(0.5 * (wind_speed**3),2)

    temperature = round(random.uniform(25,50),2)

    vibration = round(random.uniform(0.1,3.0),2)

    status = "Running"

    row = pd.DataFrame([{
        "timestamp": datetime.now(),
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
        "rpm": rpm,
        "voltage": voltage,
        "current": current,
        "power": power,
        "temperature": temperature,
        "vibration": vibration,
        "status": status
    }])

    row.to_csv(
        csv_file,
        mode="a",
        header=False,
        index=False
    )

    print(row.iloc[0].to_dict())

    time.sleep(1)