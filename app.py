import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Fitness Weather Dashboard",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------
BASE_DIR = os.path.dirname(_file_)

csv_path = os.path.join(BASE_DIR, "merged.csv")

merged = pd.read_csv(csv_path)

# -------------------------------
# TITLE
# -------------------------------
st.title("🏋️ Fitness + Weather Dashboard")

st.markdown(
    "Analyze how weather conditions affect fitness activity."
)

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📋 Merged Dataset")

st.dataframe(merged)

# -------------------------------
# CHARTS
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚶 Daily Steps")
    st.line_chart(merged["steps"])

with col2:
    st.subheader("🌡️ Temperature")
    st.line_chart(merged["temp"])

# -------------------------------
# CORRELATION
# -------------------------------
corr = merged["steps"].corr(merged["temp"])

st.subheader("📊 Correlation Analysis")

st.write(f"Correlation Value: {corr:.2f}")

if corr > 0:
    st.success("People are more active in hotter weather")
else:
    st.info("People are more active in cooler weather")

# -------------------------------
# SHOW GRAPH IMAGE
# -------------------------------
st.subheader("📈 Scatter Plot")

st.image("graph.png")