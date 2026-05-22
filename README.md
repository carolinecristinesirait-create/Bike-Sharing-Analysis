# Bike Sharing Dashboard

## Deskripsi
Dashboard interaktif untuk menganalisis data Bike Sharing (harian dan per jam) menggunakan Streamlit.  
Pengguna dapat memilih dataset (Day / Hour) dan memfilter data berdasarkan bulan atau jam. Dashboard menampilkan tabel data, grafik interaktif, dan statistik ringkas dari dataset.


## Cara Menjalankan

1. Jalankan dashboard:
cd /path/to/Bike-Sharing-Analysis-main
streamlit run dashboard.py
2. Browser akan terbuka otomatis menampilkan dashboard. Gunakan sidebar untuk memilih dataset, bulan/jam, dan melihat grafik serta statistik.

## Catatan
Pastikan file CSV (day.csv dan hour.csv) berada di folder data/.
Gunakan relative path agar dashboard bisa dijalankan di perangkat lain tanpa error.
Library yang digunakan tercantum di requirements.txt:
streamlit
pandas
plotly
