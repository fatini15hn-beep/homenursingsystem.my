import streamlit as st
import database as db

# 1. Pastikan database di-initialize terlebih dahulu
db.initialize_db()

# 2. Set konfigurasi halaman utama
st.set_page_config(
    page_title="Home Nursing System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. Masukkan Top Navigation Bar (HTML yang anda hantar tadi)
db.inject_top_navbar()

# 4. Kandungan Halaman Utama (Portal Main)
st.title("Selamat Datang ke Home Nursing System Portal")
st.subheader("Sistem Pengurusan Lawatan Jururawat untuk Pesakit Selepas Keluar Hospital")

st.markdown("""
Sistem ini direka khas untuk memudahkan pemantauan kesihatan pesakit di rumah, 
pengurusan jadual temujanji jururawat, serta penyampaian arahan memo perubatan secara digital.
""")

st.info("💡 Sila gunakan menu **LOGIN** di bahagian atas untuk masuk ke dashboard anda.")
import streamlit as st

# Kod khas untuk tema Biru & Putih (Medical Theme)
import streamlit as st

# KOD DESIGN VERSI PENUH: TEMA BIRU & PUTIH (TERMASUK SIDEBAR)
st.markdown("""
    <style>
    /* 1. Latar belakang utama warna putih bersih */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 2. Khas untuk SIDEBAR: Tukar jadi warna Biru Gelap (Navy Blue) */
    [data-testid="stSidebar"] {
        background-color: #0F4C81 !important;
    }
    
    /* 3. Tukar semua tulisan & ikon di dalam Sidebar jadi warna PUTIH */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-emotion-cache-qrbm77 {
        color: #FFFFFF !important;
    }
    
    /* 4. Tulisan tajuk utama halaman warna Biru Gelap profesional */
    h1, h2, h3 {
        color: #0F4C81 !important;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
    }
    
    /* 5. Butang (Button) warna Biru dengan tulisan putih */
    .stButton>button {
        background-color: #0F4C81 !important;
        color: #FFFFFF !important;
        border: 1px solid #0F4C81 !important;
        border-radius: 6px !important;
        font-weight: bold;
    }
    
    /* 6. Kesan kilat bila mouse lalu atas butang (Hover) */
    .stButton>button:hover {
        background-color: #1D74B4 !important;
        border-color: #1D74B4 !important;
    }
    
    /* 7. Kotak input borang warna kelabu lembut supaya teks senang dibaca */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)
