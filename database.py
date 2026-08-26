import sqlite3
import pandas as pd
import streamlit as st

DB_FILE = "nursing_system.db"

# 1. Prosedur Utama: Membina database fail SQLite secara automatik dalam VS Code
def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Jadual Pesakit (Saringan umur 18-59 & ada ruangan jenis penyakit)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            illness TEXT,
            status TEXT DEFAULT 'New Case'
        )
    """)
    
    # Jadual Jururawat (Aina & Fatimah)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nurses (
            id TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            zone TEXT
        )
    """)
    
    # Jadual Laporan Rutin Harian Jururawat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            blood_pressure TEXT,
            pulse_rate INTEGER,
            blood_sugar REAL,
            wound_condition TEXT,
            nurse_memo TEXT
        )
    """)

    # Jadual Temujanji (Appointments) untuk Kalendar Admin & Nurse
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            nurse_id TEXT,
            visit_date TEXT,
            visit_time TEXT,
            notes TEXT
        )
    """)
    
    # Masukkan data contoh awal jika jadual dikesan kosong
    cursor.execute("SELECT COUNT(*) FROM patients")
    row = cursor.fetchone()
    if row and row[0] == 0:
        cursor.execute("INSERT INTO patients VALUES ('P001', 'Ahmad Ali', 35, 'Lelaki', '0123456789', 'Pasca-Pembedahan Stroke', 'Stable')")
        cursor.execute("INSERT INTO patients VALUES ('P002', 'Siti Aminah', 42, 'Perempuan', '0179876543', 'Kencing Manis & Penjagaan Luka Kronik', 'Requires Visit')")
        cursor.execute("INSERT INTO nurses VALUES ('N001', 'Nurse Aina', '0112223333', 'Zon A')")
        cursor.execute("INSERT INTO nurses VALUES ('N002', 'Nurse Fatimah', '0144445555', 'Zon B')")
        
    conn.commit()
    conn.close()

# ─── BARU: FUNGSI TAMBAHAN UNTUK MENYELESAIKAN RALAT NOTIFIKASI LOGIN ───
def initialize_notification_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Mencipta jadual notifikasi digital secara automatik jika belum wujud
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_role TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def initialize_assessment_db():
    pass

# Fungsi Menyuntik Menu Navigasi Atas Versi Korporat Premium Tanpa Emoji
def inject_top_navbar():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none !important;}
            [data-testid="stSidebarCollapseButton"] {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            .navbar-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #ffffff;
                padding: 18px 4%;
                border-bottom: 4px solid #004687;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 99999;
            }
            .logo-section {
                font-size: 14px;
                font-weight: 800;
                color: #004687;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }
            .menu-items { display: flex; gap: 25px; }
            .menu-link { text-decoration: none !important; color: #475569 !important; font-weight: 700; font-size: 14px; }
            .menu-link:hover { color: #004687 !important; }
            .main-content-padding { margin-top: 110px; }
        </style>
        
        <div class="navbar-container">
            <div class="logo-section">
                HOME NURSING SYSTEM FOR POST-DISCHARGE PATIENTS FOLLOW-UP
            </div>
            <div class="menu-items">
                <a href="/" target="_self" class="menu-link">PORTAL MAIN</a>
                <a href="/Home_Page" target="_self" class="menu-link">ABOUT US</a>
                <a href="/Login" target="_self" class="menu-link">LOGIN</a>
            </div>
        </div>
        <div class="main-content-padding"></div>
    """, unsafe_allow_html=True)

# Fungsi untuk Admin mendaftarkan pesakit baru (Saringan umur 18-59)
def add_patient(pt_id, name, age, gender, phone, illness):
    if not (18 <= age <= 59):
        return False, "⚠️ Gagal! Umur pesakit mestilah di antara 18 hingga 59 tahun sahaja."
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (id, name, age, gender, phone, illness) VALUES (?, ?, ?, ?, ?, ?)",
            (pt_id, name, age, gender, phone, illness)
        )
        conn.commit()
        return True, f"✅ Pesakit {name} berjaya disimpan kekal ke dalam SQLite database!"
    except sqlite3.IntegrityError:
        return False, "⚠️ Gagal! ID Pesakit ini sudah wujud."
    finally:
        conn.close()

# Fungsi untuk Admin menetapkan Temujanji Kalendar Baru
def add_appointment(pt_id, nurse_id, visit_date, visit_time, notes):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (patient_id, nurse_id, visit_date, visit_time, notes) VALUES (?, ?, ?, ?, ?)",
        (pt_id, nurse_id, str(visit_date), visit_time, notes)
    )
    conn.commit()
    conn.close()
    return True, "✅ Jadual temujanji baru berjaya didaftarkan kekal!"

# Fungsi untuk jururawat menyimpan laporan pemeriksaan harian pesakit
def add_assessment(pt_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, memo):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO assessments (patient_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, nurse_memo) VALUES (?, ?, ?, ?, ?, ?)",
        (pt_id, blood_pressure, pulse_rate, blood_sugar, wound_condition, memo)
    )
    conn.commit()
    conn.close()
    return True, "✅ Laporan pemeriksaan harian berjaya disimpan!"

# Fungsi memuatkan data dari SQLite ke bentuk jadual Pandas (Paparan pada web)
def get_patients_df():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

def get_nurses_df():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM nurses", conn)
    conn.close()
    return df

def get_assessments_df():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM assessments", conn)
    conn.close()
    return df

# Fungsi untuk mendapatkan data jadual temujanji lengkap bagi paparan web
def get_appointments_df():
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT a.id, p.name AS 'Nama Pesakit', p.illness AS 'Jenis Penyakit', 
               n.name AS 'Jururawat Bertugas', a.visit_date AS 'Tarikh Lawatan', 
               a.visit_time AS 'Masa', a.notes AS 'Nota Alatan'
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN nurses n ON a.nurse_id = n.id
        ORDER BY a.visit_date ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
