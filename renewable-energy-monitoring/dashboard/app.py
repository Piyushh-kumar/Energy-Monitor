import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import path


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Maini Renewables Dashboard",
    layout="wide"
)

st.title("⚡ Maini Renewables Renewable Energy Dashboard")

# ==========================================
# LOAD DATA SAFELY
# ==========================================


BASE_DIR = Path(__file__).resolve().parent.parent

data_file = BASE_DIR / "turbine_data.csv"
sample_file = BASE_DIR / "sample_data.csv"

if data_file.exists():
    df = pd.read_csv(data_file)

elif sample_file.exists():
    st.info("Using sample data")
    df = pd.read_csv(sample_file)

else:
    st.error(
        f"""
        No data files found.

        Expected:
        {data_file}

        OR

        {sample_file}
        """
    )
    st.stop()

# ==========================================
# VALIDATE COLUMNS
# ==========================================

required_columns = [
    "wind_speed",
    "wind_direction",
    "rpm",
    "voltage",
    "current",
    "power",
    "temperature",
    "vibration",
    "status"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns: {missing_columns}"
    )

    st.write("Columns found:")

    st.write(df.columns.tolist())

    st.stop()

# ==========================================
# GET LATEST ROW
# ==========================================

latest = df.iloc[-1]

# ==========================================
# ENERGY CALCULATIONS
# ==========================================

df["energy_wh"] = df["power"] / 3600

total_energy = df["energy_wh"].sum()

# ==========================================
# KPI ROW 1
# ==========================================

st.subheader("Live Turbine Status")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Wind Speed",
        f"{latest['wind_speed']:.2f} m/s"
    )

with col2:
    st.metric(
        "RPM",
        f"{latest['rpm']:.0f}"
    )

with col3:
    st.metric(
        "Power",
        f"{latest['power']:.2f} W"
    )

with col4:
    st.metric(
        "Temperature",
        f"{latest['temperature']:.2f} °C"
    )

with col5:
    st.metric(
        "Vibration",
        f"{latest['vibration']:.2f} g"
    )

# ==========================================
# KPI ROW 2
# ==========================================

st.subheader("Electrical Parameters")

col6, col7, col8, col9 = st.columns(4)

with col6:
    st.metric(
        "Voltage",
        f"{latest['voltage']:.2f} V"
    )

with col7:
    st.metric(
        "Current",
        f"{latest['current']:.2f} A"
    )

with col8:
    st.metric(
        "Wind Direction",
        f"{latest['wind_direction']}°"
    )

with col9:
    st.metric(
        "Status",
        latest["status"]
    )

# ==========================================
# ENERGY CARD
# ==========================================

st.success(
    f"Total Energy Generated: {total_energy:.2f} Wh"
)

st.divider()

# ==========================================
# GAUGES
# ==========================================

st.subheader("Live Gauges")

g1, g2, g3 = st.columns(3)

with g1:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=latest["wind_speed"],
            title={"text": "Wind Speed"},
            gauge={
                "axis": {
                    "range": [0, 20]
                }
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with g2:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=latest["rpm"],
            title={"text": "RPM"},
            gauge={
                "axis": {
                    "range": [0, 300]
                }
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with g3:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=latest["power"],
            title={"text": "Power Output"},
            gauge={
                "axis": {
                    "range": [0, 2000]
                }
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================
# WIND SPEED TREND
# ==========================================

st.subheader("Wind Speed Trend")

fig1 = px.line(
    df,
    y="wind_speed",
    title="Wind Speed vs Time"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# POWER TREND
# ==========================================

st.subheader("Power Output Trend")

fig2 = px.line(
    df,
    y="power",
    title="Power Output vs Time"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# POWER CURVE
# ==========================================

st.subheader("Power Curve")

fig3 = px.scatter(
    df,
    x="wind_speed",
    y="power",
    title="Wind Speed vs Power Output"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# TEMPERATURE TREND
# ==========================================

st.subheader("Temperature Trend")

fig4 = px.line(
    df,
    y="temperature",
    title="Temperature"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# VIBRATION TREND
# ==========================================

st.subheader("Vibration Trend")

fig5 = px.line(
    df,
    y="vibration",
    title="Vibration"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==========================================
# ALARM SYSTEM
# ==========================================

st.subheader("Alarm Monitoring")

if latest["temperature"] > 45:
    st.error(
        "⚠ High Generator Temperature"
    )

if latest["vibration"] > 2.5:
    st.warning(
        "⚠ High Vibration Detected"
    )

if latest["wind_speed"] > 15:
    st.warning(
        "⚠ High Wind Speed"
    )

if (
    latest["temperature"] <= 45
    and latest["vibration"] <= 2.5
    and latest["wind_speed"] <= 15
):
    st.success(
        "✅ System Operating Normally"
    )

# ==========================================
# RAW DATA
# ==========================================

st.subheader("Recent Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)