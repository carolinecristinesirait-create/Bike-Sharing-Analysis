# Bike Sharing Dashboard

## Deskripsi
Dashboard interaktif untuk menganalisis data Bike Sharing (harian dan per jam) menggunakan Streamlit.  
Pengguna dapat memilih dataset (Day / Hour) dan memfilter data berdasarkan bulan atau jam. Dashboard menampilkan tabel data, grafik interaktif, dan statistik ringkas dari dataset.

## Struktur Folder
Submission Proyek Analisis Data_Caroline Cristine Sirait/
├─ data/ # Berisi day.csv dan hour.csv
├─ dashboard.py # Streamlit dashboard
├─ requirements.txt # Daftar library yang dibutuhkan
├─ notebook.ipnyb # Hasil analisis data
└─ README.md


## Cara Menjalankan

1. Jalankan dashboard:
cd "C:\Users\Caroline Sirait\Downloads\dashboard project"
streamlit run dashboard.py
4. Browser akan terbuka otomatis menampilkan dashboard. Gunakan sidebar untuk memilih dataset, bulan/jam, dan melihat grafik serta statistik.

## Catatan
Pastikan file CSV (day.csv dan hour.csv) berada di folder data/.
Gunakan relative path agar dashboard bisa dijalankan di perangkat lain tanpa error.
Library yang digunakan tercantum di requirements.txt:
streamlit
pandas
plotly