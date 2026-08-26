import streamlit as st
import database as db
import datetime

st.set_page_config(page_title="Admin Dashboard", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

if not st.session_state.logged_in or st.session_state.user_role != "Admin":
    st.error("🚫 Akses Disekat! Halaman ini hanya boleh dibuka oleh Admin 'Ali' selepas Log Masuk.")
else:
    st.write(f"## Admin Dashboard - Pengurusan Hub (User: {st.session_state.username_display})")
    
    # Mencipta 3 tab pilihan utama
    menu = st.tabs(["Pengurusan Pesakit", "Pengurusan Jururawat", "🗓️ Jadual Temujanji Lawatan"])
    
    # ─── TAB 1: PENGURUSAN PESAKIT (Guna indeks) ───
    with menu[0]:
        st.write("### Pendaftaran Pesakit Pasca-Discaj Baru")
        st.info("Semua maklumat pendaftaran pesakit wajib diisi oleh Admin Ali sahaja mengikut protokol pusat.")
        
        with st.form("admin_add_patient", clear_on_submit=True):
            pt_id = st.text_input("ID Pesakit (Contoh: P003)")
            name = st.text_input("Nama Penuh Pesakit")
            age = st.number_input("Umur Pesakit (Had SV: 18 - 59)", min_value=0, max_value=120, value=25)
            gender = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
            phone = st.text_input("Nombor Telefon Bimbit (Contoh: 0123456789)")
            illness = st.text_area("Jenis Penyakit / Diagnosis Pesakit")
            
            if st.form_submit_button("Daftar Masuk Pesakit", type="primary"):
                if pt_id and name and phone and illness:
                    clean_phone = phone.strip()
                    if not clean_phone.isdigit() or not (10 <= len(clean_phone) <= 11):
                        st.error("⚠️ Ralat! Nombor telefon Malaysia mestilah antara 10-11 digit.")
                    else:
                        success, msg = db.add_patient(pt_id, name, age, gender, clean_phone, illness)
                        if success: 
                            st.success(msg)
                            st.rerun()
                        else: 
                            st.error(msg)
                else:
                    st.warning("⚠️ Sila lengkapkan kesemua ruangan maklumat!")
                    
        st.markdown("---")
        st.write("### 📊 Pangkalan Data Senarai Pesakit Berdaftar")
        st.dataframe(db.get_patients_df(), use_container_width=True)
        
    # ─── TAB 2: PENGURUSAN JURURAWAT (Guna indeks) ───
    with menu[1]:
        st.write("### Pangkalan Data Kakitangan Jururawat (Tetap)")
        st.dataframe(db.get_nurses_df(), use_container_width=True)
        
    # ─── TAB 3: SISTEM TEMUJANJI KALENDAR (Guna indeks) ───
    with menu[2]:
        st.write("### 📅 Tetapkan Jadual & Tarikh Lawatan Jururawat ke Rumah Pesakit")
        st.info("Pilih pesakit, jururawat bertugas, dan tetapkan tarikh kalendar mengikut syif.")
        
        df_patients = db.get_patients_df()
        df_nurses = db.get_nurses_df()
        
        if df_patients.empty or df_nurses.empty:
            st.warning("Pangkalan data pesakit atau jururawat dikesan kosong. Sila daftar maklumat terlebih dahulu.")
        else:
            patient_options = {row['name']: row['id'] for _, row in df_patients.iterrows()}
            nurse_options = {row['name']: row['id'] for _, row in df_nurses.iterrows()}
            
            with st.form("add_appointment_form", clear_on_submit=True):
                selected_pt_name = st.selectbox("Pilih Pesakit Pasca-Discaj:", list(patient_options.keys()))
                selected_nurse_name = st.selectbox("Tugaskan Jururawat:", list(nurse_options.keys()))
                
                visit_date = st.date_input("Pilih Tarikh Lawatan:", datetime.date.today())
                visit_time = st.selectbox("Pilih Slot Waktu Syif:", ["09:00 AM (Pagi)", "11:30 AM (Tengahari)", "02:30 PM (Petang)", "05:00 PM (Lewat Petang)"])
                notes = st.text_area("Nota Persediaan Rawatan")
                
                if st.form_submit_button("Sahkan & Daftar Temujanji Kalendar", type="primary"):
                    p_id = patient_options[selected_pt_name]
                    n_id = nurse_options[selected_nurse_name]
                    
                    success, msg = db.add_appointment(p_id, n_id, visit_date, visit_time, notes)
                    st.success(msg)
                    st.rerun()
            
            st.markdown("---")
            st.write("### 📊 Jadual Induk Log Temujanji Aktif")
            df_app = db.get_appointments_df()
            if not df_app.empty:
                st.dataframe(df_app, use_container_width=True)
            else:
                st.info("Tiada jadual lawatan aktif berdaftar buat masa ini.")



