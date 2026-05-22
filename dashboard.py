# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Path relative ---
data_folder = os.path.join(os.path.dirname(__file__), "data")
day_data = pd.read_csv(os.path.join(data_folder, "day.csv"))
hour_data = pd.read_csv(os.path.join(data_folder, "hour.csv"))

# --- Sidebar: Pilihan Dataset ---
st.sidebar.header("Pengaturan Dashboard")
dataset_choice = st.sidebar.selectbox("Pilih Dataset", ["Day", "Hour"])

# --- Filter Data ---
if dataset_choice == "Day":
    data = day_data.copy()
    tahun = st.sidebar.selectbox("Tahun", sorted(data['yr'].unique()))
    bulan = st.sidebar.slider("Bulan", int(data['mnth'].min()), int(data['mnth'].max()), int(data['mnth'].min()))
    data_filtered = data[(data['yr'] == tahun) & (data['mnth'] == bulan)]
else:
    data = hour_data.copy()
    jam = st.sidebar.slider("Jam", int(data['hr'].min()), int(data['hr'].max()), int(data['hr'].min()))
    data_filtered = data[data['hr'] == jam]

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4E73B0;'>Bike Sharing Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Data Table ---
st.subheader("Tabel Data Filtered")
st.dataframe(data_filtered)

# --- Line Chart: Total User ---
st.subheader("Jumlah Pengguna (Line Chart)")
x_axis = 'dteday' if dataset_choice == 'Day' else 'hr'
fig_line = px.line(
    data_filtered,
    x=x_axis,
    y='cnt',
    labels={'cnt': 'Total User', 'dteday': 'Tanggal', 'hr': 'Jam'},
    title='Jumlah Pengguna'
)
st.plotly_chart(fig_line, use_container_width=True)

# --- Pie Chart: Distribusi Weather (Day dataset only) ---
if dataset_choice == "Day":
    st.subheader("Distribusi User Berdasarkan Kondisi Cuaca")
    weather_counts = data_filtered.groupby("weathersit")['cnt'].sum().reset_index()
    fig_pie = px.pie(
        weather_counts,
        values='cnt',
        names='weathersit',
        color='weathersit',
        color_discrete_map={
            1: '#3498db',  # Clear / Cerah
            2: '#95a5a6',  # Mist / Cloudy
            3: '#9b59b6',  # Light Rain / Snow
            4: '#e74c3c'   # Heavy Rain / Storm
        },
        title="User per Kondisi Cuaca"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Statistik Ringkas ---
st.subheader("Statistik Ringkas")
st.write(data_filtered.describe())

# --- Peak Hour Insight (Hour dataset only) ---
if dataset_choice == "Hour":
    peak_row = data_filtered.loc[data_filtered['cnt'].idxmax()]
    st.markdown(f"**Peak Hour:** Jam {peak_row['hr']}, Total User: {peak_row['cnt']}")
