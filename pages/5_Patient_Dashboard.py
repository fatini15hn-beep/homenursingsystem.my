import streamlit as st
import database as db

# Sembunyikan sidebar asal dan suntik navbar rekaan sendiri
st.set_page_config(page_title="Patient Dashboard", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

# Semakan sekatan akses peranan (Hanya peranan Patient dibenarkan masuk)
if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Patient":
    st.error("🚫 Access Denied! Please log in as a patient to view treatment records.")
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
    st.write("### 👥 1. Patient Profile & Basic Information")
    df_pt = db.get_patients_df()
    
    if not df_pt.empty:
        # Susun semula kolum dan tukar nama pengepala (header) mengikut kesesuaian borang
        df_pt_clean = df_pt[['id', 'name', 'age', 'gender', 'phone', 'illness', 'status']]
        df_pt_clean.columns = ['ID Pesakit', 'Nama Penuh Pesakit', 'Umur (Tahun)', 'Jantina', 'No. Telefon / Contact', 'Jenis Penyakit Kronik', 'Status Kes Perawatan']
        
        # Memaparkan keseluruhan data profil pesakit
        st.dataframe(df_pt_clean, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No patient profile data found in the database.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # 2. PAPARAN SEJARAH KLINIKAL / LAPORAN PEMERIKSAAN RAWATAN (BERDASARKAN BORANG JURURAWAT)
    # =========================================================================
    st.write("### 🩺 2. Clinical Examination Record & Treatment Recommendations")
    df_ass = db.get_assessments_df()
    
    if not df_ass.empty:
        # Susun kolum laporan rawatan dan gunakan nama berdasarkan Borang Data Perawatan
        df_ass_clean = df_ass[['id', 'patient_id', 'blood_pressure', 'pulse_rate', 'blood_sugar', 'wound_condition', 'nurse_memo']]
        df_ass_clean.columns = [
            'Report No.', 
            'Patient ID', 
            'Blood Pressure (BP Reading)', 
            'Pulse Rate (pulses/minute)', 
            'Blood Sugar Levels', 
            'Chief Complaint / Wound Condition', 
            'Diagnosis & Treatment Recommendations'
        ]
        
        # Memaparkan keseluruhan data klinikal tanpa sebarang sekatan tapisan
        st.dataframe(df_ass_clean, use_container_width=True, hide_index=True)
        
        # PEMBETULAN: Menutup tag HTML markdown yang terpotong sebelum ini dengan sempurna
        st.markdown("""
            <div style='background-color: #f1f5f9; padding: 15px; border-left: 5px solid #0284c7; border-radius: 4px; margin-top: 15px;'>
                <p style='margin: 0; font-size: 13px; color: #334155; font-weight: bold;'>
                    📝 Therapy/Medication Treatment Consent Note:
                </p>
                <p style='margin: 3px 0 0 0; font-size: 13px; color: #475569; font-style: italic;'>
                    "All the above patients are deemed to have consented to receive the treatment provided by the healthcare provider (Nurse) who are on duty from their respective homes."
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No clinical data records, blood pressure readings, or diagnostic suggestions were found in the database at this time.")




