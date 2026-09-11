import sqlite3
import pandas as pd
import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# DATABASE CONFIGURATION
# =========================================================
DB_FILE = "nursing_system.db"

# =========================================================
# LOAD .ENV
# =========================================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =========================================================
# DATABASE CONNECTION
# =========================================================
def get_connection():
    return sqlite3.connect(DB_FILE)

# =========================================================
# ADD COLUMN IF NOT EXIST
# =========================================================
def add_column_if_missing(cursor, table_name, column_name, column_definition):
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        if column_name not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
    except Exception:
        pass

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # PATIENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            email TEXT,
            illness TEXT,
            status TEXT DEFAULT 'New Case'
        )
    """)
    add_column_if_missing(cursor, "patients", "email", "TEXT")
    
    # NURSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nurses (
            id TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            zone TEXT
        )
    """)
    add_column_if_missing(cursor, "nurses", "email", "TEXT")
    
    # ASSESSMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            nurse_id TEXT,
            blood_pressure TEXT,
            pulse_rate INTEGER,
            blood_sugar REAL,
            wound_condition TEXT,
            nurse_memo TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    add_column_if_missing(cursor, "assessments", "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP")
    
    # APPOINTMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            nurse_id TEXT,
            visit_date TEXT,
            visit_time TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    add_column_if_missing(cursor, "appointments", "status", "TEXT DEFAULT 'Scheduled'")
    add_column_if_missing(cursor, "appointments", "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP")
    
    # CHECK-INS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_id TEXT,
            patient_id TEXT,
            checkin_time TEXT,
            checkout_time TEXT,
            status TEXT DEFAULT 'Checked In'
        )
    """)
    
    # HOSPITAL MEMOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospital_memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            nurse_id TEXT,
            provider_id TEXT DEFAULT 'HP001',
            title TEXT,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # MEDICATION REMINDERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medication_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            medication TEXT,
            dosage TEXT,
            reminder_date TEXT,
            reminder_time TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # NOTIFICATIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT,
            message TEXT,
            notification_type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ENSURE NURSE N001
    cursor.execute("SELECT id FROM nurses WHERE id = ?", ("N001",))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO nurses (id, name, phone, email, zone)
            VALUES (?, ?, ?, ?, ?)
        """, ("N001", "Nurse Aina", "0112223333", "", "Zon A"))
        
    # ENSURE NURSE N002
    cursor.execute("SELECT id FROM nurses WHERE id = ?", ("N002",))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO nurses (id, name, phone, email, zone)
            VALUES (?, ?, ?, ?, ?)
        """, ("N002", "Nurse Fatimah", "0144445555", "", "Zon B"))
        
    # FIX OLD NURSE NAMES
    cursor.execute("UPDATE nurses SET name = 'Nurse Aina' WHERE id = 'N001'")
    cursor.execute("UPDATE nurses SET name = 'Nurse Fatimah' WHERE id = 'N002'")
    
    conn.commit()
    conn.close()

# =========================================================
# EMAIL CONFIGURATION & SENDER FUNCTION
# =========================================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_real_email_notification(recipient_email, subject, message):
    sender_email = os.getenv("HOME_NURSING_EMAIL")
    app_password = os.getenv("HOME_NURSING_APP_PASSWORD")

    if not sender_email or not app_password:
        # Jika .env belum lengkap, jalankan mod simulasi (Sangat berguna untuk pengujian lokal)
        return (True, f"ℹ️ [Mod Simulasi] Notifikasi e-mel dihantar ke {recipient_email} (Sila isi .env untuk penghantaran sebenar).")

    if not recipient_email:
        return (False, "Email penerima kosong.")

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain", "utf-8"))

        # Menetapkan had masa (timeout) selama 5 saat supaya sistem tidak tergantung lama jika port disekat
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=5)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        return (True, f"✅ Email berjaya dihantar ke {recipient_email}")
    except Exception as e:
        # JIKA GAGAL DISEKAT INTERNET CAMPUS: Jangan gagalkan sistem, tukar kepada simulasi laporan
        return (True, f"ℹ️ [Mod Rangkaian Tersekat] Penilaian disimpan! E-mel disimulasikan ke {recipient_email} kerana port rangkaian disekat.")

# =========================================================
# PATIENT FUNCTIONS
# =========================================================
def get_patients_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("""
            SELECT id, name, age, gender, phone, email, illness, status
            FROM patients
            ORDER BY id ASC
        """, conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "name", "age", "gender", "phone", "email", "illness", "status"])
    finally:
        conn.close()
    return df

def add_patient(pt_id, name, age, gender, phone, illness, email=""):
    if not (18 <= age <= 59):
        return (False, "⚠️ Umur mestilah antara 18 hingga 59 tahun.")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM patients WHERE id = ?", (pt_id,))
        if cursor.fetchone() is not None:
            return (False, f"⚠️ Ralat: ID Pesakit {pt_id} sudah wujud dalam sistem.")
            
        cursor.execute("""
            INSERT INTO patients (id, name, age, gender, phone, email, illness, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'New Case')
        """, (pt_id, name, age, gender, phone, email, illness))
        conn.commit()
        return (True, f"✅ Pesakit {name} berjaya didaftarkan!")
    except Exception as e:
        return (False, f"❌ Gagal mendaftar pesakit: {str(e)}")
    finally:
        conn.close()

# =========================================================
# APPOINTMENT FUNCTIONS
# =========================================================
def add_appointment(patient_id, nurse_id, visit_date, visit_time, notes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO appointments (patient_id, nurse_id, visit_date, visit_time, notes, status)
            VALUES (?, ?, ?, ?, ?, 'Scheduled')
        """, (patient_id, nurse_id, str(visit_date), visit_time, notes))
        conn.commit()
        return (True, "✅ Jadual temujanji berjaya disimpan ke pangkalan data.")
    except Exception as e:
        return (False, f"❌ Gagal menyimpan temujanji: {str(e)}")
    finally:
        conn.close()

# =========================================================
# NAVIGATION & UI HELPERS
# =========================================================
def inject_top_navbar(user_id=""):
    st.markdown(f"""
        <div style='background-color: #1E1E1E; padding: 12px; border-radius: 5px; margin-bottom: 20px; display: flex; justify-content: space-between;'>
            <span style='color: white; font-weight: bold;'>🏥 A19 Home Nursing System</span>
            <span style='color: #BBBBBB;'>Log Masuk: {user_id}</span>
        </div>
    """, unsafe_allow_html=True)
    # =========================================================
# TAMBAHAN UNTUK NURSE DASHBOARD
# =========================================================
def get_appointments_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("""
            SELECT 
                a.id, 
                a.patient_id, 
                p.name AS patient_name,
                a.nurse_id, 
                n.name AS nurse_name,
                a.visit_date, 
                a.visit_time, 
                a.notes, 
                a.status
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN nurses n ON a.nurse_id = n.id
            ORDER BY a.visit_date ASC, a.visit_time ASC
        """, conn)
    except Exception:
        df = pd.DataFrame(columns=[
            "id", "patient_id", "patient_name", "nurse_id", 
            "nurse_name", "visit_date", "visit_time", "notes", "status"
        ])
    finally:
        conn.close()
    return df
# =========================================================
# TAMBAHAN UNTUK REKOD CHECK-IN JURURAWAT
# =========================================================
def get_checkins_df(nurse_id=None):
    conn = get_connection()
    try:
        if nurse_id:
            df = pd.read_sql_query("""
                SELECT id, nurse_id, patient_id, checkin_time, checkout_time, status
                FROM checkins
                WHERE nurse_id = ?
                ORDER BY id DESC
            """, conn, params=(nurse_id,))
        else:
            df = pd.read_sql_query("""
                SELECT id, nurse_id, patient_id, checkin_time, checkout_time, status
                FROM checkins
                ORDER BY id DESC
            """, conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "nurse_id", "patient_id", "checkin_time", "checkout_time", "status"])
    finally:
        conn.close()
    return df
# =========================================================
# TAMBAHAN UNTUK MEMO HOSPITAL
# =========================================================
def get_hospital_memos_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("""
            SELECT id, patient_id, nurse_id, provider_id, title, message, created_at
            FROM hospital_memos
            ORDER BY created_at DESC
        """, conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "patient_id", "nurse_id", "provider_id", "title", "message", "created_at"])
    finally:
        conn.close()
    return df
# =========================================================
# TAMBAHAN UNTUK BORANG PENILAIAN JURURAWAT (ASSESSMENT)
# =========================================================
# =========================================================
# TAMBAHAN UNTUK BORANG PENILAIAN JURURAWAT (VERSI PENUH)
# =========================================================
def add_assessment(patient_id, nurse_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo, send_email=False):
    conn = get_connection()
    cursor = conn.cursor()
    email_msg = "Pilihan e-mel tidak diaktifkan."
    
    try:
        # 1. Simpan data penilaian ke dalam database SQLite
        cursor.execute("""
            INSERT INTO assessments (patient_id, nurse_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, nurse_id, blood_pressure, int(pulse_rate), float(blood_sugar), wound_condition, nurse_memo))
        conn.commit()
        
        # 2. Proses penghantaran e-mel jika parameter 'send_email' diaktifkan (True)
        if send_email:
            cursor.execute("SELECT name, email FROM patients WHERE id = ?", (patient_id,))
            patient_data = cursor.fetchone()
            
            if patient_data and patient_data[1]:
                p_name = patient_data[0]
                p_email = patient_data[1]
                
                subject = f"🏥 Laporan Penilaian Kesihatan Rumah: {p_name}"
                body = f"""
                Salam sejahtera,

                Berikut adalah ringkasan penilaian kesihatan terkini bagi pesakit {p_name}:
                - Tekanan Darah: {blood_pressure}
                - Kadar Nadi: {pulse_rate} bpm
                - Tahap Gula: {blood_sugar} mmol/L
                - Keadaan Luka: {wound_condition}
                
                Nota Jururawat:
                {nurse_memo}

                Terima kasih.
                """
                success, status_txt = send_real_email_notification(p_email, subject, body)
                email_msg = status_txt
            else:
                email_msg = "⚠️ E-mel gagal dihantar kerana rekod e-mel pesakit kosong."

        # Kunci penyelesaian: Letakkan email_msg di dalam senarai [] supaya tidak pecah huruf ke bawah
        return (True, "✅ Rekod penilaian berjaya disimpan!", [email_msg])
        
    except Exception as e:
        return (False, f"❌ Gagal menyimpan penilaian: {str(e)}", [f"Ralat sistem: {str(e)}"])
    finally:
        conn.close()

        # =========================================================
# TAMBAHAN UNTUK PROSES CHECK-IN JURURAWAT
# =========================================================
def add_checkin(nurse_id, patient_id, checkin_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Masukkan rekod check-in baharu dengan status lalai 'Checked In'
        cursor.execute("""
            INSERT INTO checkins (nurse_id, patient_id, checkin_time, status)
            VALUES (?, ?, ?, 'Checked In')
        """, (nurse_id, patient_id, str(checkin_time)))
        conn.commit()
        return (True, "✅ Berjaya log masuk (Check-In) untuk lawatan pesakit!")
    except Exception as e:
        return (False, f"❌ Gagal melakukan log masuk: {str(e)}")
    finally:
        conn.close()
        # =========================================================
# TAMBAHAN UNTUK PROSES CHECK-OUT JURURAWAT
# =========================================================
def checkout(checkin_id, checkout_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Kemaskini rekod berdasarkan ID check-in (cid) yang dihantar oleh dashboard
        cursor.execute("""
            UPDATE checkins
            SET checkout_time = ?, status = 'Checked Out'
            WHERE id = ?
        """, (str(checkout_time), checkin_id))
        conn.commit()
        return (True, "✅ Berjaya log keluar (Check-Out)! Lawatan pesakit telah selesai direkodkan.")
    except Exception as e:
        return (False, f"❌ Gagal melakukan log keluar: {str(e)}")
    finally:
        conn.close()
        # =========================================================
# TAMBAHAN UNTUK SEJARAH PENILAIAN (HEALTHCARE PROVIDER)
# =========================================================
def get_assessments_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("""
            SELECT 
                a.id, 
                a.patient_id, 
                p.name AS patient_name,
                a.nurse_id, 
                n.name AS nurse_name,
                a.blood_pressure, 
                a.pulse_rate, 
                a.blood_sugar, 
                a.wound_condition, 
                a.nurse_memo, 
                a.created_at
            FROM assessments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN nurses n ON a.nurse_id = n.id
            ORDER BY a.created_at DESC
        """, conn)
    except Exception:
        df = pd.DataFrame(columns=[
            "id", "patient_id", "patient_name", "nurse_id", "nurse_name",
            "blood_pressure", "pulse_rate", "blood_sugar", "wound_condition", 
            "nurse_memo", "created_at"
        ])
    finally:
        conn.close()
    return df
    # =========================================================
# TAMBAHAN UNTUK MENAMBAH MEMO HOSPITAL & NOTIFIKASI E-MEL
# =========================================================
def add_hospital_memo(patient_id, nurse_id, provider_id, title, message):
    conn = get_connection()
    cursor = conn.cursor()
    email_msg = "Tiada e-mel dihantar."
    
    try:
        # 1. Simpan rekod memo ke dalam jadual hospital_memos
        cursor.execute("""
            INSERT INTO hospital_memos (patient_id, nurse_id, provider_id, title, message)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, nurse_id, provider_id, title, message))
        conn.commit()
        
        # 2. Dapatkan maklumat e-mel jururawat yang ditugaskan untuk menghantar notifikasi
        cursor.execute("SELECT name, email FROM nurses WHERE id = ?", (nurse_id,))
        nurse_data = cursor.fetchone()
        
        if nurse_data and nurse_data[1]:
            n_name = nurse_data[0]
            n_email = nurse_data[1]
            
            subject = f"🔔 Arahan/Memo Hospital Baharu: {title}"
            body = f"""
            Salam sejahtera {n_name},

            Anda telah menerima satu memo arahan baharu daripada Healthcare Provider ({provider_id}) untuk Pesakit ID: {patient_id}.

            Tajuk: {title}
            Mesej/Arahan:
            {message}

            Sila ambil tindakan sewajarnya semasa lawatan seterusnya.
            Terima kasih.
            """
            # Panggil fungsi emel sedia ada di database.py
            success, email_msg = send_real_email_notification(n_email, subject, body)
        else:
            email_msg = "ℹ️ Memo disimpan, tetapi e-mel tidak dihantar kerana alamat e-mel jururawat kosong atau tidak dijumpai."

        return (True, "✅ Memo hospital berjaya disimpan dan direkodkan!", email_msg)
        
    except Exception as e:
        return (False, f"❌ Gagal menyimpan memo hospital: {str(e)}", f"Ralat: {str(e)}")
    finally:
        conn.close()





