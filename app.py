import streamlit as st
from google import genai

# ------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Waskita Sastra - Kajian Klasik & Kawi",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# KLIEN GEMINI (API key dari Streamlit Secrets)
# ------------------------------------------------------------------
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("API Key belum dikonfigurasi di Streamlit Secrets. Harap atur terlebih dahulu di pengaturan aplikasi Anda.")
    client = None

MODELS = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]


def ask_gemini(prompt: str):
    """Coba beberapa model berurutan. Mengembalikan (teks, nama_model, error_terakhir)."""
    last_error = None
    for model_name in MODELS:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            if response.text:
                return response.text, model_name, None
        except Exception as e:
            last_error = e  # coba model berikutnya
    return None, None, last_error


# ------------------------------------------------------------------
# DATA: CONTOH NASKAH (TAB TELAAH & PUSTAKA)
# ------------------------------------------------------------------
SAMPLES = [
    {
        "label": "🌀 Kalatidha",
        "title": "Serat Kalatidha",
        "author": "R.Ng. Ranggawarsita",
        "meta": "Pupuh Sinom · Jawa Baru, abad ke-19",
        "text": (
            "Amenangi jaman edan,\n"
            "ewuh aya ing pambudi,\n"
            "melu edan nora tahan,\n"
            "yen tan melu anglakoni,\n"
            "boya keduman melik,\n"
            "kaliren wekasanipun,\n"
            "ndilalah kersa Allah,\n"
            "begja-begjane kang lali,\n"
            "luwih begja kang eling lawan waspada."
        ),
    },
    {
        "label": "🪷 Sutasoma",
        "title": "Kakawin Sutasoma",
        "author": "Mpu Tantular",
        "meta": "Kakawin · Jawa Kuno, abad ke-14",
        "text": (
            "Rwāneka dhātu winuwus Buddha Wiśwa,\n"
            "Bhinnêki rakwa ring apan kena parwanosěn,\n"
            "Mangka ng Jinatwa kalawan Śiwatatwa tunggal,\n"
            "Bhinnêka tunggal ika tan hana dharma mangrwa."
        ),
    },
    {
        "label": "🔥 Wedhatama",
        "title": "Serat Wedhatama",
        "author": "K.G.P.A.A. Mangkunegara IV",
        "meta": "Pupuh Pangkur · Jawa Baru, abad ke-19",
        "text": (
            "Mingkar mingkuring angkara,\n"
            "akarana karenan mardi siwi,\n"
            "sinawung resmining kidung,\n"
            "sinuba sinukarta,\n"
            "mrih kretarta pakartining ngelmu luhung,\n"
            "kang tumrap neng tanah Jawa,\n"
            "agama ageming aji."
        ),
    },
]

# ------------------------------------------------------------------
# DATA: CONTOH KALIMAT UNTUK TAB GUBAH
# ------------------------------------------------------------------
GUBAH_SAMPLES = [
    ("👑 Kuasa itu titipan", "Jangan sombong karena berkuasa, sebab kekuasaan hanyalah titipan yang suatu saat akan diambil kembali."),
    ("🌊 Ingat asal-usul", "Hidup ini sementara. Ingatlah dari mana kita berasal dan ke mana kita akan kembali."),
    ("💞 Cinta tulus", "Cinta yang tulus tidak menuntut balasan, ia mengalir seperti air yang menghidupi tanah."),
]

# ------------------------------------------------------------------
# DATA: PEDOMAN METRUM TEMBANG MACAPAT (guru wilangan, guru lagu)
# ------------------------------------------------------------------
MACAPAT = {
    "Dhandhanggula": [(10, "i"), (10, "a"), (8, "e"), (7, "u"), (9, "i"), (7, "a"), (6, "u"), (8, "a"), (12, "i"), (7, "a")],
    "Sinom": [(8, "a"), (8, "i"), (8, "a"), (8, "i"), (7, "i"), (8, "u"), (7, "a"), (8, "i"), (12, "a")],
    "Pangkur": [(8, "a"), (11, "i"), (8, "u"), (7, "a"), (12, "u"), (8, "a"), (8, "i")],
    "Kinanthi": [(8, "u"), (8, "i"), (8, "a"), (8, "i"), (8, "a"), (8, "i")],
    "Asmaradana": [(8, "i"), (8, "a"), (8, "e"), (8, "a"), (7, "a"), (8, "u"), (8, "a")],
    "Mijil": [(10, "i"), (6, "o"), (10, "e"), (10, "i"), (6, "i"), (6, "u")],
    "Maskumambang": [(12, "i"), (6, "a"), (8, "i"), (8, "a")],
    "Durma": [(12, "a"), (7, "i"), (6, "a"), (7, "a"), (8, "i"), (5, "a"), (7, "i")],
    "Pocung": [(12, "u"), (6, "a"), (8, "i"), (12, "a")],
    "Gambuh": [(7, "u"), (10, "u"), (12, "i"), (8, "u"), (8, "o")],
    "Megatruh": [(12, "u"), (8, "i"), (8, "u"), (8, "i"), (8, "o")],
}

RAGAM_OPTIONS = {
    "Jawa Kuno / Kawi": "Jawa Kuno (Kawi) dengan kosakata serapan Sanskerta bergaya kakawin",
    "Jawa Tengahan": "Jawa Tengahan (gaya kidung, masa Majapahit akhir)",
    "Jawa Baru Sastra": "Jawa Baru sastra tinggi (bahasa tembang gaya Wedhatama / Wulangreh), memakai kosakata kawi secukupnya",
}

BENTUK_OPTIONS = [
    "Gancaran (prosa puitis)",
    "Tembang Macapat",
    "Gaya Kakawin (bait 4 baris)",
]

NADA_OPTIONS = [
    "Filosofis & kontemplatif",
    "Nasihat & keutamaan hidup",
    "Spiritual / religius",
    "Kepemimpinan & kebijaksanaan",
    "Romantis & lembut",
    "Duka & perenungan",
]


def macapat_spec(pupuh: str) -> str:
    rows = MACAPAT[pupuh]
    parts = [f"baris {i}: {n} suku kata, berakhir vokal {v}" for i, (n, v) in enumerate(rows, 1)]
    return f"pupuh {pupuh}, {len(rows)} baris. Aturan: " + "; ".join(parts)


# ------------------------------------------------------------------
# STATE & CALLBACK
# ------------------------------------------------------------------
for _k in ("input_text", "gubah_text"):
    if _k not in st.session_state:
        st.session_state[_k] = ""


def set_state(key: str, value: str):
    st.session_state[key] = value


# ------------------------------------------------------------------
# CSS: TEMA "LONTAR EMAS"
# ------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&family=Noto+Sans+Javanese:wght@400;700&display=swap');

:root {
  --gold: #D4A857;
  --gold-soft: #E8C98A;
  --ink: #14110F;
  --panel: #1E1915;
  --line: #3A3027;
  --text: #EDE4D3;
  --muted: #A89B86;
}

html, body, [class*="css"] { font-family: 'Inter', 'Noto Sans Javanese', sans-serif; }

.stApp {
  background:
    radial-gradient(900px 500px at 50% -8%, rgba(212,168,87,0.16) 0%, transparent 70%),
    radial-gradient(700px 400px at 100% 100%, rgba(111,165,143,0.08) 0%, transparent 70%),
    var(--ink);
  color: var(--text);
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.2rem; max-width: 760px; }

/* ---------- HERO ---------- */
.hero {
  text-align: center;
  padding: 2rem 1rem 1.4rem;
  margin-bottom: 1.2rem;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: linear-gradient(160deg, rgba(212,168,87,0.12), rgba(212,168,87,0.02) 55%, transparent);
  box-shadow: 0 10px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
}
.hero .aksara {
  font-family: 'Noto Sans Javanese', serif;
  font-size: 1.45rem;
  color: var(--gold);
  letter-spacing: 0.08em;
  opacity: 0.95;
}
.hero .title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  margin: 0.15rem 0 0.1rem;
  background: linear-gradient(90deg, #F6E3B4, #D4A857 50%, #F6E3B4);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero .subtitle {
  color: var(--muted);
  font-size: 0.92rem;
  max-width: 500px;
  margin: 0.3rem auto 0.9rem;
}
.orn { color: var(--gold); text-align: center; letter-spacing: 0.7em; opacity: 0.7; margin: 0.4rem 0; font-size: 0.8rem; }
.pills span {
  display: inline-block;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.22rem 0.8rem;
  margin: 0.15rem;
  font-size: 0.76rem;
  color: var(--gold-soft);
  background: rgba(212,168,87,0.07);
}

/* ---------- TAB ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 0.2rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { color: var(--muted); font-weight: 500; padding: 0.6rem 0.8rem; }
.stTabs [aria-selected="true"] { color: var(--gold) !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--gold) !important; }

/* ---------- SECTION LABEL ---------- */
.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.55rem;
  font-weight: 600;
  color: var(--gold-soft);
  margin: 0.8rem 0 0.2rem;
}
.hint { color: var(--muted); font-size: 0.82rem; margin-bottom: 0.4rem; }

/* ---------- INPUT ---------- */
.stTextArea label p, .stRadio label p, .stSelectbox label p, .stCheckbox label p {
  color: var(--muted) !important; font-size: 0.82rem !important;
}
.stTextArea [data-baseweb="textarea"] {
  background: #17130F !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
}
.stTextArea [data-baseweb="textarea"]:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(212,168,87,0.18) !important;
}
.stTextArea textarea {
  background: transparent !important;
  color: var(--text) !important;
  font-family: 'Cormorant Garamond', 'Noto Sans Javanese', serif !important;
  font-size: 1.22rem !important;
  line-height: 1.6 !important;
}
.stTextArea textarea::placeholder { color: #6F6556 !important; font-style: italic; }

/* ---------- TOMBOL ---------- */
.stButton > button, .stDownloadButton > button {
  width: 100%;
  border-radius: 12px;
  font-weight: 600;
  transition: all .18s ease;
}
.stButton > button[kind="secondary"],
[data-testid="stBaseButton-secondary"] {
  background: rgba(212,168,87,0.07);
  color: var(--gold-soft);
  border: 1px solid var(--line);
  font-size: 0.85rem;
}
.stButton > button[kind="secondary"]:hover,
[data-testid="stBaseButton-secondary"]:hover {
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(212,168,87,0.14);
  transform: translateY(-1px);
}
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg, #E8C98A 0%, #D4A857 45%, #B98A3A 100%);
  color: #1A130A;
  border: none;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  letter-spacing: 0.02em;
  box-shadow: 0 6px 20px rgba(212,168,87,0.28);
}
.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(212,168,87,0.38);
  color: #1A130A;
}
.stDownloadButton > button {
  background: transparent;
  color: var(--gold-soft);
  border: 1px solid var(--gold);
}
.stDownloadButton > button:hover { background: rgba(212,168,87,0.12); color: var(--gold); }

/* ---------- KARTU HASIL ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: linear-gradient(180deg, #1F1A15, #19150F);
  border: 1px solid var(--line) !important;
  border-left: 4px solid var(--gold) !important;
  border-radius: 14px !important;
  box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
  font-family: 'Cormorant Garamond', serif;
  color: var(--gold-soft);
  font-size: 1.45rem;
  font-weight: 700;
  margin-top: 1rem;
  padding-bottom: 0.2rem;
  border-bottom: 1px solid var(--line);
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li { color: var(--text); line-height: 1.7; }
[data-testid="stVerticalBlockBorderWrapper"] strong { color: var(--gold-soft); }
[data-testid="stVerticalBlockBorderWrapper"] em { color: #CFE3D8; }

/* ---------- EXPANDER ---------- */
[data-testid="stExpander"] {
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  background: rgba(30,25,21,0.7);
}
[data-testid="stExpander"] summary p { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: var(--gold-soft); font-weight: 600; }

.excerpt {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.15rem;
  line-height: 1.7;
  color: var(--text);
  border-left: 3px solid var(--gold);
  padding: 0.2rem 0 0.2rem 1rem;
  margin: 0.4rem 0 0.8rem;
  white-space: pre-line;
}
.meta { color: var(--muted); font-size: 0.8rem; }
.disclaimer { color: var(--muted); font-size: 0.76rem; text-align: center; margin-top: 1rem; }
hr { border-color: var(--line); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
HERO = """
<div class="hero">
<div class="aksara">ꦮꦱ꧀ꦏꦶꦠ ꦱꦱ꧀ꦠꦿ</div>
<div class="title">Waskita Sastra</div>
<div class="subtitle">Menyingkap makna naskah Jawa Kuno, Kawi, dan sastra Nusantara, serta menggubah kalimat Anda menjadi sastra Jawa dengan bantuan kecerdasan buatan.</div>
<div class="orn">✦ ✦ ✦</div>
<div class="pills">
<span>📖 Terjemahan &amp; Bedah Makna</span>
<span>✍️ Gubah ke Sastra Kuno</span>
<span>🌌 Rujukan Filosofi</span>
</div>
</div>
"""
st.markdown(HERO, unsafe_allow_html=True)

# ------------------------------------------------------------------
# TAB
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Telaah", "✍️ Gubah", "📚 Pustaka", "ℹ️ Tentang"])

# ================= TAB 1: TELAAH =================
with tab1:
    st.markdown('<div class="section-title">Telaah Naskah</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Tempel teks Jawa Kuno / Kawi / bait sastra untuk diterjemahkan dan dibedah maknanya, '
        "atau coba salah satu naskah contoh.</div>",
        unsafe_allow_html=True,
    )

    chip_cols = st.columns(len(SAMPLES))
    for i, s in enumerate(SAMPLES):
        with chip_cols[i]:
            st.button(s["label"], key=f"chip_{i}", on_click=set_state, args=("input_text", s["text"]))

    user_input = st.text_area(
        "Teks Jawa Kuno / Kawi / bait sastra:",
        key="input_text",
        height=190,
        max_chars=3000,
        placeholder="Ketik atau tempel bait sastra di sini...\n\nContoh: Amenangi jaman edan, ewuh aya ing pambudi...",
    )

    depth = st.radio(
        "Kedalaman analisis",
        ["Ringkas", "Mendalam"],
        index=1,
        horizontal=True,
        key="depth",
    )

    col_go, col_clear = st.columns([3, 1])
    with col_go:
        go_telaah = st.button("✨ Terjemahkan & Bedah Makna", type="primary", key="go_telaah")
    with col_clear:
        st.button("🗑 Hapus", key="clear_telaah", on_click=set_state, args=("input_text", ""))

    if go_telaah:
        if not user_input.strip():
            st.warning("Mohon masukkan teks terlebih dahulu.")
        elif client is None:
            st.error("API Key belum dikonfigurasi.")
        else:
            if depth == "Ringkas":
                format_rule = (
                    "Berikan jawaban RINGKAS (sekitar 150-250 kata) dengan tiga bagian:\n"
                    "### Terjemahan Bebas\n### Kosakata Penting\n### Makna & Filosofi"
                )
            else:
                format_rule = (
                    "Berikan jawaban MENDALAM dengan tiga bagian:\n"
                    "### Terjemahan Bebas (Bahasa Indonesia)\nTerjemahan utuh yang puitis namun akurat.\n"
                    "### Bedah Kosakata & Analisis Per Baris\nUraikan kata penting (kawi/kuna) beserta arti harfiahnya.\n"
                    "### Nilai Filosofi & Kosmologi\nMakna mendalam atau sasmita di balik teks."
                )

            prompt = f"""
Bertindaklah sebagai ahli filologi, sastra Jawa Kuno, dan Kawi Nusantara.
Analisis teks sastra berikut:
\"\"\"
{user_input}
\"\"\"

{format_rule}

Gunakan judul bagian dengan format "###" (jangan "#" atau "##").
Jika ada kata atau bagian yang Anda tidak yakin, katakan terus terang.
"""
            with st.spinner("Membaca lontar... menimbang kata dan makna..."):
                text, used_model, err = ask_gemini(prompt)

            if text:
                st.session_state["result"] = {"text": text, "model": used_model, "source": user_input}
            else:
                st.session_state.pop("result", None)
                st.error(f"Gagal menghubungi Gemini: {err}")

    res = st.session_state.get("result")
    if res:
        st.markdown('<div class="orn">✦ ✦ ✦</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📖 Hasil Telaah</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(res["text"])
        st.caption(f"Dianalisis dengan {res['model']}")

        export_md = (
            "# Waskita Sastra - Hasil Telaah\n\n"
            "## Teks Asli\n\n"
            + "\n".join("> " + line for line in res["source"].splitlines())
            + "\n\n---\n\n"
            + res["text"]
        )
        st.download_button(
            "⬇ Simpan hasil (.md)",
            data=export_md,
            file_name="waskita-sastra-telaah.md",
            mime="text/markdown",
            key="dl_telaah",
        )
        st.markdown(
            '<div class="disclaimer">Hasil AI dapat keliru, terutama pada teks Kawi/Jawa Kuno. '
            "Verifikasi dengan kamus (mis. Old Javanese-English Dictionary karya Zoetmulder) atau ahli filologi.</div>",
            unsafe_allow_html=True,
        )

# ================= TAB 2: GUBAH =================
with tab2:
    st.markdown('<div class="section-title">Gubah ke Sastra Jawa</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Tulis kalimat dalam bahasa Indonesia (atau bahasa lain, otomatis dikenali). '
        "Aplikasi akan menggubahnya menjadi sastra Jawa, lengkap dengan terjemahan balik, alasan pilihan kata, "
        "dan rujukan filosofinya.</div>",
        unsafe_allow_html=True,
    )

    g_cols = st.columns(len(GUBAH_SAMPLES))
    for i, (label, sentence) in enumerate(GUBAH_SAMPLES):
        with g_cols[i]:
            st.button(label, key=f"gchip_{i}", on_click=set_state, args=("gubah_text", sentence))

    gubah_input = st.text_area(
        "Kalimat atau gagasan yang ingin digubah:",
        key="gubah_text",
        height=140,
        max_chars=1500,
        placeholder="Tulis kalimat, pesan, atau gagasan Anda di sini...\n\nContoh: Hidup ini sementara, ingatlah asal dan tujuan kita.",
    )

    c1, c2 = st.columns(2)
    with c1:
        ragam = st.selectbox("Ragam bahasa", list(RAGAM_OPTIONS.keys()), key="ragam")
    with c2:
        bentuk = st.selectbox("Bentuk karya", BENTUK_OPTIONS, key="bentuk")

    pupuh = None
    if bentuk == "Tembang Macapat":
        pupuh = st.selectbox("Pupuh (metrum macapat)", list(MACAPAT.keys()), key="pupuh")

    nada = st.selectbox("Nada & tema", NADA_OPTIONS, key="nada")
    pakai_aksara = st.checkbox("Sertakan aksara Jawa (Hanacaraka), eksperimental", key="pakai_aksara")

    col_go2, col_clear2 = st.columns([3, 1])
    with col_go2:
        go_gubah = st.button("✍️ Gubah Menjadi Sastra", type="primary", key="go_gubah")
    with col_clear2:
        st.button("🗑 Hapus", key="clear_gubah", on_click=set_state, args=("gubah_text", ""))

    if go_gubah:
        if not gubah_input.strip():
            st.warning("Mohon tulis kalimat yang ingin digubah terlebih dahulu.")
        elif client is None:
            st.error("API Key belum dikonfigurasi.")
        else:
            if bentuk == "Tembang Macapat":
                bentuk_detail = "Tembang Macapat, " + macapat_spec(pupuh)
                catatan_bentuk = (
                    "### Catatan Metrum\n"
                    "Tuliskan jumlah suku kata dan vokal akhir setiap baris gubahan, lalu bandingkan dengan aturan pupuh. "
                    "Jika ada baris yang belum sesuai, tulis terus terang barisnya dan seberapa besar penyimpangannya."
                )
            elif bentuk == "Gaya Kakawin (bait 4 baris)":
                bentuk_detail = (
                    "Gaya kakawin: satu atau dua bait, masing-masing 4 baris, dengan irama berimbang dan "
                    "diksi bergaya kakawin. Tidak perlu memenuhi metrum guru-laghu yang ketat."
                )
                catatan_bentuk = (
                    "### Catatan Bentuk\n"
                    "Jelaskan singkat bahwa gubahan ini bergaya kakawin namun tidak memenuhi metrum guru-laghu ketat."
                )
            else:
                bentuk_detail = "Gancaran: prosa puitis 3-6 kalimat, dengan irama dan paralelisme khas sastra Jawa."
                catatan_bentuk = ""

            aksara_rule = (
                "\n### Aksara Jawa (Hanacaraka)\n"
                "Tulis gubahan dalam aksara Jawa Unicode. Ini eksperimental; jika tidak yakin dengan penulisannya, "
                "katakan terus terang."
                if pakai_aksara
                else ""
            )

            prompt = f"""
Bertindaklah sebagai pujangga dan ahli filologi Jawa Kuno (Kawi), sekaligus guru tembang macapat.

TUGAS: Gubahlah teks berikut menjadi sastra Jawa. Teks asal boleh berbahasa apa pun; kenali sendiri bahasanya,
pahami maknanya, lalu gubah.
\"\"\"
{gubah_input}
\"\"\"

SPESIFIKASI
- Ragam bahasa: {RAGAM_OPTIONS[ragam]}
- Bentuk: {bentuk_detail}
- Nada & tema: {nada}

ATURAN
- Pertahankan makna asli teks; boleh memperindah, jangan membalik atau menambah gagasan yang bertentangan.
- Pakai kosakata Jawa Kuno/kawi yang Anda yakini benar. Tandai kata yang kurang Anda yakini dengan tanda (?).
- Jangan mengarang kutipan naskah. Jangan mengaku gubahan ini sebagai naskah asli kuno; ini gubahan baru.
- Gunakan judul bagian dengan format "###" (jangan "#" atau "##").

FORMAT JAWABAN (urut):
### Gubahan
(hasil gubahan; untuk macapat dan kakawin, tulis satu baris per baris)
### Terjemahan Balik (Bahasa Indonesia)
(terjemahan gubahan ke bahasa Indonesia agar pengguna bisa memeriksa kesetiaan makna)
### Pilihan Kata & Alasan Puitis
(daftar kata kunci: kata, arti, dan alasan pemilihannya: nuansa, asal kata, bunyi/irama, kaitan dengan sasmita)
### Rujukan Filosofi & Sastra
(2-3 konsep filosofi Jawa yang selaras dengan isi teks, misalnya dari Wedhatama, Wulangreh, Kalatidha, Serat Centhini, \
Dewaruci, Kakawin Sutasoma, Arjunawiwaha, atau Bharatayuddha, beserta kaitannya secara singkat. \
Jangan mengutip bait secara harfiah kecuali Anda sangat yakin; jika tidak yakin, jelaskan temanya saja dan tulis \
"perlu diverifikasi".)
{catatan_bentuk}{aksara_rule}
"""
            with st.spinner("Menggubah bait... memilih kata dan irama..."):
                text, used_model, err = ask_gemini(prompt)

            if text:
                st.session_state["result_gubah"] = {
                    "text": text,
                    "model": used_model,
                    "source": gubah_input,
                    "ragam": ragam,
                    "bentuk": bentuk + (f" ({pupuh})" if pupuh else ""),
                    "nada": nada,
                }
            else:
                st.session_state.pop("result_gubah", None)
                st.error(f"Gagal menghubungi Gemini: {err}")

    resg = st.session_state.get("result_gubah")
    if resg:
        st.markdown('<div class="orn">✦ ✦ ✦</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✍️ Hasil Gubahan</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(resg["text"])
        st.caption(f"{resg['ragam']} · {resg['bentuk']} · {resg['nada']} · {resg['model']}")

        export_g = (
            "# Waskita Sastra - Hasil Gubahan\n\n"
            "## Teks Asal\n\n"
            + "\n".join("> " + line for line in resg["source"].splitlines())
            + f"\n\n*{resg['ragam']} · {resg['bentuk']} · {resg['nada']}*\n\n---\n\n"
            + resg["text"]
        )
        st.download_button(
            "⬇ Simpan gubahan (.md)",
            data=export_g,
            file_name="waskita-sastra-gubahan.md",
            mime="text/markdown",
            key="dl_gubah",
        )
        st.markdown(
            '<div class="disclaimer">Ini gubahan baru hasil AI, bukan naskah kuno asli. Kosakata Kawi dan metrum bisa '
            "keliru; kata bertanda (?) perlu diperiksa. Verifikasi dengan kamus Zoetmulder atau ahli sastra Jawa "
            "sebelum dipublikasikan.</div>",
            unsafe_allow_html=True,
        )

# ================= TAB 3: PUSTAKA =================
with tab3:
    st.markdown('<div class="section-title">Pustaka Naskah Klasik</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Pilih naskah, lalu tekan "Muat ke Telaah" dan kembali ke tab Telaah.</div>',
        unsafe_allow_html=True,
    )

    for i, s in enumerate(SAMPLES):
        with st.expander(f"{s['title']}  ·  {s['author']}"):
            st.markdown(f'<div class="meta">{s["meta"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="excerpt">{s["text"]}</div>', unsafe_allow_html=True)
            if st.button("Muat ke Telaah", key=f"load_{i}", on_click=set_state, args=("input_text", s["text"])):
                st.toast("Teks dimuat. Buka tab Telaah untuk menganalisis.", icon="📜")

# ================= TAB 4: TENTANG =================
with tab4:
    st.markdown('<div class="section-title">Tentang Waskita Sastra</div>', unsafe_allow_html=True)
    st.write(
        "Waskita Sastra membantu peneliti, penggiat budaya, dan masyarakat umum mengkaji teks sastra "
        "Nusantara: menerjemahkan, membedah kosakata, menggali lapisan makna filosofisnya, dan menggubah "
        "kalimat modern menjadi sastra Jawa."
    )
    st.markdown('<div class="orn">✦ ✦ ✦</div>', unsafe_allow_html=True)
    st.caption("Dibangun dengan Python, Streamlit, & Gemini AI · Mobile Optimized")
