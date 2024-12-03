import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk
from tkinter.simpledialog import Dialog
from tkcalendar import Calendar
from database import get_reminders, add_reminder, delete_reminder
from datetime import datetime


class ReminderDialog(Dialog):
    def body(self, master):
        self.title("Añadir Recordatorio")

        # Campo de Nombre
        Label(master, text="Nombre del Recordatorio:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Calendario para Fecha
        Label(master, text="Fecha:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.calendar = Calendar(master, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=1, column=1, padx=10, pady=5)

        # Selector de Hora
        Label(master, text="Hora:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.hour_combobox = ttk.Combobox(master, values=[f"{i:02}" for i in range(24)], width=5)
        self.hour_combobox.set("00")
        self.hour_combobox.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="w")

        # Selector de Minutos
        self.minute_combobox = ttk.Combobox(master, values=[f"{i:02}" for i in range(60)], width=5)
        self.minute_combobox.set("00")
        self.minute_combobox.grid(row=2, column=1, padx=(80, 0), pady=5, sticky="w")

        return self.name_entry

    def apply(self):
        """Captura los datos ingresados por el usuario y valida el formato."""
        name = self.name_entry.get()
        date = self.calendar.get_date()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()

        if not name:
            messagebox.showerror("Error", "El nombre del recordatorio no puede estar vacío.")
            return

        # Crear el formato de fecha y hora final
        datetime_str = f"{date} {hour}:{minute}"
        try:
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")  # Validar formato
            add_reminder(name, datetime_str)
            messagebox.showinfo("Éxito", "Recordatorio añadido correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Fecha u hora inválida. Inténtalo de nuevo.")


class ReminderScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Recordatorios", font=("Arial", 16)).pack(pady=10)

        self.reminder_tree = ttk.Treeview(self, columns=("ID", "Nombre", "Fecha y Hora"), show="headings")
        self.reminder_tree.heading("ID", text="ID")
        self.reminder_tree.heading("Nombre", text="Nombre")
        self.reminder_tree.heading("Fecha y Hora", text="Fecha y Hora")
        self.reminder_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self, text="Añadir Recordatorio", command=self.add_reminder_dialog).pack(pady=5)
        tk.Button(self, text="Eliminar Recordatorio", command=self.delete_selected_reminder).pack(pady=5)
        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("MainScreen")).pack(pady=5)

        self.refresh_reminder_list()
        self.check_reminders()

    def refresh_reminder_list(self):
        try:
            for row in self.reminder_tree.get_children():
                self.reminder_tree.delete(row)
            reminders = get_reminders()
            for reminder in reminders:
                self.reminder_tree.insert("", "end", values=reminder)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los recordatorios: {e}")

    def add_reminder_dialog(self):
        ReminderDialog(self)
        self.refresh_reminder_list()

    def delete_selected_reminder(self):
        selected_item = self.reminder_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Selecciona un recordatorio.")
            return
        reminder_id = self.reminder_tree.item(selected_item, "values")[0]
        delete_reminder(reminder_id)
        self.refresh_reminder_list()

    def check_reminders(self):
        reminders = get_reminders()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for reminder in reminders:
            if reminder[2] == now:
                messagebox.showinfo("Recordatorio", f"¡Recordatorio!: {reminder[1]}")
                delete_reminder(reminder[0])
                self.refresh_reminder_list()
        self.after(60000, self.check_reminders)
