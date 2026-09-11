import streamlit as st
import database as db

def render_notification_panel(user_id):
    # Semak jika panel notifikasi dibuka
    if st.session_state.get("show_notification_panel", False):
        st.markdown("### 🔔 Mesej & Notifikasi Sistem")
        
        # Ambil senarai mesej dari database
        notifications = db.get_notifications(user_id)
        
        if not notifications:
            st.info("Tiada sebarang notifikasi baharu buat masa ini.")
            return

        # Sediakan butang untuk tanda semua sebagai dibaca
        if st.button("Tanda Semua Telah Dibaca ✔️", key="mark_all_read_btn"):
            db.mark_all_notifications_as_read(user_id)
            st.success("Semua mesej ditanda sebagai dibaca!")
            st.rerun()
            
        st.markdown("---")
        
        # Paparkan setiap mesej menggunakan kad reka bentuk yang cantik
        for notif in notifications:
            notif_id, title, message, notif_type, is_read, created_at = notif
            
            # Tentukan warna latar belakang berdasarkan status baca
            bg_color = "#e2e8f0" if is_read else "#eff6ff"
            border_color = "#cbd5e1" if is_read else "#3b82f6"
            text_style = "color: #64748b;" if is_read else "color: #1e3a8a; font-weight: bold;"
            
            st.markdown(f"""
                <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; padding: 15px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="{text_style} font-size: 16px;">{title}</span>
                        <span style="font-size: 11px; color: #94a3b8;">{created_at}</span>
                    </div>
                    <p style="margin: 5px 0 0 0; font-size: 14px; color: #334155;">{message}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Jika mesej belum dibaca, paparkan butang individu untuk dibaca
            if not is_read:
                if st.button(f"Tanda Dibaca", key=f"read_{notif_id}"):
                    db.mark_notification_as_read(notif_id)
                    st.rerun()
        st.markdown("---")
