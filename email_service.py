import smtplib  # <-- Pastikan ada perkataan 'import' di sini
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_appointment_email(nurse_email, nurse_name, patient_name, appointment_date, appointment_time):
    # 1. Konfigurasi emel penghantar
    sender_email = "homenursingsystem1@gmail.com" 
    
    # ⚠️ Masukkan 16 aksara tanpa sebarang simbol '_' atau jarak (space)
    app_password = "ojmydojafegkptti" 

    # 2. Sediakan kandungan emel
    subject = "New Home Visit Appointment"
    body = f"""Dear Nurse {nurse_name},

A new home visit appointment has been scheduled.

Patient: {patient_name}
Date: {appointment_date}
Time: {appointment_time}

Please check your appointment schedule.

Home Nursing System"""

    # 3. Tetapkan header emel
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = nurse_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # 4. BETUL: Menggunakan 'smtp.gmail.com' (Bukan '//gmail.com')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        
        # Log masuk menggunakan App Password
        server.login(sender_email, app_password)
        
        # Hantar emel
        server.sendmail(sender_email, nurse_email, msg.as_string())
        server.quit()
        
        print(f"✅ Emel berjaya dihantar kepada {nurse_name} ({nurse_email})")
        return True
        
    except Exception as e:
        print(f"❌ Gagal menghantar emel: {e}")
        return False

# --- KOD UNTUK UJI (TEST RUN) ---
if __name__ == "__main__":
    print("Memulakan ujian penghantaran emel...")
    
    test_nurse_email = "homenursingsystem1@gmail.com" 
    
    send_appointment_email(
        nurse_email=test_nurse_email,
        nurse_name="Aina",
        patient_name="Ahmad Ali",
        appointment_date="10 September 2026",
        appointment_time="10:00 AM"
    )

