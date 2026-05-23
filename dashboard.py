# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Konfigurasi Halaman (Harus diletakkan paling atas) ---
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Kustomisasi Tema CSS (Putih - Navy) ---
st.markdown("""
    <style>
    /* Latar belakang utama putih */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Warna teks heading Navy */
    h1, h2, h3, h4, h5, h6 {
        color: #0A2342 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Kustomisasi Metrik KPI */
    div[data-testid="stMetricValue"] {
        color: #1D4E89;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #0A2342;
        font-size: 16px;
    }
    /* Garis pemisah Navy */
    hr {
        border: 1px solid #1D4E89;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Path relative & Load Data ---
@st.cache_data
def load_data():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    day_df = pd.read_csv(os.path.join(data_folder, "day.csv"))
    hour_df = pd.read_csv(os.path.join(data_folder, "hour.csv"))
    
    # Mapping nilai untuk kemudahan visualisasi
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear/Partly Cloudy', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'}
    
    day_df['season_label'] = day_df['season'].map(season_map)
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)
    
    # Format tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    return day_df, hour_df

day_data, hour_data = load_data()

# --- Sidebar: Pengaturan & Filter ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #0A2342;'>Pengaturan Filter</h2>", unsafe_allow_html=True)
    
    dataset_choice = st.selectbox("Pilih Analisis Basis Waktu:", ["Harian (Day)", "Per Jam (Hour)"])
    
    st.markdown("---")
    st.markdown("### Filter Rentang Waktu")
    
    if dataset_choice == "Harian (Day)":
        data = day_data.copy()
        min_date = data['dteday'].min().date()
        max_date = data['dteday'].max().date()
        
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        data_filtered = data[(data['dteday'].dt.date >= start_date) & (data['dteday'].dt.date <= end_date)]
    else:
        data = hour_data.copy()
        jam = st.slider("Pilih Jam (0-23)", 0, 23, (0, 23))
        data_filtered = data[(data['hr'] >= jam[0]) & (data['hr'] <= jam[1])]

# --- Header Dashboard ---
st.markdown("<h1 style='text-align: center;'>🚲 Bike Sharing Data Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1D4E89; font-size: 18px;'>Menganalisis pola penggunaan sepeda berdasarkan cuaca, musim, dan tipe pengguna.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Elemen Interaktif: Row Metrik (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

total_rides = data_filtered['cnt'].sum()
total_casual = data_filtered['casual'].sum()
total_registered = data_filtered['registered'].sum()
avg_rides = int(data_filtered['cnt'].mean())

col1.metric("Total Penyewaan", f"{total_rides:,}")
col2.metric("Pengguna Kasual", f"{total_casual:,}")
col3.metric("Pengguna Terdaftar", f"{total_registered:,}")
col4.metric("Rata-rata Sewa", f"{avg_rides:,}")

st.markdown("<br>", unsafe_allow_html=True)

# --- Elemen Interaktif: Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Performa & Tren", "⛅ Pengaruh Cuaca & Musim", "💡 Explanatory & Strategi", "🗃️ Data Mentahan"])

with tab1:
    st.subheader("Tren Penyewaan Sepeda")
    if dataset_choice == "Harian (Day)":
        fig_trend = px.line(
            data_filtered, x='dteday', y=['casual', 'registered', 'cnt'],
            labels={'value': 'Jumlah Pengguna', 'dteday': 'Tanggal', 'variable': 'Tipe Pengguna'},
            color_discrete_map={'cnt': '#0A2342', 'registered': '#1D4E89', 'casual': '#7393B3'},
            title="Tren Harian: Kasual vs Terdaftar vs Total"
        )
    else:
        trend_hourly = data_filtered.groupby('hr')['cnt'].mean().reset_index()
        fig_trend = px.bar(
            trend_hourly, x='hr', y='cnt',
            labels={'cnt': 'Rata-rata Penyewaan', 'hr': 'Jam dalam Sehari'},
            color_discrete_sequence=['#1D4E89'],
            title="Pola Penyewaan Rata-rata per Jam"
        )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Distribusi Berdasarkan Musim")
        if 'season_label' in data_filtered.columns:
            season_counts = data_filtered.groupby('season_label')[['casual', 'registered']].sum().reset_index()
            fig_season = px.bar(
                season_counts, x='season_label', y=['casual', 'registered'],
                barmode='group',
                labels={'value': 'Total Sewa', 'season_label': 'Musim'},
                color_discrete_map={'registered': '#0A2342', 'casual': '#7393B3'},
            )
            st.plotly_chart(fig_season, use_container_width=True)
        else:
            st.info("Filter Harian (Day) untuk melihat data agregat musim yang lebih akurat.")
            
    with col_b:
        st.subheader("Persentase Kondisi Cuaca")
        weather_counts = data_filtered.groupby("weather_label")['cnt'].sum().reset_index()
        fig_weather = px.pie(
            weather_counts, values='cnt', names='weather_label', hole=0.4,
            color_discrete_sequence=['#0A2342', '#1D4E89', '#5C82B6', '#A1BFE0']
        )
        st.plotly_chart(fig_weather, use_container_width=True)

with tab3:
    st.subheader("Menjawab Pertanyaan Bisnis & Rekomendasi")
    
    st.markdown("""
    Berdasarkan *Explanatory Analysis*, ditemukan dua wawasan utama mengenai perilaku pengguna:
    """)
    
    with st.expander("1. Bagaimana memulihkan performa di Musim Semi (Spring) untuk pengguna Kasual?"):
        st.markdown("""
        **Analisis:** Pengguna Casual sangat sensitif terhadap perubahan cuaca dan musim, terlihat dari penurunan signifikan pada Musim Semi atau saat cuaca masih dingin/transisi.
        
        **Tindakan Bisnis (Spring Activation):**
        - Mengadakan promo akhir pekan berskala besar di awal bulan Maret (contoh: *"Spring Weekend Ride"*).
        - Memberikan diskon khusus untuk penyewaan grup atau keluarga untuk menarik minat mereka kembali bersepeda setelah musim dingin berlalu.
        """)
        
    with st.expander("2. Bagaimana mempertahankan loyalitas Komuter (Registered) di kala cuaca buruk?"):
        st.markdown("""
        **Analisis:** Pengguna Terdaftar (Registered) adalah fondasi utama karena mereka menggunakan sepeda untuk mobilitas harian (komuter). Namun, cuaca yang kurang bersahabat (berawan atau hujan tipis) tetap menjadi hambatan.
        
        **Tindakan Bisnis (Program Apresiasi):**
        - Memberikan insentif seperti poin loyalitas ganda pada hari-hari dengan cuaca kurang baik.
        - Menyediakan fitur *booking prioritas*.
        - Melengkapi fasilitas fisik di stasiun utama, seperti pelindung sadel anti-air, agar perjalanan mereka tetap nyaman.
        """)

with tab4:
    st.subheader("Data Mentah (Raw Data)")
    st.write(f"Menampilkan data berdasarkan filter saat ini. Total baris: **{data_filtered.shape[0]}**")
    st.dataframe(
        data_filtered,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Statistik Deskriptif")
    st.write(data_filtered[['cnt', 'casual', 'registered', 'temp', 'hum', 'windspeed']].describe())

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #1D4E89; font-size: 14px;'>Dibuat dengan ❤️ | Data Analysis by Caroline Cristine Sirait</p>", unsafe_allow_html=True)
