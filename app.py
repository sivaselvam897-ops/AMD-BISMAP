import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

st.set_page_config(page_title="Geo-AI Digital Twin", layout="wide")

st.title("🧠 Geo-AI Business Digital Twin")
st.caption("Simulate a business before it exists")

areas = [
    {"name": "Zone A", "lat": 9.93, "lon": 78.12, "population": 12000, "demand": 8, "supply": 4, "competition": 3},
    {"name": "Zone B", "lat": 9.95, "lon": 78.14, "population": 8000, "demand": 5, "supply": 6, "competition": 7},
    {"name": "Zone C", "lat": 9.91, "lon": 78.10, "population": 15000, "demand": 9, "supply": 3, "competition": 2},
]

m = folium.Map(location=[9.93, 78.12], zoom_start=13)

heat_data = [
    [a["lat"], a["lon"], a["demand"] - a["supply"]]
    for a in areas
]

HeatMap(
    heat_data,
    radius=30,
    blur=20,
    min_opacity=0.4
).add_to(m)

st.subheader("📍 Opportunity Heatmap")
st_folium(m, width=700, height=450)

def simulate_business(area):
    adjusted_demand = area["demand"] * (1 + growth / 100)
adjusted_competition = max(0, area["competition"] + competition_change)

daily_orders = int(
    area["population"] * 0.015 *
    (adjusted_demand / 10) *
    (1 - adjusted_competition / 10)
)

monthly_revenue = daily_orders * 180 * 30
risk = (adjusted_competition + area["supply"]) / 20
    return daily_orders, monthly_revenue, risk

st.divider()
st.subheader("🏪 Digital Twin Simulation")
st.subheader("🎛️ Scenario Controls")

growth = st.slider("Demand Growth (%)", -20, 50, 10)
competition_change = st.slider("Competition Change", -3, 3, 0)

selected = st.selectbox("Select Area", [a["name"] for a in areas])
area = next(a for a in areas if a["name"] == selected)

orders, revenue, risk = simulate_business(area)

st.metric("Daily Orders", orders)
st.metric("Monthly Revenue (₹)", f"{revenue:,}")
st.metric("Risk Score", round(risk, 2))
st.subheader("📈 6-Month Revenue Simulation")

months = ["M1", "M2", "M3", "M4", "M5", "M6"]
revenue_projection = [revenue * (1 + i * 0.08) for i in range(6)]

df = pd.DataFrame({
    "Month": months,
    "Revenue": revenue_projection
})

st.line_chart(df.set_index("Month"))

if risk < 0.5:
    st.success("Low Risk – High Opportunity")
else:
    st.warning("Moderate Risk – Needs Differentiation")
st.subheader("🧩 Business Ecosystem Impact")

ecosystem = []

if area["demand"] > 7:
    ecosystem.append("Food Delivery")
if area["supply"] > 5:
    ecosystem.append("Logistics Support")
if area["population"] > 10000:
    ecosystem.append("Wholesale Suppliers")

for e in ecosystem:
    st.write("🔗 Connected Business:", e)
