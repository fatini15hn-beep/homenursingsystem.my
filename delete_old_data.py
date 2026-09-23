import sqlite3

# 1. Connect to your database file
# (Note: If your database file has a different name like 'system.db', change it below)
database_name = "home_nursing.db" 

conn = sqlite3.connect(database_name)
cursor = conn.cursor()

try:
    print("Starting the database cleanup process...")
    
    # 2. Delete all records from the appointments table
    cursor.execute("DELETE FROM appointments")
    conn.commit()
    
    print("✅ SUCCESS! All old appointment records (Fatini & Sarah) have been cleared.")
    print("Please refresh your Streamlit dashboard now.")

except sqlite3.OperationalError as e:
    print(f"❌ Error: Table not found or the .db file name is incorrect ({e})")
    print("Please check your 'database.py' file to find the correct database file name.")
    
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    
finally:
    conn.close()
