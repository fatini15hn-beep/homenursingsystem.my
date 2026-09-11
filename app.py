import streamlit as st

# 1. KOD STYLE REKA BENTUK (CSS MANTAP)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Box Banner Utama */
    .hero-container {
        padding: 2.5rem;
        background: linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid #E2E8F0;
    }
    
    .hero-title {
        color: #0F4C81 !important;
        font-family: 'Arial Black', sans-serif;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        line-height: 1.1;
        margin-bottom: 5px;
    }
    
    .hero-subtitle {
        color: #1D74B4 !important;
        font-size: 2.3rem !important;
        font-weight: 700 !important;
        margin-bottom: 15px;
    }
    
    .hero-text {
        color: #64748B !important;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 25px;
    }

    /* Menghilangkan border asal kelabu sekeliling gambar Streamlit */
    [data-testid="stImage"] img {
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. PROSES MEMBAHAGIKAN 2 LAJUR (KIRI TEKS, KANAN GAMBAR)
# Lajur kiri diberi ruang lebih besar (rasio 3:2)
col1, col2 = st.columns([3, 2])

with col1:
    # Bagian Teks Hero di sebelah Kiri
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
    
    # Menambah 2 buah butang moden bersambung di bawah teks
    btn_col1, btn_col2 = st.columns([1, 2])
    with btn_col1:
        st.button("Read More →")
    with btn_col2:
        st.button("▶ Watch Video")

with col2:
    # Bagian Gambar Doktor di sebelah Kanan
    # Kita guna gambar doktor medical yang sedia ada di internet secara percuma
    st.image("https://freepik.com", width=320)


