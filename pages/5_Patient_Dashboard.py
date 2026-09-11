import streamlit as st
import database as db

# Sembunyikan sidebar asal dan suntik navbar rekaan sendiri
st.set_page_config(page_title="Patient Dashboard", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

# Semakan sekatan akses peranan (Hanya peranan Patient dibenarkan masuk)
if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Patient":
    st.error("🚫 Akses Disekat! Sila Log Masuk sebagai Pesakit untuk melihat rekod rawatan.")
else:
    # Header Dashboard Utama
    st.markdown(f"""
        <div style='background-color: #004687; padding: 20px; border-radius: 10px; margin-bottom: 25px; color: white;'>
            <h2 style='margin: 0; color: white;'>🏥 PORTAL PESAKIT - SEMAKAN DATA PERAWATAN PESAKIT</h2>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Log masuk aktif: <b>{st.session_state.username_display}</b> | Peranan: Pesakit Awam</p>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # 1. PAPARAN SENARAI KESELURUHAN PROFIL PESAKIT
    # =========================================================================
    st.write("### 👥 1. Maklumat Profil & Maklumat Asas Pesakit")
    df_pt = db.get_patients_df()
    
    if not df_pt.empty:
        # Susun semula kolum dan tukar nama pengepala (header) mengikut kesesuaian borang
        df_pt_clean = df_pt[['id', 'name', 'age', 'gender', 'phone', 'illness', 'status']]
        df_pt_clean.columns = ['ID Pesakit', 'Nama Penuh Pesakit', 'Umur (Tahun)', 'Jantina', 'No. Telefon / Contact', 'Jenis Penyakit Kronik', 'Status Kes Perawatan']
        
        # Memaparkan keseluruhan data profil pesakit
        st.dataframe(df_pt_clean, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Tiada data profil pesakit dijumpai dalam pangkalan data.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # 2. PAPARAN SEJARAH KLINIKAL / LAPORAN PEMERIKSAAN RAWATAN (BERDASARKAN BORANG JURURAWAT)
    # =========================================================================
    st.write("### 🩺 2. Rekod Pemeriksaan Klinikal & Cadangan Perawatan")
    df_ass = db.get_assessments_df()
    
    if not df_ass.empty:
        # Susun kolum laporan rawatan dan gunakan nama berdasarkan Borang Data Perawatan
        df_ass_clean = df_ass[['id', 'patient_id', 'blood_pressure', 'pulse_rate', 'blood_sugar', 'wound_condition', 'nurse_memo']]
        df_ass_clean.columns = [
            'No. Laporan', 
            'ID Pesakit', 
            'Tekanan Darah (Bacaan BP)', 
            'Kadar Nadi (Nadi / minit)', 
            'Tahap Gula Darah', 
            'Keluhan Utama / Kondisi Luka', 
            'Diagnosa & Cadangan Perawatan'
        ]
        
        # Memaparkan keseluruhan data klinikal tanpa sebarang sekatan tapisan
        st.dataframe(df_ass_clean, use_container_width=True, hide_index=True)
        
        # PEMBETULAN: Menutup tag HTML markdown yang terpotong sebelum ini dengan sempurna
        st.markdown("""
            <div style='background-color: #f1f5f9; padding: 15px; border-left: 5px solid #0284c7; border-radius: 4px; margin-top: 15px;'>
                <p style='margin: 0; font-size: 13px; color: #334155; font-weight: bold;'>
                    📝 Nota Persetujuan Perawatan Terapi/Pengubatan:
                </p>
                <p style='margin: 3px 0 0 0; font-size: 13px; color: #475569; font-style: italic;'>
                    "Semua pesakit di atas dianggap telah bersetuju untuk menerima rawatan yang diberikan oleh perawat (Nurse) yang bertugas di rumah masing-masing."
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Tiada rekod data klinikal, bacaan BP, atau cadangan diagnosa dijumpai dalam pangkalan data buat masa ini.")




