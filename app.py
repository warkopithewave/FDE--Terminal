import html

import pandas as pd
import streamlit as st

# 1. Pengaturan Halaman Dasar
st.set_page_config(page_title="Terminal FDE - Radar Sentimen", layout="wide")

# 2. Judul Dashboard
st.title("Terminal FDE - Radar Sentimen")

# 3. Fitur Pencarian (Search Bar)
search_query = st.text_input("🔍 Cari Ticker Emiten, Topik, atau Keyword:")

REQUIRED_COLS = ["judul", "emiten", "kategori", "waktu", "skor", "sumber"]


# 4. Fungsi Mengambil Data dari Google Sheets
# ttl=60 artinya data di-refresh otomatis setiap 60 detik
@st.cache_data(ttl=60)
def load_data():
    try:
        url = st.secrets["SHEET_CSV_URL"]
    except Exception:
        return None, "SHEET_CSV_URL belum diisi di Streamlit Secrets (Manage app → Settings → Secrets)."

    try:
        df = pd.read_csv(url)
    except Exception as e:
        return None, f"Gagal memuat data dari Google Sheets: {e}"

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        return None, f"Kolom tidak ditemukan di sheet: {missing}. Kolom yang ada: {list(df.columns)}"

    # Berita terbaru (paling bawah di Sheets) tampil paling atas di web
    return df.iloc[::-1], None


# 5. Fungsi Kartu Berita
def tampil_kartu(row, warna_bg, warna_garis):
    tanggal = row.get("tanggal")
    if tanggal is None or pd.isna(tanggal) or str(tanggal).strip() == "":
        tanggal = row.get("waktu", "-")

    esc = lambda v: html.escape(str(v))

    st.markdown(
        f"""
        <div style="background-color: {warna_bg}; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid {warna_garis};">
            <strong style="font-size: 16px; color: #222;">{esc(row['judul'])}</strong><br>
            <small style="color: #666;">📅 {esc(tanggal)}</small><br><br>
            <span style="color: #333;">Skor: <b>{esc(row['skor'])}</b></span><br>
            <span style="color: #333;">Katalis: <b>{esc(row['emiten'])}</b></span><br>
            <em style="color: #888; font-size: 13px;">Sumber: {esc(row['sumber'])}</em>
        </div>
        """,
        unsafe_allow_html=True,
    )


# 6. Memproses Data & Layout Tampilan
df, err = load_data()

if err:
    st.error(err)
elif df.empty:
    st.info("Sistem Terminal FDE sedang memantau RSS. Belum ada data berita yang masuk.")
else:
    # Filter data jika pengguna mengetik sesuatu di Search Bar
    if search_query:
        df = df[
            df["judul"].astype(str).str.contains(search_query, case=False, na=False)
            | df["emiten"].astype(str).str.contains(search_query, case=False, na=False)
        ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔥 Hot News / Urgent")
        hot_news = df[df["kategori"].astype(str).str.contains("Hot", case=False, na=False)]
        for _, row in hot_news.iterrows():
            tampil_kartu(row, "#fbece5", "#d9534f")

    with col2:
        st.subheader("📈 Good News")
        good_news = df[df["kategori"].astype(str).str.contains("Good", case=False, na=False)]
        for _, row in good_news.iterrows():
            tampil_kartu(row, "#eaf1ea", "#5cb85c")

    with col3:
        st.subheader("📉 Bad News")
        bad_news = df[df["kategori"].astype(str).str.contains("Bad", case=False, na=False)]
        for _, row in bad_news.iterrows():
            tampil_kartu(row, "#f4f4f4", "#777")
