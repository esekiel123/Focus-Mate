import tkinter as tk
from utils import get_random_phrase
from screens.reminder_screen import ReminderScreen

class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text=get_random_phrase(), font=("Arial", 14), wraplength=400).pack(pady=20)
        tk.Button(self, text="Hábitos", command=lambda: controller.show_frame("HabitScreen")).pack(pady=5)
        tk.Button(self, text="Recordatorios", command=lambda: controller.show_frame("ReminderScreen")).pack(pady=5)
