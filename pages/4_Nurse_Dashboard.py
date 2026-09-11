import streamlit as st
import database as db
import pandas as pd
from datetime import datetime

# =========================================================
# INITIALIZATION
# =========================================================
db.initialize_db()

st.set_page_config(
    page_title="Nurse Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

db.inject_top_navbar()

# =========================================================
# ACCESS CONTROL
# =========================================================
if (
    not st.session_state.get("logged_in")
    or st.session_state.get("user_role") != "Nurse"
):
    st.error("Akses Nurse sahaja.")
    st.stop()

# =========================================================
# NURSE INFORMATION
# =========================================================
nid = st.session_state.user_id
nname = st.session_state.username_display

st.title(f"Nurse Dashboard — {nname}")
st.caption(f"Nurse ID: {nid} | Home visit, assessment and daily work")

# =========================================================
# LOAD DATA
# =========================================================
patients = db.get_patients_df()
apps = db.get_appointments_df()

if not apps.empty:
    assigned = apps[apps["nurse_id"].astype(str) == str(nid)].copy()
else:
    assigned = apps

# =========================================================
# TABS
# =========================================================
tabs = st.tabs([
    "My Schedule",
    "Patient Review",
    "Home Visit & Check-In",
    "Assessment",
    "Hospital Memo",
    "Clock-Out"
])

# =========================================================
# TAB 1: MY SCHEDULE
# =========================================================
with tabs[0]:
    st.subheader("My Home Visit Schedule")
    if assigned.empty:
        st.info("Tiada appointment yang assigned kepada anda.")
    else:
        st.dataframe(assigned, use_container_width=True)

# =========================================================
# TAB 2: PATIENT REVIEW
# =========================================================
with tabs[1]:
    st.subheader("Pre-Visit Patient Review")
    if assigned.empty:
        st.info("Tiada patient assigned.")
    else:
        pid = st.selectbox("Patient", assigned["patient_id"].tolist())
        selected_patient = patients[patients["id"].astype(str) == str(pid)]
        
        if not selected_patient.empty:
            p = selected_patient.iloc[0]
            st.info(f"Patient: {p['name']} | ID: {p['id']} | Age: {p['age']} | Phone: {p['phone']}")
            st.write(f"**Illness:** {p['illness']}")
            st.write(f"**Status:** {p['status']}")
            st.write(f"**Email:** {p.get('email', '')}")

# =========================================================
# TAB 3: HOME VISIT & CHECK-IN
# =========================================================
with tabs[2]:
    st.subheader("Home Visit Check-In / Check-Out")
    if assigned.empty:
        st.info("Tiada appointment.")
    else:
        pid = st.selectbox("Patient for visit", assigned["patient_id"].tolist(), key="ci_patient")

        # CHECK-IN BUTTON
        if st.button("Check-In / Start Home Visit", type="primary"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ok, msg = db.add_checkin(nid, pid, current_time)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

        # CHECK-IN TABLE
        ci = db.get_checkins_df(nid)
        st.dataframe(ci, use_container_width=True)

        # CHECK-OUT BUTTON
        if not ci.empty:
            open_ci = ci[ci["status"] == "Checked In"]
            if not open_ci.empty:
                cid = int(open_ci.iloc[0]["id"])
                if st.button("Check-Out / Complete Home Visit"):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ok, msg = db.checkout(cid, current_time)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# =========================================================
# TAB 4: ASSESSMENT (BAGIAN EMAIL PESAKIT DITAMBAH DI SINI)
# =========================================================
with tabs[3]:
    st.subheader("In-Home Nursing Assessment")
    if assigned.empty:
        st.info("Tiada patient assigned.")
    else:
        with st.form("assessment_form"):
            # 1. Ambil ID Pesakit yang ada temujanji dengan Nurse ini
            list_pid = assigned["patient_id"].tolist()
            
            # 2. Bina format teks baru untuk selectbox supaya nampak ID, Nama & Email sekali gus
            options_format = {}
            for p_id in list_pid:
                match_p = patients[patients["id"].astype(str) == str(p_id)]
                if not match_p.empty:
                    p_data = match_p.iloc[0]
                    p_name = p_data["name"]
                    p_email = p_data.get("email", "")
                    p_email_text = f" ({p_email})" if p_email else " (Tiada Email)"
                    
                    # Simpan format teks paparan sebagai Key, dan ID sebenar sebagai Value
                    options_format[f"ID: {p_id} - {p_name}{p_email_text}"] = p_id
                else:
                    options_format[f"ID: {p_id}"] = p_id

            # 3. Paparkan senarai pilihan pesakit dengan maklumat lengkap
            selected_display = st.selectbox(
                "Pilih Pesakit",
                options=list(options_format.keys()),
                key="ass_pid_display"
            )
            
            # Extract ID pesakit sebenar yang dipilih untuk dihantar ke database
            pid = options_format[selected_display]

            bp = st.text_input("Blood Pressure (mmHg)")
            pulse = st.number_input("Pulse Rate (bpm)", min_value=30, max_value=200, value=75)
            sugar = st.number_input("Blood Sugar (mmol/L)", min_value=0.0, max_value=30.0, value=5.5)
            wound = st.selectbox("Wound Condition", ["No Wound", "Healing Well", "Signs of Infection", "Needs New Dressing"])
            memo = st.text_area("Nurse Memo")
            send_email = st.checkbox("Send assessment email to patient", value=True)
            submit = st.form_submit_button("Save Assessment", type="primary")

            if submit:
                if not bp:
                    st.warning("Blood pressure wajib diisi.")
                elif not memo:
                    st.warning("Nurse memo wajib diisi.")
                else:
                    ok, msg, email_results = db.add_assessment(pid, nid, bp, pulse, sugar, wound, memo, send_email)
                    if ok:
                        st.success(msg)
                        
                        if email_results:
                            for result in email_results:
                                if "berjaya" in result.lower() or "sent" in result.lower():
                                    st.success(result)
                                else:
                                    st.warning(result)

# =========================================================
# TAB 5: HOSPITAL MEMO
# =========================================================
with tabs[4]:
    st.subheader("Hospital Instructions & Memos")
    memos = db.get_hospital_memos_df()
    if not memos.empty:
        my_memos = memos[memos["nurse_id"].astype(str) == str(nid)]
        if my_memos.empty:
            st.info("Tiada hospital memo untuk pesakit anda.")
        else:
            st.dataframe(my_memos, use_container_width=True)
    else:
        st.info("Tiada sebarang hospital memo dalam sistem.")

# =========================================================
# TAB 6: CLOCK-OUT
# =========================================================
with tabs[5]:
    st.subheader("End Daily Shift")
    if st.button("Log Keluar dari Sistem", type="primary", key="btn_logout"):
        st.session_state.clear()
        st.success("Anda telah berjaya log keluar.")
        st.rerun()
