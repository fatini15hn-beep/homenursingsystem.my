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

# =========================================================
# ACCESS CONTROL
# =========================================================
if (
    not st.session_state.get("logged_in")
    or st.session_state.get("user_role") != "Admin"
):
    # TUKAR AYAT DI SINI SAHAJA UNTUK MENGIKUT GAMBAR CONTOH
    st.error("Access Denied! Please log in as an admin to view treatment records.")
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
    "Patient Managementt",
    "Nursing Management",
    "🗓️ Visit Appointment Schedule"
])

# =========================================================
# TAB 1 - PATIENT MANAGEMENT
# =========================================================
with menu[0]:
    st.write("### New Post-Discharge Patient Registration")
    st.info("All patient registration information must be entered by the Admin in accordance with center protocols.")

    with st.form("admin_add_patient", clear_on_submit=True):
        pt_id = st.text_input("ID Petient", placeholder="Contoh: P004")
        name = st.text_input("Patient Full Name")
        
        # ➕ TAMBAH RUANGAN EMAIL PESAKIT DI SINI:
        email = st.text_input("Email Patient", placeholder="Contoh: patient@gmail.com")
        
        age = st.number_input("Patient Age (18 - 59 Years old)", min_value=18, max_value=59, value=25)
        gender = st.selectbox("Gender", ["Lelaki", "Perempuan"])
        phone = st.text_input("Mobile Phone Number", placeholder="Contoh: 0123456789")
        illness = st.text_area("Type of Disease / Patient Diagnosis")
        submitted = st.form_submit_button("Patient Check-in", type="primary")

        if submitted:
            if pt_id and name and phone and illness:
                clean_phone = phone.strip()
                if not clean_phone.isdigit() or not (10 <= len(clean_phone) <= 11):
                    st.error("⚠️ Error! Malaysian phone numbers must be between 10 and 11 digits long.")
                else:
                    # ➕ Menghantar nilai 'email' yang diisi ke fungsi database
                    success, msg = db.add_patient(pt_id, name, age, gender, clean_phone, illness, email)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("⚠️ Please complete all information fields!")

    st.markdown("---")
    st.write("### 📊 Registered Patient List Database")

    df_patients = db.get_patients_df()
    if not df_patients.empty:
        st.dataframe(df_patients, use_container_width=True, hide_index=True)
    else:
        st.info("There are no registered patients at this time.")

# =========================================================
# TAB 2 - NURSE MANAGEMENT
# =========================================================
with menu[1]:
    st.write("### Nursing Staff Database")

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
    st.success("✓ Number of Registered Nurses: 2")

# =========================================================
# TAB 3 - APPOINTMENT MANAGEMENT
# =========================================================
with menu[2]:
    st.write("### 📅 Schedule Nurse Home Visits")
    st.info("The admin can set a visit schedule for Nurse Aina or Nurse Fatimah")

    df_patients = db.get_patients_df()
    nurse_options = {
        "Nurse Aina (N001)": "N001",
        "Nurse Fatimah (N002)": "N002"
    }

    if df_patients.empty:
        st.warning("The patient database is empty. Please register the patient first in Tab 1..")
    else:
        patient_options = {row["name"]: row["id"] for _, row in df_patients.iterrows()}

        with st.form("add_appointment_form", clear_on_submit=True):
            selected_pt_name = st.selectbox("Select Post-Discharge Patients:", list(patient_options.keys()))
            selected_nurse_name = st.selectbox("Assign a nurse:", list(nurse_options.keys()))
            visit_date = st.date_input("Select Visit Date:", datetime.date.today())
            visit_time = st.selectbox("Select Shift Time Slot:", [
                "09:00 AM (Morning)",
                "11:30 AM (Morning)",
                "02:30 PM (Midday)",
                "05:00 PM (Late Afternoon)"
            ])
            notes = st.text_area("Treatment Preparation Notes")
            submitted = st.form_submit_button("Confirm & Schedule Calendar Appointment", type="primary")

            if submitted:
                p_id = patient_options[selected_pt_name]
                n_id = nurse_options[selected_nurse_name]

                # Simpan rekod temujanji ke dalam database SQLite
                success, msg = db.add_appointment(p_id, n_id, visit_date, visit_time, notes)

                if success:
                    notif_title = "📅 New Visit Appointment Schedule"
                    notif_msg = f"You have been assigned to visit the patient. {selected_pt_name} on {visit_date} ({visit_time}). Notes: {notes}"
                    
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
                        st.success(f"{msg} And the task notification email was successfully sent to the nurse. {nurse_display_name}!")
                    except Exception as e:
                        st.success(msg)
                        st.warning(f"⚠️ The schedule was saved, but the email failed to send to the nurse.: {str(e)}")
                    st.rerun()
                else:
                    st.error(msg)
