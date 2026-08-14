import os
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. PAGE CONFIGURATION & NAVIGATION
# ==============================================================================
st.set_page_config(
    page_title="India AQI Geographic Monitor",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.sidebar.title("🌍 AQI Analysis")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 AQI Analysis",
        "📈 AQI Trends"
    ]
)

CSV_PATH = "data.csv"

# Check and delete old schema file if it doesn't match the new custom columns
if os.path.exists(CSV_PATH):
    try:
        temp_df = pd.read_csv(CSV_PATH)
        if "aqi_value" not in temp_df.columns:
            os.remove(CSV_PATH)
    except Exception:
        os.remove(CSV_PATH)

# ==============================================================================
# 2. BUILT-IN GEOGRAPHIC COORDINATES FOR INDIAN AREAS & STATES
# ==============================================================================
CITY_COORDS = {
    # Delhi NCR
    "new delhi": (28.6139, 77.2090), "delhi": (28.6139, 77.2090), "noida": (28.5355, 77.3910), "ghaziabad": (28.6692, 77.4538),
    "gurugram": (28.4595, 77.0266), "gurgaon": (28.4595, 77.0266), "faridabad": (28.4089, 77.3178),
    # Maharashtra
    "mumbai": (19.0760, 72.8777), "pune": (18.5204, 73.8567), "nagpur": (21.1458, 79.0882), "thane": (19.2183, 72.9781),
    "nashik": (19.9975, 73.7898), "aurangabad": (19.8762, 75.3433), "solapur": (17.6599, 75.9064),
    # Karnataka
    "bengaluru": (12.9716, 77.5946), "bangalore": (12.9716, 77.5946), "mysuru": (12.2958, 76.6394), "mysore": (12.2958, 76.6394),
    "hubli": (15.3647, 75.1240), "mangaluru": (12.9141, 74.8560), "belagavi": (15.8497, 74.4977),
    # Tamil Nadu
    "chennai": (13.0827, 80.2707), "coimbatore": (11.0168, 76.9558), "madurai": (9.9252, 78.1198), "trichy": (10.7905, 78.7047),
    # Uttar Pradesh
    "lucknow": (26.8467, 80.9462), "kanpur": (26.4499, 80.3319), "agra": (27.1767, 78.0081), "varanasi": (25.3176, 82.9739),
    "meerut": (28.9845, 77.7064), "prayagraj": (25.4358, 81.8463), "allahabad": (25.4358, 81.8463), "bareilly": (28.3670, 79.4304),
    # West Bengal
    "kolkata": (22.5726, 88.3639), "siliguri": (26.7271, 88.3953), "howrah": (22.5769, 88.3186), "durgapur": (23.5204, 87.3119),
    # Gujarat
    "ahmedabad": (23.0225, 72.5714), "surat": (21.1702, 72.8311), "vadodara": (22.3072, 73.1812), "rajkot": (22.3039, 70.8022),
    # Rajasthan
    "jaipur": (26.9124, 75.7873), "udaipur": (24.5854, 73.7125), "jodhpur": (26.2389, 73.0243), "kota": (25.1825, 75.8396),
    # Punjab
    "amritsar": (31.6340, 74.8723), "ludhiana": (30.9010, 75.8573), "jalandhar": (31.3260, 75.5762), "patiala": (30.3398, 76.3869),
    # Kerala
    "kochi": (9.9312, 76.2673), "trivandrum": (8.5241, 76.9366), "thiruvananthapuram": (8.5241, 76.9366), "kozhikode": (11.2588, 75.7804),
    # Other major capitals
    "hyderabad": (17.3850, 78.4867), "patna": (25.5941, 85.1376), "bhopal": (23.2599, 77.4126), "ranchi": (23.3441, 85.3096),
    "raipur": (21.2514, 81.6296), "bhubaneswar": (20.2961, 85.8245), "guwahati": (26.1158, 91.7086), "dehradun": (30.3165, 78.0322),
    "shimla": (31.1048, 77.1734), "panaji": (15.4909, 73.8278), "srinagar": (34.0837, 74.7973), "jammu": (32.7266, 74.8570)
}

STATE_COORDS = {
    "rajasthan": (27.0238, 74.2179), "gujarat": (22.2587, 71.1924), "maharashtra": (19.7515, 75.7139),
    "karnataka": (15.3173, 75.7139), "andhra pradesh": (15.9129, 79.7400), "tamil nadu": (11.1271, 78.6569),
    "madhya pradesh": (22.9734, 78.6569), "uttar pradesh": (26.8467, 80.9462), "punjab": (31.1471, 75.3412),
    "haryana": (29.0588, 76.0856), "west bengal": (22.9868, 87.8550), "kerala": (10.8505, 76.2711),
    "telangana": (18.1124, 79.0193), "odisha": (20.9517, 85.0985), "bihar": (25.0961, 85.3131),
    "delhi": (28.6139, 77.2090), "himachal pradesh": (31.1048, 77.1734), "uttarakhand": (30.0668, 79.0193),
    "jharkhand": (23.6102, 85.2796), "chhattisgarh": (21.2787, 81.8661), "assam": (26.2006, 92.9376),
    "jammu & kashmir": (33.7782, 76.5762), "jammu and kashmir": (33.7782, 76.5762), "goa": (15.2993, 74.1240)
}

# ==============================================================================
# 3. DATA GENERATOR
# ==============================================================================
def check_and_generate_data():
    """Writes a sample data.csv using the exact user-specified headers if missing."""
    if not os.path.exists(CSV_PATH):
        np.random.seed(42)
        states_cities = {
            "Delhi": ["New Delhi", "Noida"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
            "Karnataka": ["Bengaluru", "Mysuru"],
            "Tamil Nadu": ["Chennai", "Coimbatore"],
            "Uttar Pradesh": ["Lucknow", "Kanpur"],
            "West Bengal": ["Kolkata", "Siliguri"],
            "Gujarat": ["Ahmedabad", "Surat"],
            "Rajasthan": ["Jaipur", "Udaipur"],
            "Punjab": ["Amritsar", "Ludhiana"],
            "Kerala": ["Kochi", "Trivandrum"]
        }

        state_baselines = {
            "Delhi": 190, "Uttar Pradesh": 170, "Punjab": 160,
            "Rajasthan": 130, "Gujarat": 120, "West Bengal": 120,
            "Maharashtra": 90, "Tamil Nadu": 70, "Karnataka": 60, "Kerala": 45
        }

        dates = pd.date_range(start="2020-01-01", end="2026-12-01", freq="MS")
        data_rows = []

        for state, cities in states_cities.items():
            base_aqi = state_baselines[state]
            for city in cities:
                for date in dates:
                    year = date.year
                    month = date.month

                    # year multiplier
                    if year == 2020:
                        year_mult = 0.65 if month in [3, 4, 5, 6] else 0.85
                    elif year == 2021:
                        year_mult = 1.05
                    elif year == 2022:
                        year_mult = 1.10
                    elif year == 2023:
                        year_mult = 1.12
                    elif year == 2024:
                        year_mult = 1.08
                    elif year == 2025:
                        year_mult = 0.98
                    else:  # 2026
                        year_mult = 0.88

                    # seasonal multiplier
                    is_northern = state in ["Delhi", "Uttar Pradesh", "Punjab", "Rajasthan"]
                    if is_northern:
                        if month in [11, 12, 1]:
                            season_mult = 2.4 + np.random.uniform(-0.2, 0.3)
                        elif month == 10:
                            season_mult = 1.8
                        elif month == 2:
                            season_mult = 1.6
                        elif month in [7, 8, 9]:
                            season_mult = 0.45 + np.random.uniform(-0.05, 0.05)
                        else:
                            season_mult = 1.0 + np.random.uniform(-0.1, 0.1)
                    else:
                        if month in [12, 1]:
                            season_mult = 1.35 + np.random.uniform(-0.1, 0.1)
                        elif month in [6, 7, 8]:
                            season_mult = 0.6 + np.random.uniform(-0.05, 0.05)
                        else:
                            season_mult = 0.95 + np.random.uniform(-0.05, 0.05)

                    noise = np.random.normal(0, 8)
                    aqi = int((base_aqi * year_mult * season_mult) + noise)
                    aqi = max(10, min(500, aqi))

                    if aqi <= 50:
                        status = "Good"
                    elif aqi <= 100:
                        status = "Satisfactory"
                    elif aqi <= 200:
                        status = "Moderate"
                    elif aqi <= 300:
                        status = "Poor"
                    elif aqi <= 400:
                        status = "Very Poor"
                    else:
                        status = "Severe"

                    data_rows.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "state": state,
                        "area": city,
                        "number_of_monitoring_stations": np.random.randint(2, 8),
                        "prominent_pollutants": np.random.choice(["PM2.5", "PM10", "NO2", "O3"]),
                        "aqi_value": aqi,
                        "air_quality_status": status,
                        "unit": "AQI"
                    })
        df = pd.DataFrame(data_rows)
        df.to_csv(CSV_PATH, index=False)

# Recreate if missing
check_and_generate_data()

# ==============================================================================
# 4. LOAD & GEOMAP DATA
# ==============================================================================
@st.cache_data
def load_data():
    data = pd.read_csv(CSV_PATH)
    data["Date"] = pd.to_datetime(data["Date"])
    data["Year"] = data["Date"].dt.year
    data["year"] = data["Date"].dt.year
    data["month"] = data["Date"].dt.to_period("M").astype(str)

    # Dynamically inject coordinates
    lats = []
    lons = []
    for _, row in data.iterrows():
        area = str(row["area"]).strip().lower()
        state = str(row["state"]).strip().lower()

        # Default coordinates (center of India)
        lat, lon = (20.5937, 78.9629)
        found = False

        # 1. Match City/Area
        if area in CITY_COORDS:
            lat, lon = CITY_COORDS[area]
            found = True

        # 2. Match State
        if not found and state in STATE_COORDS:
            lat, lon = STATE_COORDS[state]
            found = True

        lats.append(lat)
        lons.append(lon)

    data["Latitude"] = lats
    data["Longitude"] = lons
    return data

# ==============================================================================
# 5. PAGE ROUTING
# ==============================================================================
if page == "🏠 Home":
    df = load_data()

    st.title("🌫️ India Air Quality Index Dashboard")
    st.write("A production-ready module rendering the geographic spread and rankings of areas based on your CSV dataset.")
    st.markdown("---")

    # Navigation controls
    unique_years = sorted(df["Year"].unique())
    if len(unique_years) > 1:
        selected_year = st.slider("📅 Select Timeline Year", min_value=int(unique_years[0]), max_value=int(unique_years[-1]), value=int(unique_years[-1]))
    else:
        selected_year = unique_years[0]

    # Filter data
    df_filtered = df[df["Year"] == selected_year]
    df_previous = df[df["Year"] == (selected_year - 1)]

    # Calculations for metrics
    avg_aqi = df_filtered["aqi_value"].mean()

    # Calculate delta YoY
    if not df_previous.empty:
        prev_avg_aqi = df_previous["aqi_value"].mean()
        aqi_delta = ((avg_aqi - prev_avg_aqi) / prev_avg_aqi) * 100
        delta_val = f"{aqi_delta:.1f}% YoY Change"
    else:
        delta_val = None

    # Averages by area
    area_avg = df_filtered.groupby(["area", "state"], as_index=False)["aqi_value"].mean()
    polluted_area = area_avg.loc[area_avg["aqi_value"].idxmax()]
    cleanest_area = area_avg.loc[area_avg["aqi_value"].idxmin()]

    # Unique active stations/areas
    total_stations = df_filtered["number_of_monitoring_stations"].sum()

    # KPIs Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="National Average AQI",
            value=f"{avg_aqi:.1f}",
            delta=delta_val,
            delta_color="inverse" if delta_val else "normal"
        )
    with m2:
        st.metric(
            label="🍃 Cleanest Area",
            value=cleanest_area["area"],
            delta=f"Avg AQI: {cleanest_area['aqi_value']:.1f}",
            delta_color="off"
        )
    with m3:
        st.metric(
            label="🚨 Most Polluted Area",
            value=polluted_area["area"],
            delta=f"Avg AQI: {polluted_area['aqi_value']:.1f}",
            delta_color="off"
        )
    with m4:
        st.metric(
            label="📡 Active Monitoring Stations",
            value=f"{total_stations:,}",
            delta=f"{df_filtered['area'].nunique()} Areas Monitored",
            delta_color="off"
        )

    st.markdown("---")

    # Main Content Layout: Side-by-Side Map and Standings
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🗺️ Geographic AQI Distribution Map")

        # Calculate city average for the map
        map_df = df_filtered.groupby(["area", "state", "Latitude", "Longitude"])["aqi_value"].mean().reset_index()

        # Map using open Mapbox dark style
        fig_map = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            color="aqi_value",
            size="aqi_value",
            color_continuous_scale=["#10b981", "#84cc16", "#f59e0b", "#f97316", "#ef4444", "#7c2d12"],
            hover_name="area",
            hover_data={"state": True, "aqi_value": ":.1f", "Latitude": False, "Longitude": False},
            zoom=3.8,
            center={"lat": 20.5937, "lon": 78.9629},
            height=500
        )
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(title="AQI Value")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        st.subheader("🏆 Area Standings")

        sorted_areas = area_avg.sort_values(by="aqi_value", ascending=False).reset_index(drop=True)
        sorted_areas.index += 1
        sorted_areas.index.name = "Rank"
        sorted_areas.rename(columns={"area": "Area", "state": "State", "aqi_value": "Avg AQI"}, inplace=True)

        tab_worst, tab_best = st.tabs(["🔥 Top Polluted Areas", "🍃 Top Cleanest Areas"])

        with tab_worst:
            st.dataframe(
                sorted_areas.head(10).style.background_gradient(subset=["Avg AQI"], cmap="OrRd"),
                use_container_width=True,
                height=430
            )

        with tab_best:
            st.dataframe(
                sorted_areas.tail(10).sort_values("Avg AQI").style.background_gradient(subset=["Avg AQI"], cmap="Greens"),
                use_container_width=True,
                height=430
            )

elif page == "📊 AQI Analysis":
    st.title("Air Quality Index Analysis")
    st.write('''AQI Analysis analyzes air quality data to identify pollution levels and major trends.
It compares AQI values across different cities, states, and pollutants.
This analysis helps understand pollution patterns and identify areas with poor air quality.''')
    
    df = load_data()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.sunburst(
            df,
            path=["state", "area"],
            title="AQI Distribution"
        )
        event = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            key="sunburst_chart"
        )

    with col2:
        st.subheader("Selected State Details")

        selected_label = None
        if event and event.get("selection") and event["selection"].get("points"):
            selected_label = event["selection"]["points"][0].get("label")

        if selected_label in df["state"].unique():
            st.dataframe(df[df["state"] == selected_label], use_container_width=True)
        elif selected_label in df["area"].unique():
            parent_state = df.loc[df["area"] == selected_label, "state"].iloc[0]
            st.dataframe(df[df["state"] == parent_state], use_container_width=True)
        else:
            st.info("Click on a state or area in the sunburst chart to see details here.")

    stations = (
        df.groupby(["state", "area"])["number_of_monitoring_stations"]
          .max()
          .groupby(level=0)
          .sum()
          .reset_index()
    )
    stations.columns = ["state", "stations"]
    stations = stations.sort_values("stations", ascending=False)

    fig_bar = px.bar(
        stations,
        x='state',
        y='stations',
        title='Number of Monitoring Stations',
        labels={"state": "State", "stations": "Number of Monitoring Stations"},
        color_discrete_sequence=["#ef4444"]
    )
    st.plotly_chart(fig_bar, use_container_width=True)

elif page == "📈 AQI Trends":
    df = load_data()

    # ---------- Sidebar ----------
    st.sidebar.title("Filters")
    states = ["All India"] + sorted(df["state"].unique().tolist())
    selected_state = st.sidebar.selectbox("State", states)

    years = sorted(df["year"].unique().tolist())
    year_range = st.sidebar.select_slider(
        "Year range", options=years, value=(min(years), max(years))
    )

    scope = df if selected_state == "All India" else df[df["state"] == selected_state]
    scope = scope[(scope["year"] >= year_range[0]) & (scope["year"] <= year_range[1])]

    # ---------- Header ----------
    st.title("🌫️ India AQI Trends")
    st.caption(
        f"Averaging every monitoring-station reading in the dataset · "
        f"scope: **{selected_state}** · {year_range[0]}–{year_range[1]}"
    )

    # ---------- Key stats ----------
    monthly = scope.groupby("month")["aqi_value"].mean().round(1)
    yearly = scope.groupby("year")["aqi_value"].mean().round(1)

    col1, col2, col3, col4 = st.columns(4)

    if len(monthly) >= 2:
        first_val, last_val = monthly.iloc[0], monthly.iloc[-1]
        pct = (last_val - first_val) / first_val * 100
        col1.metric(
            f"{monthly.index[0]} → {monthly.index[-1]}",
            f"{last_val:.0f} AQI",
            f"{pct:+.1f}%",
            delta_color="inverse",
        )
    else:
        col1.metric("Change", "n/a")

    if len(yearly) >= 2:
        y_first, y_last = yearly.iloc[0], yearly.iloc[-1]
        ypct = (y_last - y_first) / y_first * 100
        col2.metric(
            f"Full year {yearly.index[0]} → {yearly.index[-1]}",
            f"{y_last:.0f} AQI",
            f"{ypct:+.1f}%",
            delta_color="inverse",
        )

    if len(monthly) > 0:
        peak_month = monthly.idxmax()
        col3.metric("Worst month on record", f"{monthly.max():.0f} AQI", peak_month)

    col4.metric("Readings in view", f"{len(scope):,}")

    st.divider()

    # ---------- Monthly trend line chart ----------
    st.subheader("Monthly average AQI")

    def aqi_color(v):
        if v <= 50: return "#4caf7d"
        if v <= 100: return "#a9c93a"
        if v <= 200: return "#e0b83c"
        if v <= 300: return "#e0793c"
        return "#c04b4b"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly.index, y=monthly.values,
        mode="lines+markers",
        line=dict(color="#e0b83c", width=2.5, shape="spline"),
        marker=dict(size=7, color=[aqi_color(v) for v in monthly.values], line=dict(width=1, color="#10141c")),
        fill="tozeroy",
        fillcolor="rgba(224,184,60,0.12)",
        hovertemplate="%{x}<br>AQI %{y}<extra></extra>",
    ))
    fig.update_layout(
        height=420,
        plot_bgcolor="#10141c", paper_bgcolor="#10141c",
        font=dict(color="#eef1f6"),
        xaxis=dict(gridcolor="#1c2330", tickangle=-45),
        yaxis=dict(gridcolor="#1c2330", title="AQI"),
        margin=dict(t=20, l=10, r=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "🟢 Good ≤50 · 🟡 Satisfactory 51–100 · 🟠 Moderate 101–200 · "
        "🔴 Poor 201–300 · 🟣 Very Poor 301+"
    )

    # ---------- Yearly bars + state ranking ----------
    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.subheader("Yearly average AQI")
        fig2 = go.Figure(go.Bar(
            x=yearly.index.astype(str), y=yearly.values,
            marker_color="#e0b83c",
            text=yearly.values, textposition="outside",
        ))
        fig2.update_layout(
            height=300,
            plot_bgcolor="#10141c", paper_bgcolor="#10141c",
            font=dict(color="#eef1f6"),
            xaxis=dict(gridcolor="#1c2330"),
            yaxis=dict(gridcolor="#1c2330"),
            margin=dict(t=10, l=10, r=10, b=10),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("First/last year in range may be partial — treat as directional.")

    with c2:
        st.subheader(f"Most polluted states, {year_range[1]}")
        latest_year = df[df["year"] == year_range[1]]
        rank = (
            latest_year.groupby("state")["aqi_value"]
            .mean().round(0).sort_values(ascending=False).head(10)
        )
        st.dataframe(
            rank.rename("Avg AQI").reset_index().rename(columns={"state": "State"}),
            hide_index=True, use_container_width=True,
        )   