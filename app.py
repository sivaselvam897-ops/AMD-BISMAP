import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

# =================================================
# PAGE CONFIG + THEME
# =================================================
st.set_page_config(
    page_title="AMD-BISMAP | Geo-AI Digital Twin",
    layout="wide"
)

st.markdown("""
<style>
body {background-color:#0e1117;}
.block-container {padding-top:2rem;}
h1, h2, h3 {color:#f8fafc;}
.login-box {
    background:#111827;
    padding:30px;
    border-radius:14px;
    max-width:420px;
    margin:auto;
    border:1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# SIMPLE LOGIN SYSTEM (SESSION BASED)
# =================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.subheader("🔐 Login to AMD-BISMAP")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.experimental_rerun()
        else:
            st.error("Please enter username and password")

    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
    st.stop()

# =================================================
# APP HEADER
# =================================================
st.title("🧠 AMD-BISMAP")
st.caption(
    f"Welcome **{st.session_state.user}** · Geo-AI Digital Twin Platform"
)

# =================================================
# SIMULATED LOCATION DATA
# =================================================
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

# =================================================
# LOCATION SEARCH
# =================================================
st.subheader("🔍 Search Location")
search = st.text_input("Type location name (e.g. Zone A)").lower()

filtered_areas = [
    a for a in areas if search in a["name"].lower()
] if search else areas

if not filtered_areas:
    st.warning("No matching location found.")
    st.stop()

# =================================================
# MAP + HEATMAP + SHOP ICONS
# =================================================
st.subheader("🗺️ Demand–Supply Opportunity Map")

center = filtered_areas[0]
m = folium.Map(location=[center["lat"], center["lon"]], zoom_start=13)

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
            [area["lat"], area["lon"]],
            popup=f"{shop} ({area['name']})",
            icon=folium.Icon(
                icon=icon_map.get(shop, "info-sign"),
                prefix="glyphicon",
                color="blue"
            )
        ).add_to(m)

st_folium(m, width=1000, height=450)

# =================================================
# DIGITAL TWIN SIMULATION
# =================================================
st.divider()
st.subheader("🏪 Digital Twin Business Simulation")

selected = st.selectbox(
    "Select Area",
    [a["name"] for a in filtered_areas]
)
area = next(a for a in areas if a["name"] == selected)

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

# =================================================
# REVENUE FORECAST
# =================================================
st.subheader("📈 6-Month Revenue Projection")
months = ["M1","M2","M3","M4","M5","M6"]
projection = [monthly_revenue * (1 + i*0.08) for i in range(6)]
df = pd.DataFrame({"Month": months, "Revenue": projection})
st.line_chart(df.set_index("Month"))

# =================================================
# PRO AI BUSINESS ADVISOR (WITH STRATEGY PARAGRAPH)
# =================================================
st.divider()
st.subheader("🤖 AI Business Advisor — Pro")

question = st.text_input(
    "Ask: What business should I start here?"
)

def pro_advisor(area, revenue):
    if area["competition"] <= 3:
        competition = "Low"
    elif area["competition"] <= 6:
        competition = "Medium"
    else:
        competition = "High"

    if area["demand"] > 7 and area["competition"] < 4:
        business = "Cloud Kitchen / Quick Service Restaurant"
        budget = "₹4–₹7 Lakhs"
        strategy = (
            "Start with a small cloud kitchen focusing on 2–3 fast-moving food items. "
            "Partner with nearby supermarkets and restaurants for raw materials and delivery reach. "
            "Run online-only operations initially to reduce rent costs. "
            "With high demand and low competition, this approach can generate stable daily orders "
            "and scale into a full-service outlet within 6–9 months."
        )
    else:
        business = "Local Retail / Service Business"
        budget = "₹1–₹3 Lakhs"
        strategy = (
            "Begin with a focused retail or service setup targeting daily-need customers. "
            "Differentiate through pricing, convenience, or extended service hours. "
            "Leverage nearby supporting shops for cross-promotion. "
            "This approach ensures steady cash flow with controlled risk in competitive zones."
        )

    confidence = max(
        35,
        min(
            int((area["demand"] * 10) - (area["competition"] * 8) + (area["population"] / 2000)),
            95
        )
    )

    return business, budget, competition, confidence, strategy

if question:
    business, budget, competition, confidence, strategy = pro_advisor(area, monthly_revenue)

    st.markdown("### 📊 Advisor Recommendation")
    st.write(f"🏪 **Recommended Business:** {business}")
    st.write(f"💸 **Estimated Budget Range:** {budget}")
    st.write(f"⚔️ **Competition Level:** {competition}")
    st.write(f"📈 **Expected Monthly Revenue:** ₹{int(monthly_revenue):,}")
    st.write(f"✅ **Business Confidence Score:** {confidence}%")

    st.markdown("### 🧭 How to Start & What to Expect")
    st.write(strategy)

st.caption("This Pro advisor converts location intelligence into actionable business strategy.")
