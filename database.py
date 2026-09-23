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
        """, ("N001", "Nurse Aina", "0112223333", "", "Zone A"))
        
    # ENSURE NURSE N002
    cursor.execute("SELECT id FROM nurses WHERE id = ?", ("N002",))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO nurses (id, name, phone, email, zone)
            VALUES (?, ?, ?, ?, ?)
        """, ("N002", "Nurse Fatimah", "0144445555", "", "Zone B"))
        
    # FIX OLD NURSE NAMES
    cursor.execute("UPDATE nurses SET name = 'Nurse Aina' WHERE id = 'N001'")
    cursor.execute("UPDATE nurses SET name = 'Nurse Fatimah' WHERE id = 'N002'")
    
    conn.commit()
    conn.close()

# =========================================================
# TOP NAVBAR INJECTION 
# =========================================================
def inject_top_navbar(*args, **kwargs):
    """
    Dynamically receives any parameters (*args, **kwargs) so that no errors occur
    when called from either the Admin Dashboard or the Nurse Dashboard.
    """
    pass

# =========================================================
# EMAIL CONFIGURATION & SENDER FUNCTION (FIXED GMAIL SMTP)
# =========================================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_real_email_notification(recipient_email, subject, message):
    sender_email = os.getenv("HOME_NURSING_EMAIL")
    app_password = os.getenv("HOME_NURSING_APP_PASSWORD")
    
    if not sender_email:
        return (False, "⚠️ HOME_NURSING_EMAIL has not been configured.")
    if not app_password:
        return (False, "⚠️ HOME_NURSING_APP_PASSWORD has not been configured.")
    if not recipient_email:
        return (False, "⚠️ Recipient email is empty.")
        
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain", "utf-8"))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return (True, f"✅ Email successfully sent to {recipient_email}")
    except Exception as e:
        return (False, f"⚠️ Email failed to send: {str(e)}")

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
        return (False, "⚠️ Age must be between 18 and 59 years old.")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO patients (id, name, age, gender, phone, illness, email) VALUES (?,?,?,?,?,?,?)",
                       (pt_id, name, age, gender, phone, illness, email))
        conn.commit()
        return (True, "✅ Patient registration successful.")
    except sqlite3.IntegrityError:
        return (False, "⚠️ Patient ID already exists.")
    finally:
        conn.close()

def add_appointment(patient_id, nurse_id, visit_date, visit_time, notes):
    """
    Saves an appointment record into the SQLite database.
    Returns a tuple: (True/False, "Status message string")
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        date_str = str(visit_date)
        cursor.execute("""
            INSERT INTO appointments (patient_id, nurse_id, visit_date, visit_time, notes, status)
            VALUES (?, ?, ?, ?, ?, 'Scheduled')
        """, (patient_id, nurse_id, date_str, visit_time, notes))
        conn.commit()
        return (True, "✅ Appointment successfully registered in the system calendar!")
    except Exception as e:
        return (False, f"⚠️ Failed to save appointment: {str(e)}")
    finally:
        conn.close()

def get_appointments_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("""
            SELECT id, patient_id, nurse_id, visit_date, visit_time, notes, status, created_at
            FROM appointments
            ORDER BY id ASC
        """, conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "patient_id", "nurse_id", "visit_date", "visit_time", "notes", "status", "created_at"])
    finally:
        conn.close()
    return df
def get_checkins_df(nurse_id):
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT id, nurse_id, patient_id, checkin_time, checkout_time, status FROM checkins WHERE nurse_id = ? ORDER BY id DESC", conn, params=(nurse_id,))
    except Exception:
        df = pd.DataFrame(columns=["id", "nurse_id", "patient_id", "checkin_time", "checkout_time", "status"])
    finally:
        conn.close()
    return df
def get_hospital_memos_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT id, patient_id, nurse_id, provider_id, title, message, created_at FROM hospital_memos ORDER BY id DESC", conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "patient_id", "nurse_id", "provider_id", "title", "message", "created_at"])
    finally:
        conn.close()
    return df
def add_checkin(nurse_id, patient_id, checkin_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO checkins (nurse_id, patient_id, checkin_time, status) VALUES (?, ?, ?, 'Checked In')", (nurse_id, patient_id, checkin_time))
        conn.commit()
        return (True, "✅ Successfully checked in! Home visit session started.")
    except Exception as e:
        return (False, f"⚠️ Check-in failed: {str(e)}")
    finally:
        conn.close()
def add_assessment(patient_id, nurse_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo, send_email=True):
    conn = get_connection()
    cursor = conn.cursor()
    email_results = []
    try:
        cursor.execute("""
            INSERT INTO assessments (patient_id, nurse_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, nurse_id, blood_pressure, int(pulse_rate), float(blood_sugar), wound_condition, nurse_memo))
        conn.commit()
        
        main_msg = "✅ Assessment metrics saved successfully to the system database."
        
        if send_email:
            cursor.execute("SELECT name, email FROM patients WHERE id = ?", (patient_id,))
            patient_row = cursor.fetchone()
            
            if patient_row and patient_row[1]:
                p_name = patient_row[0]
                p_email = patient_row[1]
                
                email_subject = f"📋 Home Nursing Care Assessment Report - Patient ID: {patient_id}"
                email_body = (
                    f"Hello {p_name},\n\n"
                    f"Your home nursing care assessment report has been updated successfully.\n\n"
                    f"Assessment Details Summary:\n"
                    f"• Blood Pressure: {blood_pressure} mmHg\n"
                    f"• Pulse Rate: {pulse_rate} bpm\n"
                    f"• Blood Sugar Level: {blood_sugar} mmol/L\n"
                    f"• Wound Condition Status: {wound_condition}\n"
                    f"• Care Practitioner Memo: {nurse_memo}\n\n"
                    f"Thank you,\nHome Healthcare System Management Team"
                )
                
                email_ok, email_msg = send_real_email_notification(p_email, email_subject, email_body)
                email_results.append(email_msg)
            else:
                email_results.append("⚠️ Email not sent: Patient profile has no email address registered.")
                
        return (True, main_msg, email_results)
    except Exception as e:
        return (False, f"⚠️ Failed to save assessment metrics: {str(e)}", email_results)
    finally:
        conn.close()
def get_assessments_df():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT id, patient_id, nurse_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo, created_at FROM assessments ORDER BY id DESC", conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "patient_id", "nurse_id", "blood_pressure", "pulse_rate", "blood_sugar", "wound_condition", "nurse_memo", "created_at"])
    finally:
        conn.close()
    return df
def add_hospital_memo(patient_id, nurse_id, provider_id, title, message):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO hospital_memos (patient_id, nurse_id, provider_id, title, message) 
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, nurse_id, provider_id, title, message))
        conn.commit()
        return (True, "✅ Hospital memo successfully registered and broadcasted to the system.", [])
    except Exception as e:
        return (False, f"⚠️ Failed to save hospital memo: {str(e)}", [])
    finally:
        conn.close()


