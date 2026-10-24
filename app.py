import streamlit as st
import pandas as pd

# --- Konfigurasi Halaman & Estetika Visual ---
st.set_page_config(page_title="FDE Terminal", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Latar belakang warm cream, teks taupe/coklat pudar */
    .stApp { background-color: #F8F7F3; color: #4A4640; }
    
    /* Desain Kartu Berita */
    .hot-news { background-color: #E8D5C4; padding: 15px; border-left: 5px solid #D97757; border-radius: 5px; margin-bottom: 10px; }
    .good-news { background-color: #EAECE5; padding: 15px; border-left: 5px solid #849C82; border-radius: 5px; margin-bottom: 10px; }
    .bad-news { background-color: #F2E3E1; padding: 15px; border-left: 5px solid #B57F78; border-radius: 5px; margin-bottom: 10px; }
    
    /* Elemen teks */
    h1, h2, h3 { color: #4A4640 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Dukungan & Komunitas ---
with st.sidebar:
    st.subheader("☕ Dukung FDE")
    st.markdown("Jika terminal ini membantu riset Anda, dukung pengembangannya:")
    st.link_button("Dukung via Saweria", "https://saweria.co/username", use_container_width=True)
    st.link_button("Dukung via SociaBuzz", "https://sociabuzz.com/username/tribe", use_container_width=True)
    
    st.divider()
    st.markdown("**Komunitas:**")
    st.link_button("💬 Grup Telegram", "https://t.me/linkgrup", use_container_width=True)
    st.caption("FDE Terminal v1.0 | Data by AI")

# --- Header & Pencarian ---
st.title("Terminal FDE - Radar Sentimen")
search_query = st.text_input("🔍 Cari Ticker Emiten, Topik, atau Keyword:")

# --- Mockup Data Berita (Nanti diganti dengan data dari API/Database) ---
data_berita = [url_gsheets = "PASTE_URL_CSV_GOOGLE_SHEETS_ANDA_DI_SINI"

# Membaca data dengan Pandas, dan memastikan kolom Skor dibaca sebagai angka
df_berita = pd.read_csv(url_gsheets)
df_berita['Skor'] = pd.to_numeric(df_berita['Skor'], errors='coerce').fillna(0)
]
df_berita = pd.DataFrame(data_berita)

if search_query:
    df_berita = df_berita[df_berita.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

# --- Layout Utama: 3 Kolom Berita ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔥 Hot News / Urgent")
    for index, row in df_berita.iterrows():
        if row['skor'] >= 80 or row['skor'] <= -80:
            st.markdown(f"<div class='hot-news'><b>{row['judul']}</b><br>Skor: {row['skor']}<br>Katalis: {row['emiten']}<br><i>{row['sumber']}</i></div>", unsafe_allow_html=True)

with col2:
    st.subheader("📈 Good News")
    for index, row in df_berita.iterrows():
        if 0 < row['skor'] < 80:
            st.markdown(f"<div class='good-news'><b>{row['judul']}</b><br>Skor: {row['skor']}<br>Katalis: {row['emiten']}<br><i>{row['sumber']}</i></div>", unsafe_allow_html=True)

with col3:
    st.subheader("📉 Bad News")
    for index, row in df_berita.iterrows():
        if -80 < row['skor'] < 0:
            st.markdown(f"<div class='bad-news'><b>{row['judul']}</b><br>Skor: {row['skor']}<br>Katalis: {row['emiten']}<br><i>{row['sumber']}</i></div>", unsafe_allow_html=True)
