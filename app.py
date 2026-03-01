import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

# -------------------------------------------------
# PAGE CONFIG + THEME
# -------------------------------------------------
st.set_page_config(
    page_title="AMD-BISMAP | Geo-AI Digital Twin",
    layout="wide"
)

st.markdown("""
<style>
body {background-color:#0e1117;}
.block-container {padding-top:2rem;}
h1, h2, h3 {color:#f8fafc;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🧠 AMD-BISMAP")
st.caption("Geo-AI Digital Twin Platform — simulate businesses before they exist")

# -------------------------------------------------
# SIMULATED LOCATION DATA
# -------------------------------------------------
areas = [
    {
        "name": "Zone A",
        "lat": 9.93,
        "lon": 78.12,
        "population": 12000,
        "demand": 8,
        "supply": 4,
        "competition": 3,
        "shops": ["Grocery", "Bakery", "Tea Shop"]
    },
    {
        "name": "Zone B",
        "lat": 9.95,
        "lon": 78.14,
        "population": 8000,
        "demand": 5,
        "supply": 6,
        "competition": 7,
        "shops": ["Mobile Store", "Repair Shop"]
    },
    {
        "name": "Zone C",
        "lat": 9.91,
        "lon": 78.10,
        "population": 15000,
        "demand": 9,
        "supply": 3,
        "competition": 2,
        "shops": ["Restaurant", "Supermarket", "Pharmacy"]
    }
]

# -------------------------------------------------
# LOCATION SEARCH BAR
# -------------------------------------------------
st.subheader("🔍 Search Location")

search_query = st.text_input(
    "Type location name (e.g. Zone A, Zone B)"
).strip().lower()

filtered_areas = [
    a for a in areas if search_query in a["name"].lower()
] if search_query else areas

if not filtered_areas:
    st.warning("No matching location found.")
    st.stop()

# -------------------------------------------------
# MAP + HEATMAP + SHOP ICONS
# -------------------------------------------------
st.subheader("🗺️ Demand–Supply Opportunity Map")

center_lat = filtered_areas[0]["lat"]
center_lon = filtered_areas[0]["lon"]

m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

heat_data = [
    [a["lat"], a["lon"], a["demand"] - a["supply"]]
    for a in filtered_areas
]

HeatMap(
    heat_data,
    radius=35,
    blur=25,
    min_opacity=0.4
).add_to(m)

icon_map = {
    "Grocery": "shopping-cart",
    "Bakery": "cutlery",
    "Tea Shop": "coffee",
    "Restaurant": "cutlery",
    "Supermarket": "shopping-basket",
    "Pharmacy": "plus-sign",
    "Mobile Store": "phone",
    "Repair Shop": "wrench"
}

for area in filtered_areas:
    for shop in area["shops"]:
        folium.Marker(
            location=[area["lat"], area["lon"]],
            popup=f"{shop} ({area['name']})",
            icon=folium.Icon(
                icon=icon_map.get(shop, "info-sign"),
                prefix="glyphicon",
                color="blue"
            )
        ).add_to(m)

st_folium(m, width=1000, height=450)

st.info("🟢 Hotter zones indicate higher demand–lower supply")

# -------------------------------------------------
# DIGITAL TWIN SIMULATION
# -------------------------------------------------
st.divider()
st.subheader("🏪 Digital Twin Business Simulation")

selected_area = st.selectbox(
    "Select Area for Simulation",
    [a["name"] for a in filtered_areas]
)

area = next(a for a in areas if a["name"] == selected_area)

# -------------------------------------------------
# SCENARIO CONTROLS
# -------------------------------------------------
st.subheader("🎛️ Scenario Controls")

growth = st.slider("Demand Growth (%)", -20, 50, 10)
competition_change = st.slider("Competition Change", -3, 3, 0)

adjusted_demand = area["demand"] * (1 + growth / 100)
adjusted_competition = max(0, area["competition"] + competition_change)

daily_orders = int(
    area["population"] * 0.015 *
    (adjusted_demand / 10) *
    (1 - adjusted_competition / 10)
)

monthly_revenue = daily_orders * 180 * 30
risk_score = (adjusted_competition + area["supply"]) / 20

c1, c2, c3 = st.columns(3)
c1.metric("📦 Daily Orders", daily_orders)
c2.metric("💰 Monthly Revenue (₹)", f"{monthly_revenue:,}")
c3.metric("⚠️ Risk Score", round(risk_score, 2))

# -------------------------------------------------
# REVENUE FORECAST
# -------------------------------------------------
st.subheader("📈 6-Month Revenue Projection")

months = ["M1","M2","M3","M4","M5","M6"]
projection = [monthly_revenue * (1 + i * 0.08) for i in range(6)]

df = pd.DataFrame({"Month": months, "Revenue": projection})
st.line_chart(df.set_index("Month"))

# -------------------------------------------------
# PRO AI BUSINESS ADVISOR
# -------------------------------------------------
st.divider()
st.subheader("🤖 AI Business Advisor — Pro")

question = st.text_input(
    "Ask: What business should I start here?"
)

def pro_advisor(area, revenue):
    insights = []

    if area["competition"] <= 3:
        competition_level = "Low"
    elif area["competition"] <= 6:
        competition_level = "Medium"
    else:
        competition_level = "High"

    if area["demand"] > 7 and area["competition"] < 4:
        business = "Cloud Kitchen / QSR"
        budget = "₹4 – ₹7 Lakhs"
    elif "Supermarket" in area["shops"]:
        business = "Delivery & Logistics Service"
        budget = "₹2 – ₹4 Lakhs"
    else:
        business = "Retail / Service Business"
        budget = "₹1 – ₹3 Lakhs"

    confidence = (
        (area["demand"] * 10)
        - (area["competition"] * 8)
        + (area["population"] / 2000)
    )
    confidence = max(35, min(int(confidence), 95))

    insights.append(f"🏪 Recommended Business: {business}")
    insights.append(f"💸 Estimated Budget: {budget}")
    insights.append(f"⚔️ Competition Level: {competition_level}")
    insights.append(f"📈 Expected Monthly Revenue: ₹{int(revenue):,}")
    insights.append(f"✅ Business Confidence Score: {confidence}%")

    return insights

if question:
    st.markdown("### 📊 Advisor Output")
    for line in pro_advisor(area, monthly_revenue):
        st.write("•", line)

st.caption("Pro advisor converts geo-intelligence into capital, risk, and return metrics.")
