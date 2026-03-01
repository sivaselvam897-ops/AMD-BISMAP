import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AMD-BISMAP | Geo-AI Digital Twin",
    layout="wide"
)

st.title("🧠 AMD-BISMAP — Geo-AI Digital Twin")
st.caption("Simulate business performance before the business exists")

# -----------------------------
# SIMULATED AREA DATA
# -----------------------------
areas = [
    {"name": "Zone A", "lat": 9.93, "lon": 78.12, "population": 12000, "demand": 8, "supply": 4, "competition": 3},
    {"name": "Zone B", "lat": 9.95, "lon": 78.14, "population": 8000, "demand": 5, "supply": 6, "competition": 7},
    {"name": "Zone C", "lat": 9.91, "lon": 78.10, "population": 15000, "demand": 9, "supply": 3, "competition": 2},
]

# -----------------------------
# MAP + HEATMAP
# -----------------------------
st.subheader("🗺️ Demand–Supply Opportunity Heatmap")

m = folium.Map(location=[9.93, 78.12], zoom_start=12)

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

st_folium(m, width=900, height=450)

st.info("🟢 Green zones indicate high demand–low supply opportunity regions")

# -----------------------------
# DIGITAL TWIN SIMULATION
# -----------------------------
st.divider()
st.subheader("🏪 Digital Twin Simulation")

selected_area = st.selectbox(
    "Select Area",
    [a["name"] for a in areas]
)

area = next(a for a in areas if a["name"] == selected_area)

# -----------------------------
# SCENARIO CONTROLS
# -----------------------------
st.subheader("🎛️ Scenario Controls")

growth = st.slider("Demand Growth (%)", -20, 50, 10)
competition_change = st.slider("Competition Change", -3, 3, 0)

# -----------------------------
# DIGITAL TWIN ENGINE
# -----------------------------
adjusted_demand = area["demand"] * (1 + growth / 100)
adjusted_competition = max(0, area["competition"] + competition_change)

daily_orders = int(
    area["population"] * 0.015 *
    (adjusted_demand / 10) *
    (1 - adjusted_competition / 10)
)

monthly_revenue = daily_orders * 180 * 30
risk_score = (adjusted_competition + area["supply"]) / 20

# -----------------------------
# OUTPUT METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📦 Daily Orders", daily_orders)
col2.metric("💰 Monthly Revenue (₹)", f"{monthly_revenue:,}")
col3.metric("⚠️ Risk Score", round(risk_score, 2))

if risk_score < 0.5:
    st.success("✅ Low Risk — High Opportunity Zone")
else:
    st.warning("⚠️ Moderate Risk — Needs Differentiation")

# -----------------------------
# REVENUE FORECAST GRAPH
# -----------------------------
st.subheader("📈 6-Month Revenue Projection")

months = ["M1", "M2", "M3", "M4", "M5", "M6"]
revenue_projection = [
    monthly_revenue * (1 + i * 0.08) for i in range(6)
]

df = pd.DataFrame({
    "Month": months,
    "Revenue": revenue_projection
})

st.line_chart(df.set_index("Month"))

# -----------------------------
# BUSINESS ECOSYSTEM INTELLIGENCE
# -----------------------------
st.subheader("🧩 Business Ecosystem Impact")

ecosystem = []

if area["demand"] > 7:
    ecosystem.append("Food Delivery Platforms")
if area["supply"] > 5:
    ecosystem.append("Logistics & Fulfilment Services")
if area["population"] > 10000:
    ecosystem.append("Wholesale & Supplier Networks")

if ecosystem:
    for e in ecosystem:
        st.write("🔗 Connected Business:", e)
else:
    st.write("ℹ️ No strong ecosystem dependencies detected")

st.caption("We analyze businesses as part of an ecosystem — not in isolation.")
