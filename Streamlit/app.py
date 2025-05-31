import streamlit as st
import pandas as pd
from Main import FishingAnalyser  # Class import

# Initialise the FishingAnalyser class
fishing_analyser = FishingAnalyser()

st.markdown("""
# 🐟 Illegal Fishing Analysis App

Analyse vessel activity to identify suspected illegal fishing within Marine Protected Areas (MPAs).

How it works:
- Enter data manually or fetch it via the Global Fishing Watch API.
- Filters vessels located in ocean areas.
- Predict fishing (Yes/No) behavior using a trained classification random forest model.
- Identify suspected illegal activity by filtering through Marine Protected Zones.
- Visualize vessel activity on a map.

Illegal statuses:
- **Yes**: Fishing detected inside MPAs  
- **Maybe**: Not fishing but inside MPAs  
- **No**: Outside MPAs and not fishing  

Limitations:
Due to how expensive it would be to implement a live AIS feed into the project, I have used the Global Fishing Watch database which has a record of historical vessel journeys.

[🔗 GitHub Repository](https://github.com/GurpreetSDeol/Predicting-Illegal-Fishing-using-Machine-Learning/tree/main)  

[🔗 Portfolio Website](https://gurpreetsdeol.github.io/)
""")

# Sidebar
st.sidebar.title("Fishing Activity Analysis")
app_mode = st.sidebar.radio("Choose Mode", ["API Request", "Manual Input"])
plot_size = st.sidebar.slider("Plot size (point size)", min_value=5, max_value=30, value=10)

# Helpers
def display_table(data):
    st.subheader("Fishing Activity Data")

    df = data.copy()
    if 'geometry' in df.columns:
        df['geometry'] = df['geometry'].apply(lambda geom: geom.wkt if geom else None)

    st.write(df)


def plot_map(geo_df, point_size):
    st.subheader("Fishing Activity Map")
    fig = fishing_analyser.plot(geo_df, point_size)
    st.pyplot(fig)

# --- API Mode ---
if app_mode == "API Request":
    st.header("API Request to Retrieve Vessel Data")

    st.sidebar.header("API Request Settings")
    start_date = st.sidebar.date_input("Start Date", min_value=pd.to_datetime('2017-01-01'), max_value=pd.to_datetime('2025-04-01'))
    end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=pd.to_datetime('2025-04-01'))
    limit = st.sidebar.slider("Number of records", min_value=1, max_value=100, value=10)

    if st.sidebar.button("Fetch Data"):
        df = fishing_analyser.api_request(str(start_date), str(end_date), limit)

        if df is not None:
            ocean_df = fishing_analyser.filter_through_ocean(df)

            if ocean_df.empty:
                st.warning("No vessels found in ocean regions. Cannot proceed with prediction.")
            else:
                pred_df = fishing_analyser.predict_fishing_status(ocean_df)
                final_df = fishing_analyser.filter_through_mpz(pred_df)
                display_table(final_df)
                plot_map(final_df, plot_size)

# --- Manual Input Mode ---
elif app_mode == "Manual Input":
    st.header("Manual Vessel Data Input")
    st.sidebar.header("Enter Vessel Data")

    vessel_id = st.sidebar.text_input("Vessel ID ('unkown' if unkown)")
    speed = st.sidebar.number_input("Speed (Knots)", min_value=0.0)
    distance_from_shore = st.sidebar.number_input("Distance from Shore (m)", min_value=0)
    distance_from_port = st.sidebar.number_input("Distance from Port (m)", min_value=0)
    lat = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0)
    lon = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0)

    if st.sidebar.button("Predict and Plot"):
        # Create a dataframe for the single vessel
        vessel_data = pd.DataFrame({
            'vessel_id': [vessel_id],
            'speed': [speed],
            'distance_from_shore': [distance_from_shore],
            'distance_from_port': [distance_from_port],
            'lat': [lat],
            'lon': [lon]
        })

        # Filter through ocean
        ocean_df = fishing_analyser.filter_through_ocean(vessel_data)

        if ocean_df.empty:
            st.warning("The vessel is not in the ocean. Please check the coordinates.")
        else:
            # Predict fishing status
            pred_df = fishing_analyser.predict_fishing_status(ocean_df)

            # Filter through Marine Protected Zones
            geo_df = fishing_analyser.filter_through_mpz(pred_df)

            # Extract status and illegal values
            status_value = geo_df.iloc[0]["status"]
            illegal_value = geo_df.iloc[0]["illegal"]

            # Display cards
            col1, col2 = st.columns(2)

            with col1:
                st.metric(label="🛥️ Is the vessel fishing?", value=status_value)

            with col2:
                st.metric(label="🚫 Is the vessel fishing illegally?", value=illegal_value)

            # Show table and plot
            display_table(geo_df)
            plot_map(geo_df, plot_size)
