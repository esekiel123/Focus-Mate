import pyaudio
import numpy as np

class EmotionDetector:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model  # Modelo preentrenado para emociones
        self.stream = None
        self.running = False

    def start_detection(self):
        self.running = True
        self.stream = self._get_audio_stream()
        while self.running:
            audio_data = self._capture_audio()
            emotion = self._analyze_emotion(audio_data)
            if emotion in ["stress", "anger", "sadness"]:
                phrase = get_random_motivation()
                self.controller.update_motivation(phrase)

    def stop_detection(self):
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def _get_audio_stream(self):
        audio = pyaudio.PyAudio()
        return audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    def _capture_audio(self):
        data = self.stream.read(1024)
        audio_data = np.frombuffer(data, dtype=np.int16)
        return audio_data

    def _analyze_emotion(self, audio_data):
        # Convierte el audio en características para el modelo
        features = extract_features(audio_data)
        emotion = self.model.predict(features)  # Simulación de predicción
        return emotion

def extract_features(audio_data):
    # Procesamiento del audio (por ejemplo, extracción de MFCC)
    return np.random.rand(20)  # Datos ficticios para este ejemplo
