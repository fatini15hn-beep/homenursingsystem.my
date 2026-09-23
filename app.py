import streamlit as st
import database as db

# 1. Pastikan database di-initialize terlebih dahulu
db.initialize_db()

# 2. Set konfigurasi halaman utama
st.set_page_config(
    page_title="Home Nursing System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. Masukkan Top Navigation Bar (HTML yang anda hantar tadi)
db.inject_top_navbar()

# 4. Kandungan Halaman Utama (Portal Main)
st.title("Welcome to the Home Nursing System Portal")
st.subheader("Nurse Visit Management System for Post-Discharge Patients")

st.markdown("""
This system is specially designed to facilitate patient health monitoring at home, management of nurse appointment schedules, as well as the digital delivery of medical memo instructions""")


