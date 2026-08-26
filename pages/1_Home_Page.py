import streamlit as st
import database as db

st.set_page_config(page_title="About Us - Info", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

st.markdown("""
    <style>
        .hero-container {
            background-image: linear-gradient(rgba(0, 42, 135, 0.65), rgba(0, 42, 135, 0.65)), 
                              url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            padding: 120px 20px;
            text-align: center;
            color: white;
            border-radius: 12px;
            margin-bottom: 40px;
        }
        .hero-title { font-size: 52px !important; font-weight: 700; color: white !important; font-family: 'Helvetica Neue', Arial; }
        .hero-subtitle { font-size: 20px !important; color: #f8fafc !important; font-weight: 300; }
        
        .service-box {
            background-color: #ffffff; padding: 25px; border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #004687; margin-bottom: 20px;
        }
        .service-title { color: #004687 !important; font-weight: bold; font-size: 18px !important; margin-bottom: 8px; }
    </style>
    
    <div class="hero-container">
        <h1 class="hero-title">Pioneering Home Healthcare</h1>
        <p class="hero-subtitle">Professional Post-Discharge Patient Follow-Up Services</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.write("### Misi & Komitmen Kami")
    st.write(
        "Kami menyediakan perkhidmatan rawatan jururawat bertauliah terus ke rumah anda demi keselesaan fasa pemulihan. "
        "Sistem digital kami membantu mengintegrasikan pemantauan kesihatan pesakit pasca-discaj secara berkala bagi had umur 18-59 tahun."
    )
    
    st.write("<br>### Perkhidmatan Klinikal Utama", unsafe_allow_html=True)
    st.markdown("""
        <div class="service-box"><div class="service-title">Wound Care Management</div><p style='margin:0; font-size:14px; color:#475569;'>Penjagaan luka kronik pasca-pembedahan secara intensif di rumah pesakit.</p></div>
        <div class="service-box"><div class="service-title">Vital Signs Tracking</div><p style='margin:0; font-size:14px; color:#475569;'>Pemeriksaan dan analisis berkala tekanan darah, kadar nadi, dan tahap gula darah.</p></div>
    """, unsafe_allow_html=True)

with col2:
    st.write("### Hubungi Talian Sokongan")
    st.markdown("""
        <div style='background-color: #f8fafc; padding: 30px; border-radius: 8px; border: 1px solid #e2e8f0;'>
            <h4 style='margin-top:0; color:#0f172a;'>Talian Pertanyaan Pusat 24 Jam</h4>
            <p style='font-size:26px; color:#dc2626; font-weight:bold; margin:10px 0;'>1-300-88-NURSE</p>
            <p style='font-size:14px; color:#475569;'><b>Emel Rasmi:</b> admin@homenursing.com.my</p>
            <p style='font-size:14px; color:#475569;'><b>Pejabat Utama:</b> Blok Kesihatan, Pusat Bandar Shah Alam, Selangor.</p>
        </div>
    """, unsafe_allow_html=True)


