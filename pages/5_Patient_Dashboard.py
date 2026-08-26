import streamlit as st
import database as db

st.set_page_config(page_title="Patient Dashboard", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

if not st.session_state.logged_in or st.session_state.user_role != "Patient":
    st.error("🚫 Akses Disekat! Sila Log Masuk sebagai Pesakit untuk melihat rekod rawatan peribadi anda.")
else:
    st.write(f"## Patient Dashboard - Selamat Datang {st.session_state.username_display}")
    
    st.write("### Maklumat Profil & Jenis Penyakit Anda (Disahkan oleh Admin)")
    df_pt = db.get_patients_df()
    st.dataframe(df_pt, use_container_width=True)
    
    st.markdown("---")
    st.write("### Sejarah Laporan Lawatan Jururawat Di Rumah Anda")
    df_ass = db.get_assessments_df()
    st.dataframe(df_ass, use_container_width=True)

