
import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(
    page_title="Greenhouse Monitor",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 IoT Greenhouse Monitoring Dashboard")
st.caption("Simulation Mode - No physical sensors connected")

# Generate simulated environmental data
if "history" not in st.session_state:
    st.session_state.history = []

    for i in range(10):
        st.session_state.history.append({
            "Sample": i + 1,
            "Temperature (°C)": round(random.uniform(24, 32), 1),
            "Air Humidity (%)": round(random.uniform(50, 80), 1),
            "Soil Moisture (%)": round(random.uniform(30, 65), 1)
        })

# Generate new reading
if st.button("Generate New Reading"):
    st.session_state.history.append({
        "Sample": len(st.session_state.history) + 1,
        "Temperature (°C)": round(random.uniform(24, 35), 1),
        "Air Humidity (%)": round(random.uniform(45, 90), 1),
        "Soil Moisture (%)": round(random.uniform(20, 70), 1)
    })

df = pd.DataFrame(st.session_state.history)
latest = df.iloc[-1]

# Display readings
st.subheader("Environmental Parameters")

col1, col2, col3 = st.columns(3)

col1.metric("Temperature", f"{latest['Temperature (°C)']} °C")
col2.metric("Air Humidity", f"{latest['Air Humidity (%)']} %")
col3.metric("Soil Moisture", f"{latest['Soil Moisture (%)']} %")

# Alerts
st.subheader("Greenhouse Status")

if latest["Temperature (°C)"] > 32:
    st.warning("High temperature detected!")
else:
    st.success("Temperature is within the demo range.")

if latest["Soil Moisture (%)"] < 30:
    st.warning("Soil is dry. Irrigation may be needed.")
else:
    st.success("Soil moisture is within the demo range.")

# Charts
st.subheader("Environmental Trends")

tab1, tab2, tab3 = st.tabs([
    "Temperature",
    "Air Humidity",
    "Soil Moisture"
])

with tab1:
    fig = px.line(
        df,
        x="Sample",
        y="Temperature (°C)",
        markers=True,
        title="Temperature History"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.line(
        df,
        x="Sample",
        y="Air Humidity (%)",
        markers=True,
        title="Air Humidity History"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.line(
        df,
        x="Sample",
        y="Soil Moisture (%)",
        markers=True,
        title="Soil Moisture History"
    )
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Simulation Data Log")
st.dataframe(df, use_container_width=True)

# Export CSV
st.download_button(
    "Download CSV Report",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="greenhouse_data.csv",
    mime="text/csv"
)

st.caption("All readings are simulated, not real sensor measurements.")
