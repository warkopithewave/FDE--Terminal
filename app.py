import html
import io
import os

import pandas as pd
import streamlit as st

try:
    import segno  # untuk membuat QR code (opsional)
except ImportError:
    segno = None

# ============================================================
# PENGATURAN: EDIT BAGIAN INI
# ============================================================
# Isi link di dalam tanda kutip. Yang dikosongkan tidak akan ditampilkan.
LINK_SAWERIA = "https://saweria.co/Localcoffe"     # contoh: "https://saweria.co/namaanda"
LINK_SOCIABUZZ = "https://sociabuzz.com/localcoffegaming/tribe"   # contoh: "https://sociabuzz.com/namaanda/tribe"
LINK_TELEGRAM = "t.me/FDEwithyours"    # contoh: "https://t.me/namaanda"

# Opsional: kalau punya gambar QR sendiri (misalnya QRIS), taruh filenya di folder
# yang sama dengan app.py di GitHub, lalu tulis namanya di sini.
FILE_QRIS = ""        # contoh: "qris.png"

MAX_PER_KOLOM = 30    # jumlah berita maksimal yang ditampilkan per kolom
# ============================================================

TZ_LOKAL = "Asia/Jakarta"
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
REQUIRED_COLS = ["judul", "emiten", "kategori", "waktu", "skor", "sumber"]

st.set_page_config(page_title="Terminal FDE - Radar Sentimen", page_icon="📡", layout="wide")

CSS = """
<style>
/* Label tab Support */
button[data-baseweb="tab"] p{font-size:1rem !important;font-weight:600 !important;color:#4a4a47 !important;}
button[data-baseweb="tab"]:hover p{color:#1b1b1a !important;}
button[data-baseweb="tab"][aria-selected="true"] p{color:#1b1b1a !important;}
div[data-baseweb="tab-highlight"]{background-color:#1b1b1a !important;}
div[data-baseweb="tab-border"]{background-color:#dcdcd6 !important;}
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
:root{--ink:#1b1b1a;--ink2:#4a4a47;--muted:#8a8a85;--line:#dcdcd6;--paper:#f4f4f1;--card:#ffffff;}
.stApp{background:var(--paper);color:var(--ink);}
.block-container{padding-top:2rem;max-width:1400px;}
footer{visibility:hidden;}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:var(--muted);}
div[data-baseweb="input"]{background:#ffffff;border:1px solid var(--line);border-radius:10px;}
.stTextInput input{color:var(--ink);}
.stTextInput label p{font-family:'IBM Plex Sans',sans-serif;color:var(--ink2);font-size:.85rem;}

.hero{border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:18px;}
.hero-title{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:2rem;letter-spacing:.06em;color:var(--ink);line-height:1.1;}
.hero-sub{font-family:'IBM Plex Sans',sans-serif;color:var(--ink2);font-size:.95rem;margin-top:6px;}

.stats{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0 24px;}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 16px;min-width:110px;}
.stat b{display:block;font-family:'IBM Plex Mono',monospace;font-size:1.3rem;color:var(--ink);font-weight:600;}
.stat span{font-family:'IBM Plex Sans',sans-serif;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}

.kol-head{display:flex;justify-content:space-between;align-items:center;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:.92rem;letter-spacing:.05em;color:var(--ink);text-transform:uppercase;border-bottom:1px solid var(--ink);padding:0 0 8px;margin-bottom:14px;}
.kol-n{background:var(--ink);color:#ffffff;border-radius:999px;padding:1px 10px;font-size:.76rem;}

.kartu{background:var(--card);border:1px solid var(--line);border-left-width:5px;border-radius:10px;padding:14px 16px;margin-bottom:12px;font-family:'IBM Plex Sans',sans-serif;}
.kartu.hot{border-left-color:#1b1b1a;}
.kartu.good{border-left-color:#5c5c58;}
.kartu.bad{border-left-color:#aaaaa4;}
.atas{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:8px;}
.badge{font-family:'IBM Plex Mono',monospace;font-size:.66rem;font-weight:600;letter-spacing:.08em;padding:2px 8px;border-radius:4px;border:1px solid var(--ink);}
.hot .badge{background:#1b1b1a;color:#ffffff;}
.good .badge{background:#e6e6e1;color:#1b1b1a;border-color:#5c5c58;}
.bad .badge{background:#ffffff;color:#4a4a47;border-color:#aaaaa4;}
.tgl{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted);text-align:right;}
.judul{display:block;font-weight:600;font-size:.98rem;line-height:1.35;color:var(--ink);text-decoration:none;margin-bottom:10px;}
a.judul:hover{text-decoration:underline;}
.skor{display:flex;align-items:center;gap:10px;font-size:.78rem;color:var(--ink2);margin-bottom:8px;}
.skor .bar{flex:1;height:5px;background:#e8e8e3;border-radius:999px;overflow:hidden;}
.skor .bar i{display:block;height:100%;background:var(--ink2);border-radius:999px;}
.meta{display:flex;justify-content:space-between;gap:8px;font-size:.76rem;color:var(--muted);}
.meta b{color:var(--ink);font-family:'IBM Plex Mono',monospace;font-weight:600;}
.kosong{border:1px dashed #c9c9c2;border-radius:10px;padding:18px;text-align:center;color:var(--muted);font-size:.85rem;font-family:'IBM Plex Sans',sans-serif;}

.support{background:var(--ink);color:#f4f4f1;border-radius:14px;padding:22px 26px;margin:36px 0 12px;font-family:'IBM Plex Sans',sans-serif;}
.support-judul{font-family:'IBM Plex Mono',monospace;font-size:1.25rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;}
.support-sub{font-family:'IBM Plex Mono',monospace;font-size:.95rem;color:#c9c9c2;margin:2px 0 10px;}
.support p{margin:0;font-size:.9rem;line-height:1.5;color:#dcdcd6;}
.support-info{font-family:'IBM Plex Sans',sans-serif;color:var(--ink2);font-size:.88rem;}
.footer{font-family:'IBM Plex Sans',sans-serif;color:var(--muted);font-size:.74rem;text-align:center;margin:26px 0 6px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="hero"><div class="hero-title">TERMINAL FDE</div>'
    '<div class="hero-sub">Radar Sentimen · berita pasar dan emiten, diperbarui otomatis</div></div>',
    unsafe_allow_html=True,
)

search_query = st.text_input("Cari ticker emiten, topik, atau keyword", placeholder="contoh: JSMR, KUR, ekspor gas")


# ---------------------------------------------------------------
# Fungsi bantu
# ---------------------------------------------------------------
def esc(v):
    return html.escape(str(v))


def bersih(v, default="—"):
    if v is None or pd.isna(v):
        return default
    teks = str(v).strip()
    return default if teks in ("", "-", "nan", "None") else teks


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


def skor_info(v):
    """Kembalikan (teks skor, persen untuk bar atau None)."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return bersih(v), None
    if x != x:
        return "—", None
    teks = str(int(x)) if x == int(x) else f"{x:g}"
    return teks, max(0.0, min(100.0, x))


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

    # Pakai kolom 'tanggal' kalau ada dan terisi, kalau kosong pakai 'waktu'
    if "tanggal" in df.columns:
        mentah = df["tanggal"].where(df["tanggal"].notna() & (df["tanggal"].astype(str).str.strip() != ""), df["waktu"])
    else:
        mentah = df["waktu"]

    df["_dt"] = pd.to_datetime(mentah.apply(parse_waktu), utc=True, errors="coerce")
    df["_tampil"] = [
        format_waktu(d.tz_convert(TZ_LOKAL) if not pd.isna(d) else d, m) for d, m in zip(df["_dt"], mentah)
    ]

    # Baris terbaru di Sheets ada di bawah -> balik dulu, lalu urutkan berdasarkan waktu sebenarnya
    df = df.iloc[::-1].sort_values("_dt", ascending=False, kind="stable", na_position="last")
    return df, None


def kartu_html(row, kelas, label):
    skor_teks, persen = skor_info(row["skor"])
    bar = f'<div class="bar"><i style="width:{persen:.0f}%"></i></div>' if persen is not None else '<div class="bar"></div>'

    teks_judul = esc(bersih(row["judul"], "(tanpa judul)"))
    url = str(row.get("link", "")).strip()
    if url.lower().startswith(("http://", "https://")):
        judul = f'<a class="judul" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{teks_judul}</a>'
    else:
        judul = f'<div class="judul">{teks_judul}</div>'

    return (
        f'<div class="kartu {kelas}">'
        f'<div class="atas"><span class="badge">{label}</span><span class="tgl">{esc(row["_tampil"])}</span></div>'
        f"{judul}"
        f'<div class="skor"><span>Skor <b>{esc(skor_teks)}</b></span>{bar}</div>'
        f'<div class="meta"><span>Katalis <b>{esc(bersih(row["emiten"]))}</b></span>'
        f'<span>{esc(bersih(row["sumber"]))}</span></div>'
        f"</div>"
    )


def tampil_kolom(judul, df_kat, kelas, label):
    n = len(df_kat)
    st.markdown(
        f'<div class="kol-head"><span>{judul}</span><span class="kol-n">{n}</span></div>',
        unsafe_allow_html=True,
    )
    if df_kat.empty:
        st.markdown('<div class="kosong">Belum ada berita di kategori ini.</div>', unsafe_allow_html=True)
        return
    kartu = "".join(kartu_html(r, kelas, label) for _, r in df_kat.head(MAX_PER_KOLOM).iterrows())
    st.markdown(kartu, unsafe_allow_html=True)
    if n > MAX_PER_KOLOM:
        st.caption(f"Menampilkan {MAX_PER_KOLOM} berita terbaru dari {n}.")


@st.cache_data
def buat_qr(url):
    if segno is None:
        return None
    buf = io.BytesIO()
    segno.make(url, error="m").save(buf, kind="png", scale=8, border=2, dark="#1b1b1a", light="#ffffff")
    return buf.getvalue()


def tombol_link(label, url):
    if hasattr(st, "link_button"):
        st.link_button(label, url)
    else:
        st.markdown(f"[{label}]({url})")


def bagian_support():
    st.markdown(
        '<div class="support">'
        '<div class="support-judul">☕ Support</div>'
        '<div class="support-sub">Kopi Pahit, Roti Manis</div>'
        "<p>Dashboard ini dibuat dan dijaga secara mandiri. Kalau terasa bermanfaat, "
        "traktir kopi pahit dan roti manisnya. Cukup scan QR atau klik tombolnya.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    pilihan = []
    if LINK_SAWERIA:
        pilihan.append(("Saweria", LINK_SAWERIA, "Traktir lewat Saweria", "Scan untuk membuka halaman Saweria"))
    if LINK_SOCIABUZZ:
        pilihan.append(("Sociabuzz", LINK_SOCIABUZZ, "Traktir lewat Sociabuzz", "Scan untuk membuka halaman Sociabuzz"))
    if LINK_TELEGRAM:
        pilihan.append(("Telegram", LINK_TELEGRAM, "Chat dengan founder di Telegram", "Scan untuk membuka Telegram"))

    path_qris = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_QRIS) if FILE_QRIS else ""
    ada_qris = bool(path_qris) and os.path.exists(path_qris)

    if not pilihan and not ada_qris:
        st.markdown(
            '<div class="support-info">Link dukungan belum diisi. Edit <code>LINK_SAWERIA</code>, '
            "<code>LINK_SOCIABUZZ</code>, dan <code>LINK_TELEGRAM</code> di bagian atas <code>app.py</code>.</div>",
            unsafe_allow_html=True,
        )
        return

    nama_tab = [p[0] for p in pilihan] + (["QRIS"] if ada_qris else [])
    tabs = st.tabs(nama_tab)

    for tab, (nama, url, teks_tombol, keterangan) in zip(tabs, pilihan):
        with tab:
            kiri, kanan = st.columns([1, 2])
            with kiri:
                png = buat_qr(url)
                if png:
                    st.image(png, width=190)
            with kanan:
                st.markdown(f'<div class="support-info">{esc(keterangan)}, atau pakai link di bawah.</div>', unsafe_allow_html=True)
                st.code(url, language=None)
                tombol_link(teks_tombol, url)

    if ada_qris:
        with tabs[-1]:
            kiri, kanan = st.columns([1, 2])
            with kiri:
                st.image(path_qris, width=220)
            with kanan:
                st.markdown(
                    '<div class="support-info">Scan QRIS ini dari aplikasi bank atau e-wallet apa pun.</div>',
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------------
# Tampilan utama
# ---------------------------------------------------------------
df, err = load_data()

if err:
    st.error(err)
elif df.empty:
    st.info("Sistem Terminal FDE sedang memantau RSS. Belum ada data berita yang masuk.")
else:
    if search_query:
        df = df[
            df["judul"].astype(str).str.contains(search_query, case=False, na=False)
            | df["emiten"].astype(str).str.contains(search_query, case=False, na=False)
        ]

    kat = df["kategori"].astype(str)
    m_hot = kat.str.contains("Hot", case=False, na=False)
    m_good = kat.str.contains("Good", case=False, na=False)
    m_bad = kat.str.contains("Bad", case=False, na=False)

    terbaru = df["_dt"].max()
    teks_terbaru = format_waktu(terbaru.tz_convert(TZ_LOKAL), "—") if not pd.isna(terbaru) else "—"

    st.markdown(
        '<div class="stats">'
        f'<div class="stat"><b>{len(df)}</b><span>Total berita</span></div>'
        f'<div class="stat"><b>{int(m_hot.sum())}</b><span>Hot</span></div>'
        f'<div class="stat"><b>{int(m_good.sum())}</b><span>Good</span></div>'
        f'<div class="stat"><b>{int(m_bad.sum())}</b><span>Bad</span></div>'
        f'<div class="stat"><b style="font-size:.95rem;line-height:1.7">{esc(teks_terbaru)}</b><span>Berita terbaru</span></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        tampil_kolom("● Hot / Urgent", df[m_hot], "hot", "HOT")
    with col2:
        tampil_kolom("▲ Good News", df[m_good], "good", "GOOD")
    with col3:
        tampil_kolom("▼ Bad News", df[m_bad], "bad", "BAD")

    tanpa_kategori = int((~(m_hot | m_good | m_bad)).sum())
    if tanpa_kategori:
        st.caption(f"{tanpa_kategori} berita tidak ditampilkan karena kategorinya bukan Hot, Good, atau Bad.")

bagian_support()

st.markdown(
    '<div class="footer">Skor dan kategori dihasilkan otomatis dan bukan rekomendasi investasi. '
    "Data diperbarui sekitar tiap 60 detik.</div>",
    unsafe_allow_html=True,
)
