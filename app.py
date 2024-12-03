import tkinter as tk
from PIL import Image, ImageTk
from habit_screen import HabitScreen
from reminder_screen import ReminderScreen
from database import init_db
from utils import get_random_motivation

class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configuración de fondo y estilos
        self.configure(bg="#f0f8ff")  # Fondo azul claro

        # Título de bienvenida
        title_label = tk.Label(
            self, text="¡Bienvenido a Focus Mate!", 
            font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#333"
        )
        title_label.pack(pady=10)

        # Cargar y mostrar la imagen
        self.image = Image.open("penguin.png")
        self.image = self.image.resize((150, 150), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image=self.image_tk, bg="#f0f8ff")
        self.image_label.pack(pady=10)

        # Etiqueta de motivación
        self.motivation_label = tk.Label(
            self, text=get_random_motivation(), 
            font=("Arial", 14), wraplength=400, bg="#f0f8ff", fg="#555"
        )
        self.motivation_label.pack(pady=10)

        # Botones con estilos
        button_style = {"font": ("Arial", 12), "bg": "#87ceeb", "fg": "#fff", "relief": "raised", "bd": 2}
        tk.Button(
            self, text="Gestionar Hábitos", 
            command=lambda: controller.show_frame("HabitScreen"), **button_style
        ).pack(pady=5, ipadx=10, ipady=5)

        tk.Button(
            self, text="Gestionar Recordatorios", 
            command=lambda: controller.show_frame("ReminderScreen"), **button_style
        ).pack(pady=5, ipadx=10, ipady=5)

        tk.Button(
            self, text="Salir", command=controller.on_close, 
            font=("Arial", 12), bg="#f08080", fg="#fff", relief="raised", bd=2
        ).pack(pady=20, ipadx=10, ipady=5)

    def update_motivation_label(self, phrase):
        """Actualiza el texto de la etiqueta de motivación."""
        self.motivation_label.config(text=phrase)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motivador Personal")
        self.geometry("800x600")
        self.configure(bg="#f0f8ff")  # Fondo de la ventana principal
        self.frames = {}

        # Crear las pantallas
        for FrameClass in (MainScreen, HabitScreen, ReminderScreen):
            frame = FrameClass(parent=self, controller=self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_frame("MainScreen")

    def show_frame(self, page_name):
        """Muestra la pantalla especificada por su nombre."""
        frame = self.frames[page_name]
        frame.tkraise()

    def update_motivation(self, phrase):
        """Actualiza la frase motivacional en la interfaz cuando se detecta una emoción negativa."""
        if "MainScreen" in self.frames:
            self.frames["MainScreen"].update_motivation_label(phrase)

    def on_close(self):
        """Cierra la aplicación correctamente."""
        if hasattr(self, "emotion_detector") and self.emotion_detector:
            self.emotion_detector.stop_detection()
        self.destroy()

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    else:
        app = App()
        app.mainloop()
