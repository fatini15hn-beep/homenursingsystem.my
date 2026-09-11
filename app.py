import streamlit as st

# Kod khas untuk tema Biru & Putih (Medical Theme)
st.markdown("""
    <style>
    /* 1. Latar belakang putih bersih */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 2. Tulisan tajuk warna Biru Gelap (Navy Blue) supaya nampak profesional */
    h1, h2, h3 {
        color: #0F4C81 !important;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
    }
    
    /* 3. Butang (Button) warna Biru Medical dengan tulisan putih */
    .stButton>button {
        background-color: #0F4C81 !important;
        color: #FFFFFF !important;
        border: 1px solid #0F4C81 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* 4. Kesan apabila tetikus lalu atas butang (Hover effect) */
    .stButton>button:hover {
        background-color: #1D74B4 !important;
        color: #FFFFFF !important;
        border-color: #1D74B4 !important;
    }
    
    /* 5. Kotak Input/Borang (Sidebar atau Form) bertema putih kelabu lembut */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
        border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)



