import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Geo-AI Digital Twin", layout="wide")

st.title("🧠 Geo-AI Business Digital Twin")
st.caption("Simulate a business before it exists")

areas = [
    {"name": "Zone A", "lat": 9.93, "lon": 78.12, "population": 12000, "demand": 8, "supply": 4, "competition": 3},
    {"name": "Zone B", "lat": 9.95, "lon": 78.14, "population": 8000, "demand": 5, "supply": 6, "competition": 7},
    {"name": "Zone C", "lat": 9.91, "lon": 78.10, "population": 15000, "demand": 9, "supply": 3, "competition": 2},
]

m = folium.Map(location=[9.93, 78.12], zoom_start=13)

for area in areas:
    opportunity = area["demand"] - area["supply"]
    color = "green" if opportunity >= 4 else "orange" if opportunity >= 2 else "red"

    folium.CircleMarker(
        location=[area["lat"], area["lon"]],
        radius=12,
        popup=area["name"],
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st.subheader("📍 Opportunity Heatmap")
st_folium(m, width=700, height=450)

def simulate_business(area):
    daily_orders = int(area["population"] * 0.015 * (area["demand"]/10) * (1 - area["competition"]/10))
    monthly_revenue = daily_orders * 180 * 30
    risk = (area["competition"] + area["supply"]) / 20
    return daily_orders, monthly_revenue, risk

st.divider()
st.subheader("🏪 Digital Twin Simulation")

selected = st.selectbox("Select Area", [a["name"] for a in areas])
area = next(a for a in areas if a["name"] == selected)

orders, revenue, risk = simulate_business(area)

st.metric("Daily Orders", orders)
st.metric("Monthly Revenue (₹)", f"{revenue:,}")
st.metric("Risk Score", round(risk, 2))

if risk < 0.5:
    st.success("Low Risk – High Opportunity")
else:
    st.warning("Moderate Risk – Needs Differentiation")
