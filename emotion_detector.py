import cv2
from deepface import DeepFace

class EmotionDetector:
    def __init__(self, update_callback=None):
        """
        Inicializa el detector de emociones.
        :param update_callback: Función a llamar cuando se detecta una emoción.
        """
        self.update_callback = update_callback
        self.running = False

    def start_detection(self):
        """
        Inicia el detector de emociones.
        """
        self.running = True
        cap = cv2.VideoCapture(0)  # Activa la cámara
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Analiza el frame para detectar emociones
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                emotion = result['dominant_emotion']
                if self.update_callback:
                    self.update_callback(emotion)  # Llama a la función para actualizar la interfaz
            except Exception as e:
                print(f"Error en la detección de emociones: {e}")
            
            # Muestra el feed de la cámara en una ventana (opcional)
            cv2.imshow("Detector de Emociones", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir al presionar 'q'
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop_detection(self):
        """
        Detiene el detector de emociones.
        """
        self.running = False
