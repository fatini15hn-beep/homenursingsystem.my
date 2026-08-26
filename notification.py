import streamlit as st
import database as db


def show_notifications(user_id):
    """
    Paparkan notification bell untuk user yang sedang login.
    """

    if not user_id:
        return

    # Ambil jumlah notification belum dibaca
    unread_count = db.get_unread_notification_count(user_id)

    # Notification button
    if unread_count > 0:
        button_text = f"🔔 {unread_count}"
    else:
        button_text = "🔔"

    col1, col2, col3 = st.columns([7, 1, 1])

    with col2:

        if st.button(
            button_text,
            key="notification_button",
            use_container_width=True
        ):
            st.session_state["show_notifications"] = not st.session_state.get(
                "show_notifications",
                False
            )

    # Paparkan notification
    if st.session_state.get("show_notifications", False):

        st.markdown(
            """
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:12px;
                border:1px solid #e5e7eb;
                margin-top:10px;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
            ">
                <h3 style="margin-top:0;">
                    🔔 Notifications
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        notifications = db.get_notifications(user_id)

        if not notifications:

            st.info("No notifications available.")

        else:

            for notification in notifications:

                notification_id = notification[0]
                title = notification[1]
                message = notification[2]
                notification_type = notification[3]
                is_read = notification[4]
                created_at = notification[5]

                if notification_type == "appointment":
                    icon = "📅"

                elif notification_type == "assessment":
                    icon = "🩺"

                elif notification_type == "medication":
                    icon = "💊"

                elif notification_type == "memo":
                    icon = "📢"

                elif notification_type == "alert":
                    icon = "🚨"

                else:
                    icon = "🔵"

                if is_read == 0:

                    st.markdown(
                        f"""
                        <div style="
                            background:#eff6ff;
                            padding:15px;
                            border-radius:10px;
                            margin-bottom:10px;
                            border-left:5px solid #2563eb;
                        ">
                            <b>{icon} {title}</b>
                            <br>
                            <span>{message}</span>
                            <br>
                            <small>{created_at}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Mark as read",
                        key=f"read_{notification_id}"
                    ):

                        db.mark_notification_as_read(
                            notification_id
                        )

                        st.rerun()

                else:

                    st.markdown(
                        f"""
                        <div style="
                            background:#f8fafc;
                            padding:15px;
                            border-radius:10px;
                            margin-bottom:10px;
                            opacity:0.7;
                        ">
                            <b>{icon} {title}</b>
                            <br>
                            <span>{message}</span>
                            <br>
                            <small>{created_at}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        if notifications:

            if st.button(
                "Mark all as read",
                key="mark_all_notifications"
            ):

                db.mark_all_notifications_as_read(user_id)

                st.rerun()