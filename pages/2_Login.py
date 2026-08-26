import streamlit as st
import database as db


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Login - Portal System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

db.inject_top_navbar()


# =========================================================
# SESSION STATE
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
# LOGIN PAGE
# =========================================================

st.write("## Log Masuk Portal Sistem")
st.markdown("---")


# =========================================================
# IF ALREADY LOGGED IN
# =========================================================

if st.session_state.logged_in:

    st.warning(
        f"Anda sedang aktif log masuk sebagai "
        f"{st.session_state.user_role} "
        f"({st.session_state.username_display})."
    )

    if st.button(
        "Log Keluar Semasa",
        type="secondary"
    ):

        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username_display = None
        st.session_state.user_id = None

        st.rerun()


# =========================================================
# LOGIN FORM
# =========================================================

else:

    username = st.text_input(
        "Username (Nama Anda)"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Pilih Peranan Anda",
        [
            "Admin",
            "Nurse",
            "Patient"
        ]
    )


    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    if st.button(
        "Log Masuk",
        type="primary"
    ):

        if username and password:

            # =================================================
            # ADMIN LOGIN
            # =================================================

            if role == "Admin":

                if (
                    username.lower() == "ali"
                    and password == "1234"
                ):

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Admin"

                    st.session_state.username_display = "Ali"

                    # User ID untuk notification
                    st.session_state.user_id = "ADMIN_ALI"

                    # Pastikan notification database wujud
                    db.initialize_notification_db()

                    st.success(
                        "Akses Admin diberikan!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Ralat! Hanya Admin bernama "
                        "'Ali' dengan password sah "
                        "dibenarkan."
                    )


            # =================================================
            # NURSE LOGIN
            # =================================================

            elif role == "Nurse":

                if (
                    username.lower() == "aina"
                    and password == "1234"
                ):

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Nurse"

                    st.session_state.username_display = "Aina"

                    # Nurse Aina ID
                    st.session_state.user_id = "N001"

                    db.initialize_notification_db()

                    st.success(
                        "Akses Jururawat diberikan! "
                        "Selamat bertugas Nurse Aina."
                    )

                    st.rerun()


                elif (
                    username.lower() == "fatimah"
                    and password == "1234"
                ):

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Nurse"

                    st.session_state.username_display = "Fatimah"

                    # Nurse Fatimah ID
                    st.session_state.user_id = "N002"

                    db.initialize_notification_db()

                    st.success(
                        "Akses Jururawat diberikan! "
                        "Selamat bertugas Nurse Fatimah."
                    )

                    st.rerun()


                else:

                    st.error(
                        "Ralat! Hanya Jururawat "
                        "'Aina' atau 'Fatimah' "
                        "yang berdaftar dibenarkan."
                    )


            # =================================================
            # PATIENT LOGIN
            # =================================================

            elif role == "Patient":

                # -------------------------------------------------
                # PATIENT 01
                # -------------------------------------------------

                if username.lower() in [
                    "patient_01",
                    "patient01",
                    "ahmad"
                ]:

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Patient"

                    st.session_state.username_display = "Ahmad Patient"

                    # Patient ID
                    st.session_state.user_id = "P001"

                    db.initialize_notification_db()

                    st.success(
                        "Akses Pesakit diberikan! "
                        "Selamat datang Ahmad Patient."
                    )

                    st.rerun()


                # -------------------------------------------------
                # PATIENT 02
                # -------------------------------------------------

                elif username.lower() in [
                    "patient_02",
                    "patient02",
                    "zaki"
                ]:

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Patient"

                    st.session_state.username_display = "Zaki Patient"

                    # Patient ID
                    st.session_state.user_id = "P002"

                    db.initialize_notification_db()

                    st.success(
                        "Akses Pesakit diberikan! "
                        "Selamat datang Zaki Patient."
                    )

                    st.rerun()


                # -------------------------------------------------
                # PATIENT 03
                # -------------------------------------------------

                elif username.lower() in [
                    "patient_03",
                    "patient03",
                    "alia"
                ]:

                    st.session_state.logged_in = True

                    st.session_state.user_role = "Patient"

                    st.session_state.username_display = "Alia Patient"

                    # Patient ID
                    st.session_state.user_id = "P003"

                    db.initialize_notification_db()

                    st.success(
                        "Akses Pesakit diberikan! "
                        "Selamat datang Alia Patient."
                    )

                    st.rerun()


                else:

                    st.error(
                        "Username Patient tidak dijumpai."
                    )


        else:

            st.error(
                "Sila isi username dan password."
            )


# =========================================================
# QUICK DASHBOARD ACCESS
# =========================================================

if st.session_state.logged_in:

    st.markdown("---")

    st.write(
        "### Akses Pantas Dashboard Anda:"
    )


    # =====================================================
    # ADMIN
    # =====================================================

    if st.session_state.user_role == "Admin":

        st.page_link(
            "pages/3_Admin_Dashboard.py",
            label="Buka Admin Dashboard",
            icon="📋"
        )


    # =====================================================
    # NURSE
    # =====================================================

    elif st.session_state.user_role == "Nurse":

        st.page_link(
            "pages/4_Nurse_Dashboard.py",
            label="Buka Nurse Dashboard",
            icon="🩺"
        )


    # =====================================================
    # PATIENT
    # =====================================================

    elif st.session_state.user_role == "Patient":

        st.page_link(
            "pages/5_Patient_Dashboard.py",
            label="Buka Patient Dashboard",
            icon="🛌"
        )
