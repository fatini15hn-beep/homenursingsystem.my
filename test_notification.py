import database as db

db.create_notification(
    1,
    "New Appointment",
    "Ahmad Patient has an appointment tomorrow at 10:00 AM.",
    "appointment"
)

print("Notification created successfully.")