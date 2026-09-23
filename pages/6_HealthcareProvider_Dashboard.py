import streamlit as st
import database as db
import pandas as pd

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="Healthcare Provider Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Memanggil top navbar secara selamat
db.inject_top_navbar()

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username_display" not in st.session_state:
    st.session_state.username_display = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# =========================================================
# ACCESS CONTROL
# =========================================================
# =========================================================
# ACCESS CONTROL
# =========================================================

if (
    not st.session_state.get("logged_in")
    or st.session_state.get("user_role") != "Healthcare Provider"
):
    st.error(
        "🚫 Akses Disekat! Sila Log Masuk sebagai Healthcare Provider untuk melihat rekod rawatan."
    )

    st.page_link(
        "pages/2_Login.py",
        label="Pergi ke Halaman Login",
        icon="🔐"
    )

    st.stop()

# =========================================================
# HEADER
# =========================================================
st.title("Healthcare Provider Dashboard")
st.write(f"Welcome, Healthcare Provider **{st.session_state.username_display}**.")
st.caption("Monitor patient information, nursing assessments and recovery progress.")
st.markdown("---")

# =========================================================
# LOAD DATA FROM SQLITE
# =========================================================
df_patients = db.get_patients_df()
df_assessments = db.get_assessments_df()

# =========================================================
# SUMMARY METRICS CARD
# =========================================================
total_patients = len(df_patients)
total_assessments = len(df_assessments)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Patients", total_patients)
with col2:
    st.metric("Nursing Assessments", total_assessments)
with col3:
    if not df_assessments.empty:
        st.metric("Assessment Status", "Available")
    else:
        st.metric("Assessment Status", "No Record")

st.markdown("---")

# =========================================================
# PATIENT INFORMATION TABLE
# =========================================================
st.subheader("Patient Information")

if df_patients.empty:
    st.info("No patient information available.")
else:
    display_columns = ["id", "name", "age", "gender", "phone", "illness", "status"]
    available_columns = [col for col in display_columns if col in df_patients.columns]
    
    st.dataframe(
        df_patients[available_columns],
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# =========================================================
# SELECT PATIENT FOR DETAILED VIEW
# =========================================================
st.subheader("View Patient Details")

selected_patient_id = None
selected_patient_name = None

if not df_patients.empty:
    patient_options = {row["name"]: row["id"] for _, row in df_patients.iterrows()}
    selected_patient_name = st.selectbox("Select Patient", list(patient_options.keys()))
    selected_patient_id = patient_options[selected_patient_name]

    # Ambil baris data pesakit terpilih
    patient_data = df_patients[df_patients["id"] == selected_patient_id]

    if not patient_data.empty:
        patient = patient_data.iloc[0]
        col1, col2 = st.columns(2)

        # Personal Profil
        with col1:
            st.write("### Patient Details")
            st.write(f"**Patient ID:** {patient['id']}")
            st.write(f"**Name:** {patient['name']}")
            st.write(f"**Age:** {patient['age']}")
            st.write(f"**Gender:** {patient['gender']}")
            st.write(f"**Phone:** {patient['phone']}")

        # Maklumat Perubatan Awam
        with col2:
            st.write("### Medical Information")
            st.write(f"**Diagnosis:** {patient['illness']}")
            st.write(f"**Status:** {patient['status']}")

st.markdown("---")

# =========================================================
# NURSING ASSESSMENT HISTORY
# =========================================================
st.subheader("Nursing Assessment")

if selected_patient_id is None:
    st.info("Please select a patient first.")
else:
    patient_assessments = df_assessments[df_assessments["patient_id"] == selected_patient_id]

    if patient_assessments.empty:
        st.info(f"No nursing assessment available for {selected_patient_name}.")
    else:
        assessment_columns = ["blood_pressure", "pulse_rate", "blood_sugar", "wound_condition", "nurse_memo"]
        available_assessment_columns = [col for col in assessment_columns if col in patient_assessments.columns]

        st.dataframe(
            patient_assessments[available_assessment_columns],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

# =========================================================
# RECOVERY PROGRESS LOGS
# =========================================================
st.subheader("Recovery Progress")

if selected_patient_id is None:
    st.info("Please select a patient to view recovery progress.")
else:
    patient_assessments = df_assessments[df_assessments["patient_id"] == selected_patient_id]

    if patient_assessments.empty:
        st.info("Recovery progress will appear after the nurse submits a nursing assessment.")
    else:
        # Mengambil laporan kesihatan terkini (paling atas/terbaru)
        latest = patient_assessments.iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            if "blood_pressure" in latest:
                st.write(f"**Latest Blood Pressure:** {latest['blood_pressure']}")
            if "pulse_rate" in latest:
                st.write(f"**Latest Pulse Rate:** {latest['pulse_rate']} bpm")
            if "blood_sugar" in latest:
                st.write(f"**Latest Blood Sugar:** {latest['blood_sugar']} mmol/L")

        with col2:
            if "wound_condition" in latest:
                st.write(f"**Wound Condition:** {latest['wound_condition']}")
            if "nurse_memo" in latest:
                st.write(f"**Nurse Memo:** {latest['nurse_memo']}")

st.markdown("---")
st.caption("🔒 End of Secure Healthcare Provider Report Session.")

# =========================================================
# SAMBUNGAN KOD PENAMBAHAN HOSPITAL INSTRUCTION YANG TERGANTUNG
# =========================================================
st.write("### ✍️ Hospital Instruction / Memo to Nurse")
st.info(f"Hantar arahan perubatan rasmi mengenai pesakit **{selected_patient_name if selected_patient_name else 'Pilihan'}** terus ke Dashboard Jururawat.")

if selected_patient_id is None:
    st.warning("Sila pastikan data pesakit dipilih terlebih dahulu di bahagian atas.")
else:
    with st.form("provider_memo_form", clear_on_submit=True):
        st.text_input("Target Patient ID:", value=selected_patient_id, disabled=True)
        
        selected_nurse = st.selectbox("Assign Memo to Nurse:", ["N001 (Nurse Aina)", "N002 (Nurse Fatimah)"])
        nurse_id_target = "N001" if "N001" in selected_nurse else "N002"
        
        memo_title = st.text_input("Instruction Title:", placeholder="Contoh: Strict Glucose Monitoring / Penjagaan Luka")
        memo_message = st.text_area("Doctor's Message / Instructions:")
        
        submitted_memo = st.form_submit_button("Send Instruction to Nurse", type="primary")
        
        if submitted_memo:
            if not memo_title:
                st.warning("Sila isi tajuk arahan.")
            elif not memo_message:
                st.warning("Sila isi kandungan mesej arahan doctor.")
            else:
                provider_id = st.session_state.user_id if st.session_state.user_id else "HP001"
                ok, msg, email_res = db.add_hospital_memo(selected_patient_id, nurse_id_target, provider_id, memo_title, memo_message)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
