import streamlit as st
import pandas as pd

# Set the page title and a welcoming header
st.set_page_config(page_title="Project Atlas", layout="wide")

st.title("🚀 Project Atlas")
st.header("The Open-Source Data Visualization Platform")

st.write("Welcome to the very beginning of our project! This is our first running Streamlit app.")

# Display a sample dataframe to confirm pandas is working
st.subheader("Sample Data Test:")
df = pd.DataFrame({
    'Column A': [1, 2, 3, 4],
    'Column B': [10, 20, 30, 40]
})
st.dataframe(df)