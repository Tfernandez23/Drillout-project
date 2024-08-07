import tensorflow as tf
import numpy as np
import cv2
from datetime import datetime
from filescode.utils import EventLogger  # Asegúrate de que la ruta sea correcta

class ModelPredictor:
    def __init__(self, model_path, img_height=150, img_width=150):
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"Modelo cargado correctamente desde {model_path}")
        except IOError:
            print(f"Error: No se pudo encontrar el archivo del modelo en {model_path}")
            self.model = None
        self.img_height = img_height
        self.img_width = img_width
        self.class_labels = {0: 'Water', 1: 'BlueWater', 2: 'Empthy'}
        self.logger = EventLogger()  # Instancia de EventLogger para registrar predicciones

    def predict(self, frame, camera_name):
        if self.model is None:
            print("Modelo no cargado")
            return "No model loaded"
        
        frame = cv2.resize(frame, (self.img_width, self.img_height))  # Ajustar al tamaño correcto
        frame = frame.astype('float32') / 255.0  # Normalización
        frame = np.expand_dims(frame, axis=0)  # Expandir dimensiones para que sea compatible con el modelo

        prediction = self.model.predict(frame)
        predicted_class = np.argmax(prediction, axis=1)[0]  # Obtener la clase predicha
        predicted_label = self.class_labels[predicted_class]  # Obtener el nombre de la clase
        confidence = np.max(prediction) * 100  # Obtener la confianza de la predicción

        print(f'Predicción: {predicted_label}')
        print(f'Confianza: {confidence:.2f}%')

        # Formatear el mensaje para registrar en el archivo de texto
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{camera_name},{timestamp},{predicted_label},{confidence:.2f}%"
        
        # Registrar la predicción en el archivo de texto
        self.logger.log_event(log_message)

        return predicted_label, confidence

