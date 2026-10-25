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
TZ_LOKAL = "Asia/Jakarta"
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def parse_waktu(nilai):
    """Ubah format tanggal apa pun (ISO/UTC, RSS +0700, dll) menjadi waktu WIB."""
    if nilai is None or pd.isna(nilai) or str(nilai).strip() == "":
        return pd.NaT
    dt = pd.to_datetime(str(nilai), utc=True, errors="coerce")
    if pd.isna(dt):
        return pd.NaT
    return dt.tz_convert(TZ_LOKAL)


def format_waktu(dt, cadangan):
    """Tampilkan seperti '24 Okt 2026, 23:26 WIB'. Kalau gagal diurai, pakai teks aslinya."""
    if pd.isna(dt):
        return str(cadangan)
    return f"{dt.day} {BULAN[dt.month - 1]} {dt.year}, {dt:%H:%M} WIB"


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

    # Pakai kolom 'tanggal' kalau terisi, kalau kosong pakai 'waktu'
    if "tanggal" in df.columns:
        mentah = df["tanggal"].where(df["tanggal"].notna() & (df["tanggal"].astype(str).str.strip() != ""), df["waktu"])
    else:
        mentah = df["waktu"]

    df["_mentah"] = mentah
    df["_dt"] = pd.to_datetime(mentah.apply(parse_waktu), utc=True, errors="coerce")
    df["_tampil"] = [format_waktu(d.tz_convert(TZ_LOKAL) if not pd.isna(d) else d, m) for d, m in zip(df["_dt"], mentah)]

    # Baris terbaru di Sheets ada di bawah -> balik dulu, lalu urutkan berdasarkan waktu sebenarnya
    df = df.iloc[::-1].sort_values("_dt", ascending=False, kind="stable", na_position="last")
    return df, None


# 5. Fungsi Kartu Berita
def tampil_kartu(row, warna_bg, warna_garis):
    esc = lambda v: html.escape(str(v))

    st.markdown(
        f"""
        <div style="background-color: {warna_bg}; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid {warna_garis};">
            <strong style="font-size: 16px; color: #222;">{esc(row['judul'])}</strong><br>
            <small style="color: #666;">📅 {esc(row['_tampil'])}</small><br><br>
            <span style="color: #333;">Skor: <b>{esc(row['skor'])}</b></span><br>
            <span style="color: #333;">Katalis: <b>{esc(row['emiten'])}</b></span><br>
            <em style="color: #888; font-size: 13px;">Sumber: {esc(row['sumber'])}</em>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tampil_kolom(judul, df_kat, warna_bg, warna_garis):
    st.subheader(f"{judul} ({len(df_kat)})")
    if df_kat.empty:
        st.caption("Belum ada berita di kategori ini.")
    for _, row in df_kat.iterrows():
        tampil_kartu(row, warna_bg, warna_garis)


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

    terbaru = df["_dt"].max()
    if not pd.isna(terbaru):
        st.caption(f"Berita terbaru: {format_waktu(terbaru.tz_convert(TZ_LOKAL), '-')}")

    kat = df["kategori"].astype(str)
    col1, col2, col3 = st.columns(3)

    with col1:
        tampil_kolom("🔥 Hot News / Urgent", df[kat.str.contains("Hot", case=False, na=False)], "#fbece5", "#d9534f")
    with col2:
        tampil_kolom("📈 Good News", df[kat.str.contains("Good", case=False, na=False)], "#eaf1ea", "#5cb85c")
    with col3:
        tampil_kolom("📉 Bad News", df[kat.str.contains("Bad", case=False, na=False)], "#f4f4f4", "#777")
