import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

# -----------------------------
# PAGE CONFIG + UI THEME
# -----------------------------
st.set_page_config(
    page_title="AMD-BISMAP | Geo-AI Digital Twin",
    layout="wide"
)

st.markdown("""
<style>
body {background-color:#0e1117;}
.block-container {padding-top:2rem;}
h1, h2, h3 {color:#f8fafc;}
.metric-box {
    background:#111827;
    padding:16px;
    border-radius:12px;
    border:1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧠 AMD-BISMAP")
st.caption("Geo-AI Digital Twin Platform — simulate businesses before they exist")

# -----------------------------
# SIMULATED AREA + ECOSYSTEM DATA
# -----------------------------
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
    },
]

# -----------------------------
# MAP + HEATMAP + SHOP ICONS
# -----------------------------
st.subheader("🗺️ Demand–Supply Opportunity Map")

m = folium.Map(location=[9.93, 78.12], zoom_start=12)

heat_data = [[a["lat"], a["lon"], a["demand"] - a["supply"]] for a in areas]

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

for area in areas:
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

st.info("🟢 Green zones indicate high-demand / low-supply opportunity hotspots")

# -----------------------------
# DIGITAL TWIN SIMULATION
# -----------------------------
st.divider()
st.subheader("🏪 Digital Twin Business Simulation")

selected = st.selectbox("Select Area", [a["name"] for a in areas])
area = next(a for a in areas if a["name"] == selected)

# -----------------------------
# SCENARIO CONTROLS
# -----------------------------
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

if risk_score < 0.5:
    st.success("✅ Low Risk — High Opportunity Zone")
else:
    st.warning("⚠️ Moderate Risk — Needs Differentiation")

# -----------------------------
# REVENUE FORECAST
# -----------------------------
st.subheader("📈 6-Month Revenue Projection")

months = ["M1","M2","M3","M4","M5","M6"]
projection = [monthly_revenue * (1 + i*0.08) for i in range(6)]

df = pd.DataFrame({"Month": months, "Revenue": projection})
st.line_chart(df.set_index("Month"))

# -----------------------------
# BUSINESS ECOSYSTEM
# -----------------------------
st.subheader("🧩 Business Ecosystem Intelligence")

for shop in area["shops"]:
    st.write("🔗 Existing business:", shop)

# -----------------------------
# AI BUSINESS ADVISOR CHATBOT
# -----------------------------
st.divider()
st.subheader("🤖 AI Business Advisor")

question = st.text_input(
    "Ask something like: What business should I start here?"
)


    # -----------------------------
# PRO AI BUSINESS ADVISOR
# -----------------------------
st.divider()
st.subheader("🤖 AI Business Advisor — Pro Insights")

question = st.text_input(
    "Ask: What business should I start here?"
)

def pro_advisor(area, revenue):
    insights = []

    # --- Competition Level ---
    if area["competition"] <= 3:
        competition_level = "Low"
    elif area["competition"] <= 6:
        competition_level = "Medium"
    else:
        competition_level = "High"

    # --- Budget Estimation ---
    if area["demand"] > 7 and area["competition"] < 4:
        business = "Cloud Kitchen / QSR"
        budget = "₹4 – ₹7 Lakhs"
    elif "Supermarket" in area["shops"]:
        business = "Delivery & Logistics Service"
        budget = "₹2 – ₹4 Lakhs"
    else:
        business = "Retail / Service Business"
        budget = "₹1 – ₹3 Lakhs"

    # --- Confidence Score ---
    confidence = (
        (area["demand"] * 10)
        - (area["competition"] * 8)
        + (area["population"] / 2000)
    )
    confidence = max(30, min(int(confidence), 95))

    # --- Insights ---
    insights.append(f"🏪 **Recommended Business:** {business}")
    insights.append(f"💸 **Estimated Budget Range:** {budget}")
    insights.append(f"⚔️ **Competition Level:** {competition_level}")
    insights.append(f"📈 **Expected Monthly Revenue:** ₹{int(revenue):,}")
    insights.append(f"✅ **Business Confidence Score:** {confidence}%")

    return insights

if question:
    st.markdown("### 📊 Pro Advisor Output")
    results = pro_advisor(area, monthly_revenue)

    for r in results:
        st.markdown(r)

    if "Cloud Kitchen" in results[0]:
        st.success("🔥 High-growth opportunity with strong demand support")
    else:
        st.info("ℹ️ Moderate growth opportunity with stable returns")

    return insights

if question:
    st.markdown("### 🧠 Advisor Insights")
    for i in advisor(area):
        st.write("•", i)

st.caption("This advisor uses location intelligence, demand-supply signals, and ecosystem context.")
