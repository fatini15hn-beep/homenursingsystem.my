import streamlit as st
import database as db
import datetime
import email_service

# =========================================================
# CONFIGURATION & TOP NAVIGATION
# =========================================================
st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Admin diletakkan ID akaun khas ('Admin01') untuk log navigasi
db.inject_top_navbar(user_id="Admin01")

# =========================================================
# ADMIN ACCESS PROTECTION
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "username_display" not in st.session_state:
    st.session_state.username_display = None

if not st.session_state.logged_in or st.session_state.user_role != "Admin":
    st.error("🚫 Akses Disekat! Halaman ini hanya boleh dibuka oleh Admin.")
    st.stop()

# =========================================================
# ADMIN DASHBOARD HEADER
# =========================================================
st.write(f"## Admin Dashboard - Pengurusan Hub (User: {st.session_state.username_display})")
st.markdown("---")

# =========================================================
# 3 MAIN MANAGEMENT TABS
# =========================================================
menu = st.tabs([
    "Pengurusan Pesakit",
    "Pengurusan Jururawat",
    "🗓️ Jadual Temujanji Lawatan"
])

# =========================================================
# TAB 1 - PATIENT MANAGEMENT
# =========================================================
with menu[0]:
    st.write("### Pendaftaran Pesakit Pasca-Discaj Baru")
    st.info("Semua maklumat pendaftaran pesakit wajib diisi oleh Admin mengikut protokol pusat.")

    with st.form("admin_add_patient", clear_on_submit=True):
        pt_id = st.text_input("ID Pesakit", placeholder="Contoh: P004")
        name = st.text_input("Nama Penuh Pesakit")
        
        # ➕ TAMBAH RUANGAN EMAIL PESAKIT DI SINI:
        email = st.text_input("Email Pesakit", placeholder="Contoh: pesakit@gmail.com")
        
        age = st.number_input("Umur Pesakit (18 - 59 tahun)", min_value=18, max_value=59, value=25)
        gender = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        phone = st.text_input("Nombor Telefon Bimbit", placeholder="Contoh: 0123456789")
        illness = st.text_area("Jenis Penyakit / Diagnosis Pesakit")
        submitted = st.form_submit_button("Daftar Masuk Pesakit", type="primary")

        if submitted:
            if pt_id and name and phone and illness:
                clean_phone = phone.strip()
                if not clean_phone.isdigit() or not (10 <= len(clean_phone) <= 11):
                    st.error("⚠️ Ralat! Nombor telefon Malaysia mestilah antara 10-11 digit.")
                else:
                    # ➕ Menghantar nilai 'email' yang diisi ke fungsi database
                    success, msg = db.add_patient(pt_id, name, age, gender, clean_phone, illness, email)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("⚠️ Sila lengkapkan kesemua ruangan maklumat!")

    st.markdown("---")
    st.write("### 📊 Pangkalan Data Senarai Pesakit Berdaftar")

    df_patients = db.get_patients_df()
    if not df_patients.empty:
        st.dataframe(df_patients, use_container_width=True, hide_index=True)
    else:
        st.info("Tiada pesakit berdaftar buat masa ini.")

# =========================================================
# TAB 2 - NURSE MANAGEMENT
# =========================================================
with menu[1]:
    st.write("### Pangkalan Data Kakitangan Jururawat")

    # Paparkan Maklumat Fixed bagi Nurse Aina
    st.write("#### 👩‍⚕️ Nurse Aina")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Staff No:** N001")
    with col2:
        st.write("**Contact:** 0112223333")
    with col3:
        st.write("**Zone:** Zon A")

    st.markdown("---")

    # Paparkan Maklumat Fixed bagi Nurse Fatimah
    st.write("#### 👩‍⚕️ Nurse Fatimah")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Staff No:** N002")
    with col2:
        st.write("**Contact:** 0144445555")
    with col3:
        st.write("**Zone:** Zon B")

    st.markdown("---")
    st.success("✓ Jumlah Jururawat Berdaftar: 2")

# =========================================================
# TAB 3 - APPOINTMENT MANAGEMENT
# =========================================================
with menu[2]:
    st.write("### 📅 Tetapkan Jadual & Tarikh Lawatan Jururawat ke Rumah Pesakit")
    st.info("Admin boleh menetapkan jadual lawatan untuk Nurse Aina atau Nurse Fatimah.")

    df_patients = db.get_patients_df()
    nurse_options = {
        "Nurse Aina (N001)": "N001",
        "Nurse Fatimah (N002)": "N002"
    }

    if df_patients.empty:
        st.warning("Pangkalan data pesakit kosong. Sila daftar pesakit terlebih dahulu di Tab 1.")
    else:
        patient_options = {row["name"]: row["id"] for _, row in df_patients.iterrows()}

        with st.form("add_appointment_form", clear_on_submit=True):
            selected_pt_name = st.selectbox("Pilih Pesakit Pasca-Discaj:", list(patient_options.keys()))
            selected_nurse_name = st.selectbox("Tugaskan Jururawat:", list(nurse_options.keys()))
            visit_date = st.date_input("Pilih Tarikh Lawatan:", datetime.date.today())
            visit_time = st.selectbox("Pilih Slot Waktu Syif:", [
                "09:00 AM (Pagi)",
                "11:30 AM (Pagi)",
                "02:30 PM (Tengah Hari)",
                "05:00 PM (Lewat Petang)"
            ])
            notes = st.text_area("Nota Persediaan Rawatan")
            submitted = st.form_submit_button("Sahkan & Daftar Temujanji Kalendar", type="primary")

            if submitted:
                p_id = patient_options[selected_pt_name]
                n_id = nurse_options[selected_nurse_name]

                # Simpan rekod temujanji ke dalam database SQLite
                success, msg = db.add_appointment(p_id, n_id, visit_date, visit_time, notes)

                if success:
                    notif_title = "📅 Jadual Temujanji Lawatan Baru"
                    notif_msg = f"Anda telah ditugaskan untuk melawat pesakit {selected_pt_name} pada {visit_date} ({visit_time}). Nota: {notes}"
                    
                    if hasattr(db, "create_notification"):
                        db.create_notification(user_id=n_id, title=notif_title, message=notif_msg, notification_type="appointment")
                    else:
                        try:
                            conn = db.get_connection()
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO notifications (user_id, title, message, notification_type) 
                                VALUES (?, ?, ?, ?)
                            """, (n_id, notif_title, notif_msg, "appointment"))
                            conn.commit()
                            conn.close()
                        except Exception:
                            pass
                    
                    if n_id == "N001":
                        target_email = "homenursingsystem1@gmail.com"  
                        nurse_display_name = "Aina"
                    else:
                        target_email = "homenursingsystem1@gmail.com"  
                        nurse_display_name = "Fatimah"
                    
                    # SAMBUNGAN KOD EMAIL SERVICE YANG TERGANTUNG
                    try:
                        email_service.send_appointment_email(
                            nurse_email=target_email,
                            nurse_name=nurse_display_name,
                            patient_name=selected_pt_name,
                            visit_date=str(visit_date),
                            visit_time=visit_time,
                            notes=notes
                        )
                        st.success(f"{msg} Serta e-mel notifikasi tugasan berjaya dihantar ke Nurse {nurse_display_name}!")
                    except Exception as e:
                        st.success(msg)
                        st.warning(f"⚠️ Jadual disimpan tetapi e-mel gagal dihantar kepada jururawat: {str(e)}")
                    st.rerun()
                else:
                    st.error(msg)
