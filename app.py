import streamlit as st
import database as db

db.initialize_db()
st.set_page_config(page_title="Home Care Nursing", layout="wide", initial_sidebar_state="collapsed")
db.inject_top_navbar()

st.write("## Welcome to Home Care Nursing Portal")
st.markdown("---")

st.info("Portal ini dibina khas untuk pengurusan penjagaan pesakit pasca-discaj hospital berumur antara 18 hingga 59 tahun.")

col1, col2, col3 = st.columns(3)
df_p = db.get_patients_df()
df_n = db.get_nurses_df()

col1.metric("Pendaftaran Aktif", f"{len(df_p)} Pesakit")
col2.metric("Kakitangan Jururawat", f"{len(df_n)} Orang")
col3.metric("Liputan Servis", "24 Jam / 7 Hari")

