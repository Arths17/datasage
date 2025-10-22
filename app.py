import streamlit as st
import pandas as pd
import fastf1 as ff1
import plotly.express as px
import os  # Import the os module to create directories

# --- Page Configuration ---
# Set the page title and a wide layout for the dashboard
st.set_page_config(
    page_title="DataSage - F1 Dashboard",
    layout="wide"
)

# --- Caching ---
# Use Streamlit's caching to avoid re-loading data on every interaction.
# This is a huge performance boost.

# Ensure the cache directory exists before enabling the cache
cache_dir = 'cache_folder'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
ff1.Cache.enable_cache(cache_dir)  # Enables FastF1's built-in cache

@st.cache_data  # Streamlit's cache for the app's data
def load_session_data(year, race_name, session_type):
    """
    Loads session data from FastF1 and returns the laps dataframe.
    """
    try:
        session = ff1.get_session(year, race_name, session_type)
        session.load(telemetry=False, weather=False)  # Load basic data, not all (for speed)
        laps = session.laps
        return laps
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- Main App ---
st.title("🧙 DataSage F1 Dashboard")
st.markdown("This is the first functional version of the DataSage platform, showcasing F1 lap data.")

# --- Sidebar Inputs ---
st.sidebar.header("Dashboard Controls")
year = st.sidebar.number_input("Select Year", min_value=2018, max_value=2024, value=2024)
race_name = st.sidebar.text_input("Enter Race Name", value="Monza")
session_type = st.sidebar.selectbox("Select Session", ["Race", "Qualifying", "FP1", "FP2", "FP3"], index=0)

# --- Main Content ---
if st.sidebar.button("Load Data"):
    with st.spinner(f"Loading {year} {race_name} {session_type} data..."):
        laps_data = load_session_data(year, race_name, session_type)

    if laps_data is not None and not laps_data.empty:
        st.success(f"Successfully loaded data for {year} {race_name} {session_type}!")
        
        # Display Raw Data
        st.subheader("Raw Lap Data")
        st.dataframe(laps_data)
        
        # --- Example Plot: Lap Times ---
        st.subheader("Lap Time by Driver")
        
        # Prepare data for plotting
        lap_times = laps_data[['Driver', 'LapNumber', 'LapTime']].dropna()
        
        # Convert LapTime (timedelta) to total seconds for plotting
        lap_times['LapTimeSeconds'] = lap_times['LapTime'].dt.total_seconds()
        
        # Get list of drivers for multiselect
        drivers = lap_times['Driver'].unique()
        selected_drivers = st.multiselect("Select drivers to compare:", drivers, default=drivers[:5])
        
        if selected_drivers:
            # Filter data for selected drivers
            plot_data = lap_times[lap_times['Driver'].isin(selected_drivers)]
            
            # Create a Plotly line chart
            fig = px.line(
                plot_data,
                x="LapNumber",
                y="LapTimeSeconds",
                color="Driver",
                title="Lap Times Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least one driver to plot.")

    else:
        st.warning("No data found or an error occurred. Try a different race name (e.g., 'Bahrain', 'Silverstone', 'Monza').")

else:
    st.info("Select a year, race, and session, then click 'Load Data' in the sidebar to begin.")

