# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    tanggal = st.sidebar.date_input("Tanggal", pd.to_datetime(data['dteday'].min()))
    jam = st.sidebar.slider("Jam", int(data['hr'].min()), int(data['hr'].max()), int(data['hr'].min()))
    data_filtered = data[(pd.to_datetime(data['dteday']) == pd.to_datetime(tanggal)) & (data['hr'] == jam)]

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #1F3B6D;'>Bike Sharing Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Data Table ---
st.subheader("Tabel Data Filtered")
st.dataframe(data_filtered.style.background_gradient(cmap='Blues'))

# --- KPIs / Statistik Ringkas ---
st.subheader("Ringkasan Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", int(data_filtered['cnt'].sum()))
col2.metric("Rata-rata Users", round(data_filtered['cnt'].mean(),2))
col3.metric("Peak Users", int(data_filtered['cnt'].max()))

# --- Line Chart: Total User ---
st.subheader("Jumlah Pengguna")
x_axis = 'dteday' if dataset_choice == 'Day' else 'hr'
fig_line = px.line(
    data_filtered,
    x=x_axis,
    y='cnt',
    labels={'cnt': 'Total User', 'dteday': 'Tanggal', 'hr': 'Jam'},
    title='Jumlah Pengguna'
)
fig_line.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color="#1F3B6D")
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
            1: '#1F77B4',  # Clear / Cerah
            2: '#6C757D',  # Mist / Cloudy
            3: '#9467BD',  # Light Rain / Snow
            4: '#D62728'   # Heavy Rain / Storm
        },
        title="User per Kondisi Cuaca"
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Scatter Plot: Suhu vs Total User ---
st.subheader("Suhu vs Total User")
fig_scatter = px.scatter(
    data_filtered,
    x='temp',
    y='cnt',
    color='weathersit' if dataset_choice=='Day' else 'season',
    size='hum' if 'hum' in data_filtered.columns else None,
    labels={'temp':'Temperature', 'cnt':'Total User', 'hum':'Humidity'},
    title='Pengaruh Suhu terhadap Total User'
)
fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color="#1F3B6D")
st.plotly_chart(fig_scatter, use_container_width=True)

# --- Heatmap (Hour dataset only) ---
if dataset_choice=="Hour":
    st.subheader("Heatmap Jumlah User per Jam dan Hari")
    pivot_table = data.pivot_table(index='hr', columns='weekday', values='cnt', aggfunc='mean')
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
        y=[str(i) for i in pivot_table.index],
        colorscale='Blues'
    ))
    fig_heatmap.update_layout(title="Rata-rata User per Jam dan Hari", xaxis_title="Hari", yaxis_title="Jam")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- Peak Hour / Day Insight ---
st.subheader("Insight Pengguna")
if dataset_choice == "Day":
    peak_row = data_filtered.loc[data_filtered['cnt'].idxmax()]
    st.markdown(f"**Peak Day:** {peak_row['dteday']}, Total User: {peak_row['cnt']}")
else:
    peak_row = data_filtered.loc[data_filtered['cnt'].idxmax()]
    st.markdown(f"**Peak Hour:** Jam {peak_row['hr']}, Total User: {peak_row['cnt']}")

# --- Footer / Tips ---
st.markdown("---")
st.markdown("<p style='text-align:center;color:#1F3B6D;'>Dashboard Interaktif - Tema Putih & Navy | Sumber Data Bike Sharing</p>", unsafe_allow_html=True)
