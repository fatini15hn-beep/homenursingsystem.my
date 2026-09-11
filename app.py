import streamlit as st

# 1. KOD STRUKTUR CSS PREMIUM (BINA RUPA MACAM GAMBAR CONTOH)
st.markdown("""
    <style>
    /* Latar belakang putih bersih untuk seluruh aplikasi */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* GAYA HERO SECTION (BAHAGIAN ATAS UTAMA) */
    .hero-container {
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid #E2E8F0;
    }
    
    .hero-title {
        color: #0F4C81 !important;
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 3rem !important;
        font-weight: 800 !important;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        color: #1D74B4 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 20px;
    }
    
    .hero-text {
        color: #64748B !important;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 30px;
        max-width: 600px;
    }
    
    /* REKA BENTUK KAD SERVIS (GRID KAD DI BAHAGIAN BAWAH) */
    .service-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        border-color: #1D74B4;
    }
    
    .card-title {
        color: #0F4C81 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-bottom: 8px;
    }
    
    /* BUTANG PREMIUM CUSTOMLY DESIGNED */
    .stButton>button {
        background-color: #0F4C81 !important;
        color: #FFFFFF !important;
        border-radius: 30px !important; /* Butang bulat tepi macam gambar */
        padding: 0.6rem 2rem !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(15, 76, 129, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #1D74B4 !important;
        box-shadow: 0 4px 15px rgba(29, 116, 180, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 2. STRUKTUR HTML UNTUK TAMPILKAN TEKS HERO UTAMA MENGGUNAKAN CSS DI ATAS
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Medical &</h1>
        <h2 class="hero-subtitle">Health Care Services</h2>
        <p class="hero-text">
            Your health is our top priority. Schedule an appointment with us today 
            to experience world-class home nursing and clinical management tailored just for you.
        </p>
    </div>
""", unsafe_allow_html=True)

