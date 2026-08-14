import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="India AQI Trends", page_icon="🌫️", layout="wide")

# ---------- Load data ----------
@st.cache_data
def load_data():
    path = Path(__file__).parent / "data.csv"
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.to_period("M").astype(str)
    return df

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

st.divider()
st.caption(f"Source: data.csv · {len(df):,} total readings across {df['state'].nunique()} states/UTs")