import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Air Quality Index Analysis")
st.write('''AQI Analysis analyzes air quality data to identify pollution levels and major trends.
It compares AQI values across different cities, states, and pollutants.
This analysis helps understand pollution patterns and identify areas with poor air quality.''')
df = pd.read_csv('data.csv')

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
    labels={"state": "State", "stations": "Number of Monitoring Stations"}
)
st.plotly_chart(fig_bar, use_container_width=True)