import sqlite3
from database import DB_NAME

# Funciones de hábitos
def add_habit(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        conn.commit()

def get_habits():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits")
        return cursor.fetchall()

def update_habit(habit_id, completed):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE habits SET completed = ? WHERE id = ?", (completed, habit_id))
        conn.commit()

# Funciones de recordatorios
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
