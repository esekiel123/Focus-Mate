import tkinter as tk
from tkinter import messagebox, simpledialog
from database import get_habits, add_habit, update_habit
from utils import get_random_completion_phrase

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
        messagebox.showinfo("¡Motivación!", get_random_completion_phrase())
