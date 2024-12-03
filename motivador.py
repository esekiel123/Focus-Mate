import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter.ttk import Combobox, Treeview
import sqlite3
import threading
import random
import time
from datetime import datetime
from matplotlib import pyplot as plt

# Base de datos
DB_NAME = "motivador_personal.db"

PHRASES = [
    "¡Nunca te rindas, hoy es un buen día para comenzar!",
    "Los pequeños pasos te llevan lejos.",
    "Recuerda por qué empezaste.",
    "¡Eres capaz de grandes cosas!",
    "Cada día es una oportunidad de mejorar."
]

COMPLETION_PHRASES = [
    "¡Bien hecho! Cada hábito te acerca a tus metas.",
    "¡Sigue así, estás haciendo un gran trabajo!",
    "¡Increíble! Otro hábito completado con éxito.",
    "¡Felicidades! Estás construyendo una versión mejorada de ti mismo.",
    "¡Eres imparable! Mantén el ritmo."
]

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Tabla de hábitos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)
        # Tabla de usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                interests TEXT
            )
        """)
        # Tabla de recordatorios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        """)
        conn.commit()

# Funciones para hábitos
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

# Pantallas
class HabitScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Hábitos", font=("Arial", 16)).pack(pady=10)
        self.habit_list = tk.Listbox(self, selectmode=tk.SINGLE)
        self.habit_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(self, text="Añadir Hábito", command=self.add_habit_dialog).pack(pady=5)
        tk.Button(self, text="Marcar Completado", command=self.mark_habit).pack(pady=5)
        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("MainScreen")).pack(pady=5)
        self.load_habits()

    def load_habits(self):
        self.habit_list.delete(0, tk.END)
        habits = get_habits()
        for habit in habits:
            status = "✔" if habit[2] == 1 else "✗"
            self.habit_list.insert(tk.END, f"{habit[0]} - {habit[1]} [{status}]")

    def add_habit_dialog(self):
        habit_name = simpledialog.askstring("Nuevo Hábito", "Escribe el nombre del hábito:")
        if habit_name:
            add_habit(habit_name)
            self.load_habits()

    def mark_habit(self):
        selected = self.habit_list.curselection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un hábito.")
            return
        habit_id = int(self.habit_list.get(selected[0]).split(" - ")[0])
        update_habit(habit_id, 1)
        self.load_habits()
        # Mostrar mensaje motivacional
        messagebox.showinfo("¡Motivación!", random.choice(COMPLETION_PHRASES))


class ReminderScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Recordatorios", font=("Arial", 16)).pack(pady=10)
        self.reminder_tree = Treeview(self, columns=("ID", "Nombre", "Fecha y Hora"), show="headings")
        self.reminder_tree.heading("ID", text="ID")
        self.reminder_tree.heading("Nombre", text="Nombre")
        self.reminder_tree.heading("Fecha y Hora", text="Fecha y Hora")
        self.reminder_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(self, text="Añadir Recordatorio", command=self.add_reminder_dialog).pack(pady=5)
        tk.Button(self, text="Eliminar Recordatorio", command=self.delete_selected_reminder).pack(pady=5)
        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("MainScreen")).pack(pady=5)
        self.refresh_reminder_list()
        self.run_reminder_checker()

    def refresh_reminder_list(self):
        for row in self.reminder_tree.get_children():
            self.reminder_tree.delete(row)
        reminders = get_reminders()
        for reminder in reminders:
            self.reminder_tree.insert("", "end", values=reminder)

    def add_reminder_dialog(self):
        name = simpledialog.askstring("Nuevo Recordatorio", "Escribe el nombre del recordatorio:")
        datetime_ = simpledialog.askstring("Fecha y Hora", "Formato YYYY-MM-DD HH:MM:")
        if name and datetime_:
            try:
                datetime.strptime(datetime_, "%Y-%m-%d %H:%M")
                add_reminder(name, datetime_)
                self.refresh_reminder_list()
            except ValueError:
                messagebox.showerror("Error", "Fecha y hora inválidas.")

    def delete_selected_reminder(self):
        selected_item = self.reminder_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Selecciona un recordatorio.")
            return
        reminder_id = self.reminder_tree.item(selected_item, "values")[0]
        delete_reminder(reminder_id)
        self.refresh_reminder_list()

    def run_reminder_checker(self):
        def check_reminders():
            while True:
                reminders = get_reminders()
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                for reminder in reminders:
                    if reminder[2] == now:
                        messagebox.showinfo("Recordatorio", f"¡Recordatorio!: {reminder[1]}")
                        delete_reminder(reminder[0])
                        self.refresh_reminder_list()
                time.sleep(60)
        threading.Thread(target=check_reminders, daemon=True).start()

# Controlador principal
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motivador Personal")
        self.geometry("800x600")
        self.frames = {}
        for F in (MainScreen, HabitScreen, ReminderScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Inicializar la app
if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
