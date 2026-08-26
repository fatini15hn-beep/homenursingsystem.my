import streamlit as st
import database as db

st.set_page_config(page_title="Nurse Dashboard", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

if not st.session_state.logged_in or st.session_state.user_role != "Nurse":
    st.error("🚫 Akses Disekat! Halaman ini hanya untuk kegunaan Jururawat (Aina / Fatimah) sahaja.")
else:
    st.write(f"## Nurse Dashboard - Rutin Kerja Harian (User: {st.session_state.username_display})")
    
    rutin = st.radio("Fasa Rutin Harian Atas Talian:", [
        "1. Shift Check-In & Schedule", 
        "2. Pre-Visit Review (Semak Penyakit Pesakit)", 
        "3. In-Home Assessment Form", 
        "4. Daily Memo & Clock-Out"
    ], horizontal=True)
    
    df_pt = db.get_patients_df()
    
    if rutin == "1. Shift Check-In & Schedule":
        st.write("### Rekod Kehadiran Syif & Jadual")
        if st.button("Punch In / Mulakan Tugasan Harian", type="primary"):
            st.success("✅ Log masuk syif berjaya direkodkan pada jam 08:00 AM.")
        st.dataframe(df_pt[["id", "name", "phone", "illness", "status"]], use_container_width=True)
        
    elif rutin == "2. Pre-Visit Review (Semak Penyakit Pesakit)":
        st.write("### Semakan Profil Sebelum Bertolak")
        if not df_pt.empty:
            selected_pt = st.selectbox("Pilih Nama Pesakit:", df_pt["name"].tolist())
            pt_details = df_pt[df_pt["name"] == selected_pt].iloc[0]
            
            st.info(f"**Pesakit:** {pt_details['name']} | **ID:** {pt_details['id']}")
            st.write(f"🛑 **Jenis Penyakit Dialami:** {pt_details['illness']}")
            st.write(f"📞 Kontak Waris: {pt_details['phone']} | Umur: {pt_details['age']} Tahun")
        else:
            st.info("Tiada data pesakit dijumpai.")
        
    elif rutin == "3. In-Home Assessment Form":
        st.write("### Pengisian Data Klinikal Di Rumah Pesakit")
        if not df_pt.empty:
            with st.form("nurse_assessment", clear_on_submit=True):
                selected_id = st.selectbox("Pilih ID Pesakit untuk Diperiksa", df_pt["id"].tolist())
                bp = st.text_input("Tekanan Darah (mmHg)")
                pulse = st.number_input("Kadar Nadi (bpm)", value=75)
                sugar = st.number_input("Tahap Gula Darah (mmol/L)", value=5.5)
                wound = st.selectbox("Keadaan Luka Terkini", ["Tiada Luka", "Sembuh Baik", "Tanda Jangkitan", "Perlu Dressing Baru"])
                memo = st.text_area("Nota Tambahan Rawatan Jururawat")
                
                if st.form_submit_button("Simpan Data Pemeriksaan", type="primary"):
                    if bp and memo:
                        db.add_assessment(selected_id, bp, pulse, sugar, wound, memo)
                        st.success("✅ Data disimpan secara digital ke dalam database.")
                    else:
                        st.warning("Sila isi data tanda vital.")
        else:
            st.info("Tiada data pesakit sedia ada untuk diperiksa.")
                    
    elif rutin == "4. Daily Memo & Clock-Out":
        st.write("### Log Kerja Digital Syif Hari Ini")
        st.dataframe(db.get_assessments_df(), use_container_width=True)
        if st.button("Punch Out / Clock-Out Syif", type="secondary"):
            st.warning("🔒 Syif kerja ditutup. Sila log keluar.")

