import streamlit as st
import pandas as pd

# 1. Pengaturan Halaman Dasar
st.set_page_config(page_title="Terminal FDE - Radar Sentimen", layout="wide")

# 2. Judul Dashboard
st.title("Terminal FDE - Radar Sentimen")

# 3. Fitur Pencarian (Search Bar)
search_query = st.text_input("🔍 Cari Ticker Emiten, Topik, atau Keyword:")

REQUIRED_COLS = ["judul", "emiten", "kategori", "waktu", "skor", "sumber"]
# 4. Fungsi Mengambil Data dari Google Sheets
# ttl=60 artinya aplikasi akan otomatis me-refresh data baru setiap 60 detik
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(st.secrets["SHEET_CSV_URL"])  # simpan link di Secrets Streamlit
    except Exception as e:
        return None, f"Gagal memuat data: {e}"

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        return None, f"Kolom tidak ditemukan di sheet: {missing}. Kolom yang ada: {list(df.columns)}"
    return df.iloc[::-1], None

df, err = load_data()
if err:
    st.error(err)
elif df.empty:
    st.info("Sistem Terminal FDE sedang memantau RSS. Belum ada data berita yang masuk.")
else:
df = load_data()

# 5. Memproses Data & Layout Tampilan
if not df.empty:
    
    # Filter data jika pengguna mengetik sesuatu di Search Bar
    if search_query:
        df = df[df['judul'].str.contains(search_query, case=False, na=False) | 
                df['emiten'].str.contains(search_query, case=False, na=False)]

    # Membagi layar menjadi 3 kolom
    col1, col2, col3 = st.columns(3)

    # ================= KOLOM 1: HOT NEWS =================
    with col1:
        st.subheader("🔥 Hot News / Urgent")
        hot_news = df[df['kategori'].str.contains('Hot', case=False, na=False)]
        
        for _, row in hot_news.iterrows():
            # Menggunakan row.get('tanggal', row['waktu']) agar jika kolom tanggal kosong, ia otomatis memakai waktu Make.com
            tanggal_tampil = row.get('tanggal', row['waktu']) 
            
            st.markdown(f"""
                <div style="background-color: #fbece5; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #d9534f;">
                    <strong style="font-size: 16px; color: #222;">{row['judul']}</strong><br>
                    <small style="color: #666;">📅 {tanggal_tampil}</small><br><br>
                    <span style="color: #333;">Skor: <b>{row['skor']}</b></span><br>
                    <span style="color: #333;">Katalis: <b>{row['emiten']}</b></span><br>
                    <em style="color: #888; font-size: 13px;">Sumber: {row['sumber']}</em>
                </div>
            """, unsafe_allow_html=True)

    # ================= KOLOM 2: GOOD NEWS =================
    with col2:
        st.subheader("📈 Good News")
        good_news = df[df['kategori'].str.contains('Good', case=False, na=False)]
        
        for _, row in good_news.iterrows():
            tanggal_tampil = row.get('tanggal', row['waktu'])
            
            st.markdown(f"""
                <div style="background-color: #eaf1ea; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #5cb85c;">
                    <strong style="font-size: 16px; color: #222;">{row['judul']}</strong><br>
                    <small style="color: #666;">📅 {tanggal_tampil}</small><br><br>
                    <span style="color: #333;">Skor: <b>{row['skor']}</b></span><br>
                    <span style="color: #333;">Katalis: <b>{row['emiten']}</b></span><br>
                    <em style="color: #888; font-size: 13px;">Sumber: {row['sumber']}</em>
                </div>
            """, unsafe_allow_html=True)

    # ================= KOLOM 3: BAD NEWS =================
    with col3:
        st.subheader("📉 Bad News")
        bad_news = df[df['kategori'].str.contains('Bad', case=False, na=False)]
        
        for _, row in bad_news.iterrows():
            tanggal_tampil = row.get('tanggal', row['waktu'])
            
            st.markdown(f"""
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #777;">
                    <strong style="font-size: 16px; color: #222;">{row['judul']}</strong><br>
                    <small style="color: #666;">📅 {tanggal_tampil}</small><br><br>
                    <span style="color: #333;">Skor: <b>{row['skor']}</b></span><br>
                    <span style="color: #333;">Katalis: <b>{row['emiten']}</b></span><br>
                    <em style="color: #888; font-size: 13px;">Sumber: {row['sumber']}</em>
                </div>
            """, unsafe_allow_html=True)

else:
    st.info("Sistem Terminal FDE sedang memantau RSS. Belum ada data berita yang masuk.")
