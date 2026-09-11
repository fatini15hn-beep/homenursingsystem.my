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

st.write("## Log Masuk Portal Sistem")
st.markdown("---")

# =========================================================
# JIKA PENGGUNA SUDAH AKTIF LOG MASUK (PAUTAN PINTAS KEMBALI)
# =========================================================
if st.session_state.logged_in:
    st.info(f"✨ Sesi Aktif: Anda telah log masuk sebagai **{st.session_state.user_role}** ({st.session_state.username_display}).")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Masuk Ke Dashboard Anda ➡️", type="primary"):
            if st.session_state.user_role == "Admin":
                st.switch_page("pages/3_Admin_Dashboard.py")
            elif st.session_state.user_role == "Nurse":
                st.switch_page("pages/4_Nurse_Dashboard.py")
            elif st.session_state.user_role == "Patient":
                st.switch_page("pages/5_Patient_Dashboard.py")
            elif st.session_state.user_role == "Healthcare Provider":
                st.switch_page("pages/6_HealthcareProvider_Dashboard.py")
    
    with col2:
        if st.button("Log Keluar Semasa", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.username_display = None
            st.session_state.user_id = None
            st.rerun()

# =========================================================
# BORANG LOG MASUK UTAMA
# =========================================================
else:
    username = st.text_input("Username (Nama Anda)")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Pilih Peranan Anda", ["Admin", "Nurse", "Patient", "Healthcare Provider"])

    if st.button("Log Masuk", type="primary"):
        if username and password:
            
            # --- 1. ADMIN LOGIN ---
            if role == "Admin":
                if username.lower() == "ali" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username_display = "Ali"
                    st.session_state.user_id = "ADMIN_ALI"
                    st.success("Akses Admin diberikan!")
                    
                    st.switch_page("pages/3_Admin_Dashboard.py")
                else:
                    st.error("Ralat! Hanya Admin bernama 'Ali' dengan password sah dibenarkan.")

            # --- 2. NURSE LOGIN ---
            elif role == "Nurse":
                if username.lower() == "aina" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Nurse"
                    st.session_state.username_display = "Aina"
                    st.session_state.user_id = "N001"
                    st.success("Akses Jururawat diberikan! Selamat bertugas Nurse Aina.")
                    
                    st.switch_page("pages/4_Nurse_Dashboard.py")
                elif username.lower() == "fatimah" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Nurse"
                    st.session_state.username_display = "Fatimah"
                    st.session_state.user_id = "N002"
                    st.success("Akses Jururawat diberikan! Selamat bertugas Nurse Fatimah.")
                    
                    st.switch_page("pages/4_Nurse_Dashboard.py")
                else:
                    st.error("Ralat! Hanya Jururawat 'Aina' atau 'Fatimah' yang berdaftar dibenarkan.")

            # --- 3. DYNAMIC PATIENT LOGIN (Mengambil Data dari SQLite) ---
            elif role == "Patient":
                df_pt = db.get_patients_df()
                match = df_pt[df_pt['name'].str.lower() == username.lower()]
                
                if not match.empty and password == "1234":
                    patient_data = match.iloc[0]
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Patient"
                    st.session_state.username_display = patient_data['name']
                    st.session_state.user_id = patient_data['id']
                    st.success(f"Akses Pesakit diberikan! Selamat datang {patient_data['name']}.")
                    
                    st.switch_page("pages/5_Patient_Dashboard.py")
                else:
                    st.error("Ralat! Nama pesakit tidak dijumpai dalam pangkalan data atau kata laluan salah.")
                    
            # --- 4. HEALTHCARE PROVIDER LOGIN ---
            elif role == "Healthcare Provider":
                if username.lower() == "shahmi" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Healthcare Provider"
                    st.session_state.username_display = "Shahmi"
                    st.session_state.user_id = "H001"
                    st.success("Akses Healthcare Provider Shahmi diberikan!")
                    
                    st.switch_page("pages/6_HealthcareProvider_Dashboard.py")
                else:
                    st.error("Ralat! Username atau password Healthcare Provider salah.")
        else:
            st.warning("⚠️ Sila isi ruangan Username dan Password terlebih dahulu.")
