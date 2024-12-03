import sqlite3
from datetime import datetime

DB_NAME = "motivador_personal.db"

def add_reminder(name, datetime_):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reminders (name, datetime) VALUES (?, ?)", (name, datetime_))
        conn.commit()

def get_reminders():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminders ORDER BY datetime")
        return cursor.fetchall()

def delete_reminder(reminder_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        conn.commit()
